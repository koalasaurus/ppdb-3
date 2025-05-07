from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Admin, Notification  # Import db, User, dan Admin dari models.py
from flask_migrate import Migrate

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
        print(request.form)  # Debug: Periksa data yang diterima dari form
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
        user = User.query.filter_by(email=email).first()
        if not user or user.password != password:
            flash('Email atau password salah.')
            return redirect(url_for('login'))
        session['user_id'] = user.id
        if user.email == 'admin@example.com':  # Admin login
            return redirect(url_for('dashboard_admin'))
        return redirect(url_for('dashboard_user', user_id=user.id))
    return render_template('login.html')

# Formulir Pendaftaran
@app.route('/form/<int:user_id>', methods=['GET', 'POST'])
def form(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        flash('Formulir berhasil dikirim! Menunggu persetujuan admin.')
        return redirect(url_for('dashboard_user', user_id=user.id))
    return render_template('form.html', user=user)

# Dashboard User
@app.route('/dashboard_user/<int:user_id>', methods=['GET', 'POST'])
def dashboard_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.address = request.form['address']
        user.school = request.form['school']
        db.session.commit()
        flash('Formulir berhasil dikirim! Menunggu persetujuan admin.')
    return render_template('dashboard_user.html', user=user)

# Dashboard Admin
@app.route('/dashboard_admin', methods=['GET', 'POST'])
def dashboard_admin():
    users = User.query.all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']
        user = User.query.get(user_id)
        if action == 'approve':
            user.status = 'Approved'
            flash(f'User {user.name} telah diterima.')
        elif action == 'reject':
            user.status = 'Rejected'
            flash(f'User {user.name} telah ditolak.')
        db.session.commit()
    return render_template('dashboard_admin.html', users=users)

# Tambahkan admin secara manual (hanya untuk pertama kali)
@app.route('/create_admin')
def create_admin():
    admin = Admin(name="Super Admin", email="admin@example.com", password="admin123")
    db.session.add(admin)
    db.session.commit()
    return "Admin berhasil dibuat!"

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
    flash('Anda telah logout.')
    return redirect(url_for('index'))

@app.route('/debug')
def debug():
    users = User.query.all()
    return f"Users: {users}"

@app.route('/user_detail/<int:user_id>')
def user_detail(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan.')
        return redirect(url_for('dashboard_admin'))
    return render_template('user_detail.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Membuat tabel di database
    app.run(debug=True)