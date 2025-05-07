# PPDB Application

## Author
Andika

## Description
Aplikasi PPDB (Penerimaan Peserta Didik Baru) adalah aplikasi berbasis web yang dirancang untuk mempermudah proses pendaftaran siswa baru. Aplikasi ini memiliki fitur seperti registrasi, login, pengisian formulir pendaftaran, dashboard user untuk melihat status pendaftaran, dan dashboard admin untuk mengelola data pendaftaran.

## Features
- **Homepage**: Menampilkan informasi cara pendaftaran.
- **Register & Login**: User dapat mendaftar dan login untuk mengakses dashboard.
- **Formulir Pendaftaran**: User dapat mengisi formulir pendaftaran.
- **Dashboard User**: Menampilkan profil user dan status pendaftaran.
- **Dashboard Admin**: Admin dapat melihat data pendaftaran, menyetujui, atau menolak pendaftaran.
- **Notifikasi**: Notifikasi untuk admin jika ada formulir baru, dan untuk user jika pendaftaran diterima atau ditolak.

## Project Structure
```plaintext
ppdb-app/
├── app.py                  # File utama aplikasi Flask
├── templates/              # Folder untuk file HTML
│   ├── index.html          # Homepage
│   ├── register.html       # Halaman register
│   ├── login.html          # Halaman login
│   ├── form.html           # Formulir pendaftaran
│   ├── dashboard_user.html # Dashboard user
│   └── dashboard_admin.html# Dashboard admin
├── static/                 # Folder untuk file CSS, JS, dan gambar
│   ├── css/
│   │   └── styles.css      # File CSS
│   └── js/
│       └── scripts.js      # File JavaScript
├── db.sqlite3              # Database SQLite
└── README.md               # Dokumentasi proyek
```