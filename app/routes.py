# app/routes.py

from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from app import db
from app.models import Korban, Petugas, Kecamatan, LaporanMasyarakat # Pastikan LaporanMasyarakat diimport
from app.forms import LoginForm
from app.models import Kecamatan # Tambahkan import Kecamatan
from app.forms import KorbanForm # Tambahkan import KorbanForm
from app.forms import SearchForm, KorbanForm
from app.models import LaporanMasyarakat # Tambahkan import ini
from app.forms import LaporanForm # Tambahkan import ini
from app.models import InfoBencana # Tambahkan import ini
from app.forms import InfoBencanaForm # Tambahkan import ini
from collections import defaultdict

# --- Bagian Penting ---
# Definisikan Blueprint di sini
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    hasil_pencarian = []

    if form.validate_on_submit():
        query = form.query.data
        search_term = f"%{query}%"
        hasil_pencarian = Korban.query.filter(
            or_(
                Korban.nama_lengkap.like(search_term),
                Korban.nik.like(search_term)
            )
        ).all()

        if not hasil_pencarian:
            flash('Data korban tidak ditemukan.', 'warning')
        else:
            flash(f'Menampilkan {len(hasil_pencarian)} hasil untuk pencarian "{query}".', 'info')
    return render_template('index.html', title='Pencarian Korban', form=form, hasil_pencarian=hasil_pencarian)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Petugas.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Username atau password salah', 'danger')
            return redirect(url_for('main.login'))
        
        login_user(user, remember=form.remember_me.data)
        flash('Login berhasil!', 'success')
        
        return redirect(url_for('main.dashboard'))
        
    return render_template('login.html', title='Login Petugas', form=form, hide_nav=True)

@main.route('/logout')
def logout():
    logout_user()
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    # --- Data untuk Tabel Utama ---
    daftar_korban = Korban.query.order_by(Korban.tanggal_update.desc()).all()

    # --- Data untuk Notifikasi ---
    jumlah_laporan_baru = LaporanMasyarakat.query.filter_by(status_verifikasi='Menunggu Verifikasi').count()

    # --- Data untuk Kartu Statistik ---
    total_korban = Korban.query.count()
    statistik_status = defaultdict(int)
    for korban in daftar_korban: # Kita gunakan lagi data yang sudah diambil
        statistik_status[korban.status_korban] += 1

    # --- Data untuk Tabel Laporan Terbaru ---
    laporan_terbaru = LaporanMasyarakat.query.filter_by(status_verifikasi='Menunggu Verifikasi').order_by(LaporanMasyarakat.tanggal_laporan.desc()).limit(5).all()

    return render_template('dashboard.html', 
                           title='Dashboard', 
                           daftar_korban=daftar_korban, 
                           jumlah_laporan_baru=jumlah_laporan_baru,
                           total_korban=total_korban,
                           statistik_status=statistik_status,
                           laporan_terbaru=laporan_terbaru)

