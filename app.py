from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Notification, Admin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

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
        # Lanjutkan proses registrasi
        name = request.form['name']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
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

        # Debugging
        print(f"Email input: {email}, Password input: {password}")

        # Periksa apakah user adalah admin
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            print(f"Admin found: {admin.email}, Password DB: {admin.password}")
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('dashboard_admin'))

        # Periksa apakah user adalah user biasa
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.email}, Password DB: {user.password}")
        if not user or user.password != password:
            flash('Email atau password salah.')
            return redirect(url_for('login'))
        session['user_id'] = user.id
        return redirect(url_for('dashboard_user', user_id=user.id))
    return render_template('login.html')

# Formulir Pendaftaran
@app.route('/form/<int:user_id>', methods=['GET', 'POST'])
def form(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.address = request.form['address']
        user.school = request.form['school']
        db.session.commit()
        flash('Formulir berhasil dikirim! Menunggu persetujuan admin.')
        return redirect(url_for('dashboard_user', user_id=user.id))
    return render_template('form.html', user=user)

# Dashboard User
@app.route('/dashboard_user/<int:user_id>', methods=['GET', 'POST'])
def dashboard_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        # Debugging
        print(f"Alamat: {request.form['address']}, Asal Sekolah: {request.form['school']}")

        # Simpan data ke database
        user.address = request.form['address']
        user.school = request.form['school']
        db.session.commit()
        flash('Data berhasil diperbarui.')
        return redirect(url_for('dashboard_user', user_id=user.id))
    return render_template('dashboard_user.html', user=user)

# Dashboard Admin
@app.route('/dashboard_admin', methods=['GET', 'POST'])
def dashboard_admin():
    if 'admin_id' not in session:
        print("Admin not logged in")
        flash('Anda harus login sebagai admin untuk mengakses halaman ini.')
        return redirect(url_for('login'))

    users = User.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Ambil ID user dari form
        action = request.form.get('action')  # Ambil aksi (approve/reject) dari form
        user = User.query.get(user_id)

        if not user:
            flash('User tidak ditemukan.')
            return redirect(url_for('dashboard_admin'))

        # Proses aksi
        if action == 'approve':
            user.status = 'Approved'
            flash(f'User {user.name} telah diterima.')
        elif action == 'reject':
            user.status = 'Rejected'
            flash(f'User {user.name} telah ditolak.')

        db.session.commit()  # Simpan perubahan ke database
        return redirect(url_for('dashboard_admin'))

    return render_template('dashboard_admin.html', users=users)

# Tambahkan notifikasi untuk user
def add_notification(user_id, message):
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