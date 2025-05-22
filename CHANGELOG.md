# Changelog PPDB Universitas Sanjaya

Semua perubahan penting pada proyek ini akan didokumentasikan di sini.

## [Unreleased]
### Diperbaiki
- Upload ijazah dan kartu keluarga (KK) pada formulir pendaftaran user kini tersimpan di database dan folder uploads.
- Validasi file upload (hanya gambar: png, jpg, jpeg) untuk ijazah, KK, dan bukti pembayaran.
- Notifikasi flash untuk keberhasilan/gagal upload dokumen dan pembayaran.
- Validasi form pendaftaran (nama, alamat, sekolah, dll) agar tidak kosong.
- Progress tracker pada dashboard user menampilkan status pengisian data, upload dokumen, dan pembayaran.
- Konfirmasi dokumen (ijazah/KK) oleh admin di dashboard admin dan halaman detail user.
- Tampilan dashboard admin menampilkan status dokumen dan pembayaran user secara real-time.

### Ditambahkan
- Register dan login untuk user dan admin.
- Formulir pendaftaran user dengan upload dokumen (ijazah & KK).
- Dashboard user: progress pendaftaran, status dokumen, status pembayaran, dan notifikasi.
- Dashboard admin: daftar pendaftar, verifikasi dokumen, konfirmasi pembayaran, detail user, dan laporan statistik.
- Upload bukti pembayaran dan konfirmasi pembayaran oleh admin.
- Laporan statistik pendaftaran (admin_report) berdasarkan fakultas dan agama.
- Struktur folder: static (css, js, img, uploads), templates (HTML), migrations, models.py, app.py, README.md, CHANGELOG.md.

## [1.0.0] - 2025-05-22
### Rilis Awal
- Register akun baru (user & admin), login, logout.
- Formulir pendaftaran user.
- Upload dokumen ijazah & KK.
- Dashboard user: progress tracker, status dokumen, status pembayaran.
- Dashboard admin: manajemen pendaftar, verifikasi dokumen, konfirmasi pembayaran, laporan statistik.
- Halaman detail user untuk admin.
- Upload dan konfirmasi bukti pembayaran.
- Laporan statistik pendaftaran.


### Ditambahkan
- Struktur awal aplikasi PPDB berbasis Flask.
- Fitur register dan login user.
- Formulir pendaftaran sederhana.
- Dashboard user dan admin dasar.

### Diperbaiki
- Perbaikan validasi email dan password.
- Perbaikan tampilan form.
