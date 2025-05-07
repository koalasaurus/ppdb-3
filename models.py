from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Model untuk User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    school = db.Column(db.String(100), nullable=True)  # Asal sekolah
    address = db.Column(db.String(200), nullable=True)  # Alamat
    birth_date = db.Column(db.Date, nullable=True)  # Tanggal lahir
    phone = db.Column(db.String(15), nullable=True)  # Nomor telepon
    gender = db.Column(db.String(20), nullable=True)  # Jenis kelamin
    hobby = db.Column(db.String(200), nullable=True)  # Hobi
    parent_name = db.Column(db.String(100), nullable=True)  # Nama orang tua/wali
    parent_job = db.Column(db.String(100), nullable=True)  # Pekerjaan orang tua/wali
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Waktu pendaftaran

# Model untuk Admin
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Waktu pembuatan akun admin

# Model untuk Notifikasi
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relasi ke tabel User
    message = db.Column(db.String(255), nullable=False)  # Pesan notifikasi
    is_read = db.Column(db.Boolean, default=False)  # Status apakah notifikasi sudah dibaca
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Waktu notifikasi dibuat

    # Relasi ke User
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))