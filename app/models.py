# app/models.py

from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Fungsi user_loader yang dibutuhkan oleh Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Petugas.query.get(int(user_id))

# Class Petugas akan menjadi tabel 'petugas'
class Petugas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    
    # Relasi ke tabel lain
    korban_updates = db.relationship('Korban', backref='petugas', lazy='dynamic')
    info_updates = db.relationship('InfoBencana', backref='petugas', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Petugas {self.username}>'

# Class Kecamatan akan menjadi tabel 'kecamatan'
class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_kecamatan = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relasi
    korban = db.relationship('Korban', backref='kecamatan', lazy=True)
    info_bencana = db.relationship('InfoBencana', backref='kecamatan', uselist=False, lazy=True) # one-to-one

    def __repr__(self):
        return f'<Kecamatan {self.nama_kecamatan}>'

# Class Korban akan menjadi tabel 'korban'
class Korban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(150), nullable=False, index=True)
    nik = db.Column(db.String(16), unique=True, nullable=True, index=True)
    usia = db.Column(db.Integer)
    jenis_kelamin = db.Column(db.String(20))
    alamat_asal = db.Column(db.Text)
    lokasi_ditemukan = db.Column(db.String(255))
    status_korban = db.Column(db.String(50), nullable=False, default='Hilang', index=True)
    catatan = db.Column(db.Text)
    tanggal_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    kecamatan_id = db.Column(db.Integer, db.ForeignKey('kecamatan.id'), nullable=False)
    petugas_id = db.Column(db.Integer, db.ForeignKey('petugas.id'))

    def __repr__(self):
        return f'<Korban {self.nama_lengkap}>'

# Class LaporanMasyarakat akan menjadi tabel 'laporan_masyarakat'
class LaporanMasyarakat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_pelapor = db.Column(db.String(100), nullable=False)
    kontak_pelapor = db.Column(db.String(50))
    nama_korban_dilaporkan = db.Column(db.String(150))
    lokasi_penemuan = db.Column(db.Text)
    kondisi_saat_ditemukan = db.Column(db.Text)
    foto_url = db.Column(db.String(255))
    status_verifikasi = db.Column(db.String(50), nullable=False, default='Menunggu Verifikasi', index=True)
    tanggal_laporan = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Laporan dari {self.nama_pelapor}>'

# Class InfoBencana akan menjadi tabel 'info_bencana'
class InfoBencana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    konten = db.Column(db.Text, nullable=False)
    terakhir_diperbarui = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    kecamatan_id = db.Column(db.Integer, db.ForeignKey('kecamatan.id'), unique=True, nullable=False)
    petugas_id = db.Column(db.Integer, db.ForeignKey('petugas.id'))

    def __repr__(self):
        return f'<Info untuk {self.kecamatan.nama_kecamatan}>'