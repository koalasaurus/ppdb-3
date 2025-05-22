# PPDB Universitas Sanjaya

## Description
Aplikasi PPDB (Penerimaan Peserta Didik Baru) Universitas Sanjaya adalah sistem berbasis web yang dirancang untuk memudahkan proses pendaftaran mahasiswa baru. Aplikasi ini menyediakan fitur lengkap dari pendaftaran hingga pembayaran dan manajemen admin.

## Features
- **Authentication**
  - Register akun baru
  - Login user & admin
  - Logout

- **User Dashboard**
  - Progress tracker pendaftaran
  - Form pengisian data pribadi
  - Upload dokumen (Ijazah & KK)
  - Pembayaran dengan bukti transfer
  - Status verifikasi dokumen & pembayaran

- **Admin Dashboard**
  - Manajemen data pendaftar
  - Verifikasi dokumen
  - Konfirmasi pembayaran
  - Laporan statistik pendaftaran

## Project Structure
```plaintext
ppdb3/
├── static/
│   ├── css/
│   │   ├── admin.css
│   │   ├── detail.css
│   │   ├── form.css
│   │   ├── login.css
│   │   ├── register.css
│   │   ├── styles.css
│   │   └── user.css
│   ├── js/
│   │   └── scripts.js
│   └── img/
│       ├── Logo-Bank-BCA-1.png
│       └── mastercard.png
├── templates/
│   ├── admin_report.html
│   ├── dashboard_admin.html
│   ├── dashboard_user.html
│   ├── form.html
│   ├── index.html
│   ├── login.html
│   ├── payment.html
│   ├── register.html
│   └── user_detail.html
├── app.py
├── models.py
└── README.md
```

## Tech Stack
- **Backend**: Python Flask
- **Database**: SQLite dengan SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Bootstrap Icons

## Installation & Setup

1. **Clone Repository**
```bash
git clone [repository-url]
cd ppdb3
```

2. **Install Dependencies**
```bash
pip install flask flask-sqlalchemy flask-migrate flask-login werkzeug
```

3. **Initialize Database**
```bash
flask db init
flask db migrate
flask db upgrade
```

4. **Run Application**
```bash
python app.py
```

5. **Default Admin Account**
- Email: admin@gmail.com
- Password: admin123

## Pages & Routes
- `/` - Homepage
- `/login` - Login page
- `/register` - Registration page
- `/dashboard_user/<user_id>` - User dashboard
- `/dashboard_admin` - Admin dashboard
- `/form/<user_id>` - Form pendaftaran
- `/payment/<user_id>` - Halaman pembayaran
- `/user_detail/<user_id>` - Detail pendaftar (admin only)
- `/admin_report` - Laporan statistik (admin only)

## Contributors
- Andika - Developer

## License
MIT License

# UI Screenshots

Berikut adalah beberapa tampilan antarmuka aplikasi PPDB Universitas Sanjaya:

| Homepage | Homepage | Homepage |
|----------|----------|----------|
| ![](static/img/Screenshot%20(46).png) | ![](static/img/Screenshot%20(47).png) | ![](static/img/Screenshot%20(48).png) |
| Homepage | Homepage | Homepage |
| ![](static/img/Screenshot%20(49).png) | ![](static/img/Screenshot%20(50).png) | ![](static/img/Screenshot%20(51).png) |

| Register | Login |
|----------|-------|
| ![](static/img/Screenshot%20(52).png) | ![](static/img/Screenshot%20(53).png) |

| Halaman Admin | Halaman Admin | Halaman Admin |
|---------------|---------------|---------------|
| ![](static/img/Screenshot%20(54).png) | ![](static/img/Screenshot%20(55).png) | ![](static/img/Screenshot%20(56).png) |

| Dashboard User | Dashboard User |
|----------------|----------------|
| ![](static/img/Screenshot%20(57).png) | ![](static/img/Screenshot%20(58).png) |

| Halaman Pembayaran |
|--------------------|
| ![](static/img/Screenshot%20(59).png) |

| Formulir Pendaftaran | Formulir Pendaftaran | Formulir Pendaftaran |
|----------------------|----------------------|----------------------|
| ![](static/img/Screenshot%20(60).png) | ![](static/img/Screenshot%20(61).png) | ![](static/img/Screenshot%20(62).png) |

| Detail User (Admin) |
|---------------------|
| ![](static/img/Screenshot%20(63).png) |

| Bukti Pembayaran (Admin) |
|--------------------------|
| ![](static/img/Screenshot%20(64).png) |

| View Dokumen Ijazah/KK (Admin) |
|-------------------------------|
| ![](static/img/Screenshot%20(65).png) |

> **Catatan:**
> Untuk menampilkan gambar di atas, pastikan semua file screenshot sudah berada di folder `static/img/` di dalam root project ini.