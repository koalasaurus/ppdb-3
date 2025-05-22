# User Manual PPDB Universitas Sanjaya

Selamat datang di aplikasi PPDB (Penerimaan Peserta Didik Baru) Universitas Sanjaya! Panduan ini akan membantu Anda memahami cara menggunakan aplikasi ini, baik sebagai calon mahasiswa (user) maupun sebagai admin.

---

## 1. Instalasi & Persiapan

### a. Clone Repository
```bash
git clone [repository-url]
cd ppdb3
```

### b. Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-migrate flask-login werkzeug
```

### c. Inisialisasi Database
```bash
flask db init
flask db migrate
flask db upgrade
```

### d. Jalankan Aplikasi
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`.

---

## 2. Akun & Login

- **User**: Daftar melalui halaman Register (`/register`).
- **Admin**: Login menggunakan akun default:
  - Email: `admin@gmail.com`
  - Password: `admin123`

---

## 3. Fitur untuk User

### a. Register
- Buka `/register`.
- Isi data diri dan password.
- Setelah register, login ke aplikasi.

### b. Formulir Pendaftaran
- Setelah login, lengkapi formulir di `/form/<user_id>`.
- Isi data diri, alamat, sekolah, dll.
- Upload dokumen: **Ijazah** dan **Kartu Keluarga (KK)** (format: png, jpg, jpeg).
- Simpan formulir.

### c. Dashboard User
- Akses di `/dashboard_user/<user_id>`.
- Lihat status pendaftaran, progress tracker, status dokumen, dan pembayaran.
- Jika dokumen sudah diverifikasi admin, lanjut ke pembayaran.

### d. Pembayaran
- Buka `/payment/<user_id>`.
- Lihat info rekening, transfer biaya, dan upload bukti pembayaran.
- Tunggu konfirmasi admin.

### e. Notifikasi
- Notifikasi status pendaftaran, dokumen, dan pembayaran akan muncul di dashboard user.

---

## 4. Fitur untuk Admin

### a. Login
- Masuk ke `/login` dengan akun admin.

### b. Dashboard Admin
- Akses di `/dashboard_admin`.
- Lihat daftar pendaftar, status dokumen, dan pembayaran.
- Verifikasi dokumen (Ijazah & KK) dan konfirmasi pembayaran.
- Klik tombol detail untuk melihat data lengkap user di `/user_detail/<user_id>`.

### c. Laporan Statistik
- Buka `/admin_report` untuk melihat statistik pendaftaran berdasarkan fakultas dan agama.

---

## 5. Struktur Folder

```
ppdb3/
├── static/
│   ├── css/         # File CSS
│   ├── js/          # File JS
│   ├── img/         # Gambar
│   └── uploads/     # Upload dokumen user
├── templates/       # HTML templates
├── app.py           # Main Flask app
├── models.py        # Model database
├── migrations/      # Migrasi database
├── db.sqlite3       # Database SQLite
├── README.md        # Deskripsi proyek
├── CHANGELOG.md     # Log perubahan
└── user_manual.md   # (File ini)
```

---

## 6. Tips & Catatan
- **File upload** hanya menerima gambar (png, jpg, jpeg).
- Semua status pendaftaran, dokumen, dan pembayaran dapat dipantau di dashboard masing-masing.
- Jika ada kendala, cek notifikasi atau hubungi admin.

---

## 7. Kontak
Untuk pertanyaan lebih lanjut, hubungi admin Universitas Sanjaya.

---

Selamat menggunakan aplikasi PPDB Universitas Sanjaya!
