from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Notification, Admin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inisialisasi database
db.init_app(app)
migrate = Migrate(app, db)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email sudah terdaftar. Gunakan email lain.')
            return redirect(url_for('register'))
        # Validasi password dan konfirmasi password
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.')
            return redirect(url_for('register'))
        # Hash password sebelum menyimpannya
        hashed_password = generate_password_hash(password)
        name = request.form['name']
        user = User(name=name, email=email, password=hashed_password)  # Simpan hash password
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Periksa apakah user adalah admin
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('dashboard_admin'))

        # Periksa apakah user adalah user biasa
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):  # Periksa hash password
            session['user_id'] = user.id
            return redirect(url_for('dashboard_user', user_id=user.id))

        flash('Email atau password salah.')
        return redirect(url_for('login'))
    return render_template('login.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Formulir Pendaftaran
@app.route('/form/<int:user_id>', methods=['GET', 'POST'])
def form(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan.')
        return redirect(url_for('dashboard_user', user_id=user_id))

    if request.method == 'POST':
        # Reset status tindakan admin
        user.is_action_taken = False

        # Validasi input
        if not request.form['name']:
            flash('Nama tidak boleh kosong.')
            return redirect(url_for('form', user_id=user_id))
        if not request.form['address']:
            flash('Alamat tidak boleh kosong.')
            return redirect(url_for('form', user_id=user_id))
        if not request.form['school']:
            flash('Asal sekolah tidak boleh kosong.')
            return redirect(url_for('form', user_id=user_id))

        user.name = request.form['name']
        user.address = request.form['address']
        user.school = request.form['school']
        user.faculty = request.form.get('faculty')

        # Perbaikan di sini: konversi birth_date ke objek date
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                user.birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            except ValueError:
                user.birth_date = None
        else:
            user.birth_date = None

        user.phone = request.form.get('phone')
        user.gender = request.form.get('gender')
        user.hobby = request.form.get('hobby')
        user.parent_name = request.form.get('parent_name')
        user.parent_job = request.form.get('parent_job')
        user.religion = request.form.get('religion')

        # Proses unggahan file ijazah
        if 'ijazah' in request.files:
            ijazah = request.files['ijazah']
            if ijazah and allowed_file(ijazah.filename):
                filename = secure_filename(f"{user.id}_ijazah_{ijazah.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                ijazah.save(filepath)
                user.ijazah = f"uploads/{filename}"

        # Proses unggahan file kartu keluarga
        if 'kk' in request.files:
            kk = request.files['kk']
            if kk and allowed_file(kk.filename):
                filename = secure_filename(f"{user.id}_kk_{kk.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                kk.save(filepath)
                user.kk = f"uploads/{filename}"

        db.session.commit()
        flash('Formulir berhasil disimpan.')
        return redirect(url_for('dashboard_user', user_id=user.id))

    return render_template('form.html', user=user)

# Dashboard User
@app.route('/dashboard_user/<int:user_id>', methods=['GET', 'POST'])
def dashboard_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan.')
        return redirect(url_for('index'))

    # Hitung progres pendaftaran
    fields = [
        bool(user.name),
        bool(user.email),
        bool(user.address),
        bool(user.school),
        bool(user.faculty),
        bool(user.birth_date),
        bool(user.phone),
        bool(user.gender),
        bool(user.religion),  # <--- Tambahkan baris ini
        bool(user.hobby),
        bool(user.parent_name),
        bool(user.parent_job),
        bool(user.ijazah),
        bool(user.kk),
        bool(user.ijazah_confirmed),
        bool(user.kk_confirmed),
        user.payment_status == 'Approved'
    ]
    total_fields = len(fields)
    filled_fields = sum(fields)
    progress = int((filled_fields / total_fields) * 100)

    # Ambil notifikasi terbaru untuk user
    notification = Notification.query.filter_by(user_id=user.id).order_by(Notification.id.desc()).first()

    return render_template('dashboard_user.html', user=user, progress=progress, notification=notification)

# Dashboard Admin
@app.route('/dashboard_admin', methods=['GET', 'POST'])
def dashboard_admin():
    if 'admin_id' not in session:
        flash('Anda harus login sebagai admin untuk mengakses halaman ini.')
        return redirect(url_for('login'))

    # Urutkan user berdasarkan waktu submit terbaru
    users = User.query.order_by(User.created_at.desc()).all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Ambil ID user dari form
        action = request.form.get('action')  # Ambil aksi (approve/reject) dari form
        user = User.query.get(user_id)

        if not user:
            flash('User tidak ditemukan.')
            return redirect(url_for('dashboard_admin'))

        # Proses aksi untuk data user
        if action == 'approve':
            user.status = 'Approved'
            user.is_action_taken = True
            add_notification(user.id, "Data Anda telah diterima oleh admin.")
            flash(f'Data user {user.name} telah diterima.')
        elif action == 'reject':
            user.status = 'Rejected'
            user.is_action_taken = True
            add_notification(user.id, "Data Anda ditolak oleh admin.")
            flash(f'Data user {user.name} ditolak.')

        # Proses aksi untuk pembayaran
        elif action == 'approve_payment':
            user.payment_status = 'Approved'
            user.is_payment_action_taken = True
            add_notification(user.id, "Pembayaran Anda telah diterima oleh admin.")
            flash(f'Pembayaran user {user.name} telah diterima.')
        elif action == 'reject_payment':
            user.payment_status = 'Rejected'
            user.is_payment_action_taken = True
            add_notification(user.id, "Pembayaran Anda ditolak oleh admin.")
            flash(f'Pembayaran user {user.name} ditolak.')

        db.session.commit()  # Simpan perubahan ke database
        return redirect(url_for('dashboard_admin'))

    return render_template('dashboard_admin.html', users=users)

# Tambahkan notifikasi untuk user
def add_notification(user_id, message):
    # Periksa apakah sudah ada notifikasi untuk user
    existing_notification = Notification.query.filter_by(user_id=user_id).first()
    if existing_notification:
        # Perbarui pesan notifikasi jika sudah ada
        existing_notification.message = message
        existing_notification.is_read = False  # Tandai sebagai belum dibaca
    else:
        # Tambahkan notifikasi baru jika belum ada
        notification = Notification(user_id=user_id, message=message)
        db.session.add(notification)
    db.session.commit()

# Contoh penggunaan di route
@app.route('/send_notification/<int:user_id>')
def send_notification(user_id):
    add_notification(user_id, "Pendaftaran Anda sedang diproses.")
    return "Notifikasi berhasil dikirim!"

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)  # Hapus session admin
    flash('Anda telah logout.')
    return redirect(url_for('index'))

@app.route('/debug_users')
def debug_users():
    users = User.query.all()
    return {user.email: {"is_admin": False, "password": user.password} for user in users}

@app.route('/debug_admins')
def debug_admins():
    admins = Admin.query.all()
    return {admin.email: {"name": admin.name, "password": admin.password} for admin in admins}

@app.route('/user_detail/<int:user_id>')
def user_detail(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan.')
        return redirect(url_for('dashboard_admin'))

    return render_template('user_detail.html', user=user)

@app.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
    return redirect(url_for('dashboard_user', user_id=notification.user_id))

@app.route('/confirm_documents/<int:user_id>', methods=['POST'])
def confirm_documents(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan.')
        return redirect(url_for('dashboard_admin'))

    document = request.form.get('document')
    if document == 'ijazah':
        user.ijazah_confirmed = True
        flash('Ijazah berhasil dikonfirmasi.')
    elif document == 'kk':
        user.kk_confirmed = True
        flash('Kartu Keluarga berhasil dikonfirmasi.')

    db.session.commit()
    return redirect(url_for('user_detail', user_id=user.id))

@app.route('/payment/<int:user_id>', methods=['GET', 'POST'])
def payment(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan.')
        return redirect(url_for('dashboard_user', user_id=user_id))

    if request.method == 'POST':
        if 'payment_proof' in request.files:
            payment_proof = request.files['payment_proof']
            if payment_proof and allowed_file(payment_proof.filename):
                filename = secure_filename(f"{user.id}_payment_{payment_proof.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                payment_proof.save(filepath)
                user.payment_proof = f"uploads/{filename}"  # Simpan path relatif ke folder static
                user.payment_status = 'Pending'  # Set status pembayaran menjadi Pending
                db.session.commit()
                flash('Bukti pembayaran berhasil dikirim. Menunggu konfirmasi admin.')
                return redirect(url_for('dashboard_user', user_id=user.id))
            else:
                flash('File bukti pembayaran tidak valid.')
                return redirect(url_for('payment', user_id=user_id))

    return render_template('payment.html', user=user)

@app.route('/admin_report')
def admin_report():
    if 'admin_id' not in session:
        flash('Anda harus login sebagai admin untuk mengakses halaman ini.')
        return redirect(url_for('login'))

    # Hitung total users dan statistik status
    total_users = User.query.count()
    stats = {
        'approved': User.query.filter_by(status='Approved').count(),
        'rejected': User.query.filter_by(status='Rejected').count(),
        'pending': User.query.filter_by(status='Pending').count()
    }

    # Statistik per fakultas
    faculty_stats = []
    faculties = ['Teknologi Informasi', 'Ekonomi & Bisnis', 'Desain & Komunikasi']
    
    for faculty in faculties:
        faculty_data = {
            'name': faculty,
            'total': User.query.filter_by(faculty=faculty).count(),
            'approved': User.query.filter_by(faculty=faculty, status='Approved').count(),
            'rejected': User.query.filter_by(faculty=faculty, status='Rejected').count(),
            'pending': User.query.filter_by(faculty=faculty, status='Pending').count()
        }
        faculty_stats.append(faculty_data)

    # Data untuk grafik fakultas
    faculty_data = {
        'labels': faculties,
        'values': [stats['total'] for stats in faculty_stats]
    }

    # Data untuk grafik agama
    religions = ['Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha', 'Konghucu']
    religion_counts = [User.query.filter_by(religion=religion).count() for religion in religions]
    religion_data = {
        'labels': religions,
        'values': religion_counts
    }

    return render_template('admin_report.html',
                         total_users=total_users,
                         stats=stats,
                         faculty_stats=faculty_stats,
                         faculty_data=faculty_data,
                         religion_data=religion_data)

if __name__ == '__main__':
    with app.app_context():
        # Membuat tabel di database
        db.create_all()

        # Tambahkan admin secara manual
        admin = Admin.query.filter_by(email="admin@gmail.com").first()
        if not admin:
            admin = Admin(
                name="Admin",
                email="admin@gmail.com",
                password=generate_password_hash("admin123")  # Hash password
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin berhasil dibuat!")

    # Jalankan aplikasi Flask
    app.run(debug=True)