@main.route('/korban/tambah', methods=['GET', 'POST'])
@login_required
def tambah_korban():
    form = KorbanForm()
    # Mengisi pilihan dropdown kecamatan dari database
    form.kecamatan.choices = [(k.id, k.nama_kecamatan) for k in Kecamatan.query.order_by('nama_kecamatan').all()]

    if form.validate_on_submit():
        # Buat objek Korban baru dengan data dari form
        korban_baru = Korban(
            nama_lengkap=form.nama_lengkap.data,
            nik=form.nik.data,
            usia=form.usia.data,
            jenis_kelamin=form.jenis_kelamin.data,
            alamat_asal=form.alamat_asal.data,
            status_korban=form.status_korban.data,
            kecamatan_id=form.kecamatan.data,
            petugas=current_user  # Menghubungkan dengan admin yang sedang login
        )
        db.session.add(korban_baru)
        db.session.commit()
        flash(f'Data korban an. {korban_baru.nama_lengkap} berhasil ditambahkan!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('form_korban.html', title='Tambah Data Korban', form=form)

@main.route('/korban/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_korban(id):
    # Ambil data korban dari database berdasarkan ID-nya. 
    # get_or_404 akan otomatis menampilkan halaman Not Found jika ID tidak ada.
    korban = Korban.query.get_or_404(id)
    form = KorbanForm()
    # Mengisi pilihan dropdown kecamatan
    form.kecamatan.choices = [(k.id, k.nama_kecamatan) for k in Kecamatan.query.order_by('nama_kecamatan').all()]

    if form.validate_on_submit():
        # Jika form disubmit, update data object korban dengan data baru dari form
        korban.nama_lengkap = form.nama_lengkap.data
        korban.nik = form.nik.data
        korban.usia = form.usia.data
        korban.jenis_kelamin = form.jenis_kelamin.data
        korban.alamat_asal = form.alamat_asal.data
        korban.status_korban = form.status_korban.data
        korban.kecamatan_id = form.kecamatan.data
        korban.petugas = current_user # Update petugas yang terakhir mengedit
        db.session.commit() # Simpan perubahan ke database
        flash('Data korban berhasil diperbarui!', 'success')
        return redirect(url_for('main.dashboard'))

    # Jika ini adalah request GET (pertama kali halaman dimuat)
    # Isi form dengan data yang ada dari database
    form.nama_lengkap.data = korban.nama_lengkap
    form.nik.data = korban.nik
    form.usia.data = korban.usia
    form.jenis_kelamin.data = korban.jenis_kelamin
    form.alamat_asal.data = korban.alamat_asal
    form.status_korban.data = korban.status_korban
    form.kecamatan.data = korban.kecamatan_id

    return render_template('form_korban.html', title='Edit Data Korban', form=form)

@main.route('/korban/hapus/<int:id>', methods=['POST'])
@login_required
def hapus_korban(id):
    # Cari korban berdasarkan ID, jika tidak ada, tampilkan 404 Not Found
    korban_untuk_dihapus = Korban.query.get_or_404(id)

    # Simpan nama untuk pesan flash sebelum dihapus
    nama = korban_untuk_dihapus.nama_lengkap

    db.session.delete(korban_untuk_dihapus)
    db.session.commit()

    flash(f'Data korban an. {nama} telah berhasil dihapus.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/korban/detail/<int:id>')
@login_required
def detail_korban(id):
    korban = Korban.query.get_or_404(id)
    return render_template('detail_korban.html', title='Detail Korban', korban=korban)

@main.route('/lapor', methods=['GET', 'POST'])
def lapor():
    form = LaporanForm()
    form.kecamatan.choices = [(k.id, k.nama_kecamatan) for k in Kecamatan.query.order_by('nama_kecamatan').all()]
    if form.validate_on_submit():
        laporan_baru = LaporanMasyarakat(
            nama_pelapor=form.nama_pelapor.data,
            kontak_pelapor=form.kontak_pelapor.data,
            nama_korban_dilaporkan=form.nama_korban_dilaporkan.data,
            kondisi_saat_ditemukan=f"Status: {form.status_korban.data}. Catatan: {form.kondisi_saat_ditemukan.data}",
            lokasi_penemuan=f"Kecamatan {Kecamatan.query.get(form.kecamatan.data).nama_kecamatan}. Detail: {form.lokasi_penemuan.data}"
        )
        db.session.add(laporan_baru)
        db.session.commit()
        flash('Terima kasih! Laporan Anda telah berhasil dikirim dan akan segera diverifikasi oleh petugas.', 'success')
        return redirect(url_for('main.index'))

    return render_template('form_laporan.html', title='Buat Laporan Temuan', form=form, hide_nav=True)

@main.route('/admin/laporan')
@login_required
def daftar_laporan():
    # Ambil semua laporan yang masih menunggu
    laporan_masuk = LaporanMasyarakat.query.filter_by(status_verifikasi='Menunggu Verifikasi').order_by(LaporanMasyarakat.tanggal_laporan.asc()).all()
    return render_template('daftar_laporan.html', title='Verifikasi Laporan', daftar_laporan=laporan_masuk)

@main.route('/laporan/setujui/<int:id>', methods=['POST'])
@login_required
def setujui_laporan(id):
    laporan = LaporanMasyarakat.query.get_or_404(id)
    if laporan.status_verifikasi == 'Menunggu Verifikasi':
        # Buat data korban baru dari laporan.
        # Anda bisa sesuaikan data default jika diperlukan.
        korban_baru = Korban(
            nama_lengkap=laporan.nama_korban_dilaporkan or 'Belum Teridentifikasi',
            lokasi_ditemukan=laporan.lokasi_penemuan,
            catatan=f"Berdasarkan laporan dari {laporan.nama_pelapor}. Kondisi: {laporan.kondisi_saat_ditemukan}",
            # Asumsi default, bisa diubah admin nanti
            status_korban='Selamat', 
            kecamatan_id=1, # Ganti dengan ID kecamatan default atau buat pilihan
            petugas=current_user
        )
        db.session.add(korban_baru)
        
        # Ubah status laporan
        laporan.status_verifikasi = 'Disetujui'
        db.session.commit()
        flash('Laporan berhasil disetujui dan data korban baru telah ditambahkan.', 'success')
    else:
        flash('Laporan ini sudah pernah ditindaklanjuti.', 'warning')
        
    return redirect(url_for('main.daftar_laporan'))

@main.route('/laporan/tolak/<int:id>', methods=['POST'])
@login_required
def tolak_laporan(id):
    laporan = LaporanMasyarakat.query.get_or_404(id)
    if laporan.status_verifikasi == 'Menunggu Verifikasi':
        laporan.status_verifikasi = 'Ditolak'
        db.session.commit()
        flash('Laporan telah ditolak.', 'info')
    else:
        flash('Laporan ini sudah pernah ditindaklanjuti.', 'warning')
        
    return redirect(url_for('main.daftar_laporan'))

@main.route('/admin/info-bencana')
@login_required
def daftar_info():
    # Ambil semua data kecamatan untuk ditampilkan
    semua_kecamatan = Kecamatan.query.order_by('nama_kecamatan').all()
    return render_template('daftar_info.html', title='Manajemen Info Bencana', daftar_kecamatan=semua_kecamatan)

@main.route('/admin/info-bencana/edit/<int:kecamatan_id>', methods=['GET', 'POST'])
@login_required
def edit_info_bencana(kecamatan_id):
    kecamatan = Kecamatan.query.get_or_404(kecamatan_id)
    # Cari info yang terhubung dengan kecamatan ini, atau buat baru jika belum ada
    info = InfoBencana.query.filter_by(kecamatan_id=kecamatan.id).first()
    if not info:
        info = InfoBencana(kecamatan=kecamatan, konten='')

    form = InfoBencanaForm()
    if form.validate_on_submit():
        info.konten = form.konten.data
        info.petugas = current_user
        db.session.add(info)
        db.session.commit()
        flash(f'Informasi untuk Kecamatan {kecamatan.nama_kecamatan} berhasil diperbarui.', 'success')
        return redirect(url_for('main.daftar_info'))
    
    # Saat halaman pertama kali dimuat (GET), isi form dengan data yang ada
    form.konten.data = info.konten
    
    return render_template('form_info.html', title=f'Edit Info: {kecamatan.nama_kecamatan}', form=form)

@main.route('/info-bencana')
def public_info_list():
    semua_info = InfoBencana.query.filter(InfoBencana.konten != '').order_by(InfoBencana.terakhir_diperbarui.desc()).all()
    return render_template('public_info_list.html', title='Informasi Bencana Terkini', semua_info=semua_info)

@main.route('/info-bencana/<int:kecamatan_id>')
def public_info_detail(kecamatan_id):
    info = InfoBencana.query.filter_by(kecamatan_id=kecamatan_id).first_or_404()
    return render_template('public_info_detail.html', title=f"Info Kecamatan {info.kecamatan.nama_kecamatan}", info=info)

@main.route('/admin/visualisasi', methods=['GET'])
@login_required
def visualisasi():
    kecamatan_id_filter = request.args.get('kecamatan_id', 0, type=int)

    # Siapkan query dasar
    query_korban = Korban.query
    if kecamatan_id_filter != 0:
        query_korban = query_korban.filter(Korban.kecamatan_id == kecamatan_id_filter)

    semua_korban = query_korban.all()
    semua_kecamatan = Kecamatan.query.order_by('nama_kecamatan').all()
    
    # --- PERBAIKAN LOGIKA DI SINI ---
    # Hitung kedua statistik berdasarkan hasil query 'semua_korban'
    # tanpa dibatasi oleh kondisi if.
    
    # 1. Statistik berdasarkan Status Korban
    statistik_status = defaultdict(int)
    for korban in semua_korban:
        statistik_status[korban.status_korban] += 1
    
    # 2. Statistik berdasarkan Kecamatan
    statistik_per_kecamatan = defaultdict(int)
    for korban in semua_korban:
        if korban.kecamatan:
            statistik_per_kecamatan[korban.kecamatan.nama_kecamatan] += 1

    sorted_statistik_status = sorted(statistik_status.items(), key=lambda item: item[1], reverse=True)
    sorted_statistik_kecamatan = sorted(statistik_per_kecamatan.items(), key=lambda item: item[1], reverse=True)

    return render_template('visualisasi_admin.html', 
                           title='Visualisasi Data Korban',
                           semua_kecamatan=semua_kecamatan,
                           kecamatan_id_terpilih=kecamatan_id_filter,
                           # DIUBAH: Kirim data yang sudah diurutkan ke template
                           statistik_status=sorted_statistik_status,
                           statistik_per_kecamatan=sorted_statistik_kecamatan)