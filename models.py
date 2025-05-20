from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Model untuk User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    school = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    hobby = db.Column(db.String(100))
    parent_name = db.Column(db.String(100))
    parent_job = db.Column(db.String(100))
    ijazah = db.Column(db.String(200))  # Link ke file ijazah
    kk = db.Column(db.String(200))  # Link ke file kartu keluarga
    ijazah_confirmed = db.Column(db.Boolean, default=False)  # Status konfirmasi ijazah
    kk_confirmed = db.Column(db.Boolean, default=False)  # Status konfirmasi KK
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Waktu pendaftaran
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    payment_proof = db.Column(db.String(200))  # Path ke file bukti pembayaran
    is_action_taken = db.Column(db.Boolean, default=False)  # True jika admin sudah mengambil tindakan
    is_payment_action_taken = db.Column(db.Boolean, default=False)  # True jika admin sudah mengambil tindakan pada pembayaran
    faculty = db.Column(db.String(100))  # Fakultas pilihan user
    religion = db.Column(db.String(30))  # Tambahkan ini

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