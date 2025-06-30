# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username tidak boleh kosong.')])
    password = PasswordField('Password', validators=[DataRequired(message='Password tidak boleh kosong.')])
    remember_me = BooleanField('Ingat Saya')
    submit = SubmitField('Login')

class KorbanForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired()])
    nik = StringField('NIK', validators=[Optional(), Length(min=16, max=16)])
    usia = IntegerField('Usia', validators=[Optional()])
    jenis_kelamin = SelectField(
        'Jenis Kelamin',
        choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')],
        validators=[DataRequired()]
    )
    alamat_asal = TextAreaField('Alamat Asal')
    status_korban = SelectField(
        'Status Korban',
        choices=[
            ('Selamat', 'Selamat'),
            ('Luka Ringan', 'Luka Ringan'),
            ('Luka Berat', 'Luka Berat'),
            ('Hilang', 'Hilang'),
            ('Meninggal Dunia', 'Meninggal Dunia')
        ],
        validators=[DataRequired()]
    )
    kecamatan = SelectField('Kecamatan Ditemukan', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Simpan Data')

class SearchForm(FlaskForm):
    query = StringField(
        'Cari Korban',
        validators=[DataRequired(message='Kolom pencarian tidak boleh kosong.')],
        render_kw={'placeholder': 'Masukkan Nama atau NIK...'}
    )
    submit = SubmitField('Cari')

class LaporanForm(FlaskForm):
    nama_pelapor = StringField('Nama Lengkap Anda', validators=[DataRequired()])
    kontak_pelapor = StringField('No. HP atau Kontak yang bisa dihubungi', validators=[DataRequired()])
    nama_korban_dilaporkan = StringField('Nama Korban (jika tahu)')
    status_korban = SelectField(
        'Status Korban Saat Ditemukan',
        choices=[
            ('Selamat', 'Selamat'),
            ('Luka Ringan', 'Luka Ringan'),
            ('Luka Berat', 'Luka Berat'),
            ('Hilang', 'Hilang'),
            ('Meninggal Dunia', 'Meninggal Dunia')
        ],
        validators=[DataRequired()]
    )
    kecamatan = SelectField('Kecamatan Penemuan', coerce=int, validators=[DataRequired()])
    lokasi_penemuan = TextAreaField('Lokasi Penemuan', validators=[DataRequired()])
    kondisi_saat_ditemukan = TextAreaField('Kondisi Saat Ditemukan', validators=[DataRequired()])
    submit = SubmitField('Kirim Laporan')

class InfoBencanaForm(FlaskForm):
    konten = TextAreaField('Informasi Status Bencana', validators=[DataRequired()], render_kw={'rows': 10})
    submit = SubmitField('Simpan Informasi')