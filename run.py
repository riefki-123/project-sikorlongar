# run.py

from app import create_app, db
from app.models import Petugas, Korban, Kecamatan, InfoBencana, LaporanMasyarakat
from faker import Faker
import random

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'Petugas': Petugas, 
        'Korban': Korban,
        'Kecamatan': Kecamatan
    }

@app.cli.command("db_reset")
def db_reset():
    """Membersihkan semua data dan membuat ulang tabel."""
    db.drop_all()
    db.create_all()
    print("Database berhasil di-reset.")

@app.cli.command("seed")
def seed():
    """Mengisi database dengan data contoh."""
    print("Memulai proses seeding...")

    # Hapus data lama agar tidak duplikat
    Korban.query.delete()
    Kecamatan.query.delete()
    Petugas.query.delete()
    db.session.commit()

    # --- Membuat Data Kecamatan ---
    nama_kecamatan = ["Cisurupan", "Cikajang", "Bayongbong", "Garut Kota", "Samarang", "Pasirwangi"]
    list_kecamatan_obj = []
    for nama in nama_kecamatan:
        kec = Kecamatan(nama_kecamatan=nama)
        list_kecamatan_obj.append(kec)
        db.session.add(kec)
    db.session.commit()
    print(f"{len(list_kecamatan_obj)} data kecamatan dibuat.")

    # --- Membuat 1 Data Petugas ---
    admin_user = Petugas(nama_lengkap='Admin Utama', username='admin')
    admin_user.set_password('password') # Ganti dengan password yang aman
    db.session.add(admin_user)
    db.session.commit()
    print("1 data petugas dibuat (username: admin, pass: password).")
    
    # --- Membuat 10 Data Korban dengan Faker ---
    faker = Faker('id_ID') # Menggunakan data regional Indonesia
    status_list = ['Selamat', 'Luka Ringan', 'Luka Berat', 'Hilang', 'Meninggal Dunia']
    
    for i in range(10):
        korban = Korban(
            nama_lengkap=faker.name(),
            nik=faker.ssn(),
            usia=random.randint(5, 70),
            jenis_kelamin=random.choice(['Laki-laki', 'Perempuan']),
            alamat_asal=faker.address(),
            status_korban=random.choice(status_list),
            kecamatan=random.choice(list_kecamatan_obj),
            petugas=admin_user
        )
        db.session.add(korban)
    
    db.session.commit()
    print("10 data korban dummy berhasil dibuat.")
    print("Proses seeding selesai.")

if __name__ == '__main__':
    app.run(debug=True)