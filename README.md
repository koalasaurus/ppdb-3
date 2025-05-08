# PPDB Application

## Author
Andika

## Description
Aplikasi PPDB (Penerimaan Peserta Didik Baru) adalah aplikasi berbasis web yang dirancang untuk mempermudah proses pendaftaran siswa baru. Aplikasi ini memiliki fitur seperti registrasi, login, pengisian formulir pendaftaran, dashboard user untuk melihat status pendaftaran, dan dashboard admin untuk mengelola data pendaftaran.

## Features
- **Homepage**: Menampilkan informasi cara pendaftaran.
- **Register & Login**: User dapat mendaftar dan login untuk mengakses dashboard.
- **Formulir Pendaftaran**: User dapat mengisi formulir pendaftaran.
- **Dashboard User**: Menampilkan profil user, status pendaftaran, dan notifikasi.
- **Dashboard Admin**: Admin dapat melihat data pendaftaran, menyetujui, atau menolak pendaftaran.
- **Notifikasi**: 
  - Untuk admin jika ada formulir baru.
  - Untuk user jika pendaftaran diterima atau ditolak.

## Project Structure
```plaintext
ppdb-app/
├── app.py                  # File utama aplikasi Flask
├── models.py               # Model database untuk User, Admin, dan Notifikasi
├── templates/              # Folder untuk file HTML
│   ├── index.html          # Homepage
│   ├── register.html       # Halaman register
│   ├── login.html          # Halaman login
│   ├── form.html           # Formulir pendaftaran
│   ├── dashboard_user.html # Dashboard user
│   ├── dashboard_admin.html# Dashboard admin
│   └── user_detail.html    # Halaman detail user untuk admin
├── static/                 # Folder untuk file CSS, JS, dan gambar
│   ├── css/
│   │   ├── styles.css      # File CSS utama
│   │   ├── form.css        # File CSS untuk formulir
│   │   ├── admin.css       # File CSS untuk dashboard admin
│   │   └── detail.css      # File CSS untuk halaman detail user
│   └── js/
│       └── scripts.js      # File JavaScript
├── db.sqlite3              # Database SQLite
└── README.md               # Dokumentasi proyek
```

## How to Run
1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd ppdb-app
   ```

2. **Install Dependencies**:
   Pastikan Anda memiliki Python terinstal. Kemudian jalankan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Database**:
   Inisialisasi database dengan perintah berikut:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run Application**:
   Jalankan aplikasi dengan perintah:
   ```bash
   flask run
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:5000`.

5. **Access Application**:
   - **Homepage**: `http://127.0.0.1:5000/`
   - **Admin Dashboard**: `http://127.0.0.1:5000/dashboard_admin`
   - **User Dashboard**: `http://127.0.0.1:5000/dashboard_user/<user_id>`

## Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Werkzeug

## License
Proyek ini menggunakan lisensi **MIT**.