# Healthy Diet Planner - Python Flask & SQLite Edition

Ini adalah rancangan lengkap website **Healthy Diet Planner** menggunakan framework **Python Flask** dan database **SQLite** sesuai dengan struktur direktori yang Anda minta.

## Struktur Direktori

```text
healthy_diet_planner/
│
├── app.py                  # Server utama Flask & Pengisi Database Otomatis
├── templates/              # File Frontend HTML Murni
│   ├── index.html          # Halaman Beranda (Home)
│   ├── menu.html           # Halaman Menu Diet & Minuman Sehat
│   ├── olahraga.html       # Halaman Rekomendasi Olahraga Kebugaran
│   ├── bmi.html            # Halaman Kalkulator BMI & Jadwal Diet Harian
│   └── tentang.html        # Halaman Tentang Platform
│
├── database.db             # Database SQLite (Akan terbuat otomatis saat app.py dijalankan)
└── README.md               # Dokumentasi panduan ini
```

---

## Cara Menjalankan di Komputer Lokal

### 1. Prasyarat (Prerequisites)
Pastikan Anda sudah menginstal **Python 3** di komputer Anda. Anda bisa mengunduhnya di [python.org](https://www.python.org/).

### 2. Instalasi Flask
Buka terminal (Command Prompt / Powershell di Windows, atau Terminal di macOS/Linux), arahkan ke folder ini, lalu instal Flask dengan perintah berikut:

```bash
pip install Flask
```

### 3. Jalankan Aplikasi
Jalankan file `app.py` menggunakan Python:

```bash
python app.py
```

Setelah dijalankan, Anda akan melihat pesan seperti ini di terminal Anda:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.5.1:5000
```

### 4. Buka di Browser
Buka browser favorit Anda (Google Chrome, Mozilla Firefox, Microsoft Edge, dll.), lalu ketik alamat berikut di URL bar:

**[http://127.0.0.1:5000](http://127.0.0.1:5000)** atau **[http://localhost:5000](http://localhost:5000)**

---

## Detail Fitur yang Diimplementasikan

1. **Auto-Database Initializer**: Saat `app.py` dijalankan pertama kali, program akan secara otomatis membuat file `database.db` menggunakan SQLite dan menyuntikkan (seeding) **25 menu diet**, **10 minuman sehat**, dan **15 aktivitas olahraga** lengkap dengan estimasi kalori dan nutrisi masing-masing.
2. **Kalkulator BMI Terintegrasi**: Pengguna memasukkan berat badan (kg) dan tinggi badan (cm). Program akan mengkalkulasi skor BMI, menentukan klasifikasi tubuh (Kurus, Normal, Overweight, Obesitas), dan menyajikan rencana diet strategis yang sesuai.
3. **Jadwal Diet Harian**: Jadwal sirkadian pola makan harian (Sarapan 07.00, Snack 10.00, Makan Siang 12.30, Snack 15.30, Makan Malam 18.30, serta pengingat Minum Air).
4. **Desain Elegan Berbasis Palette Resmi**:
   * `#DCD3E3` (Aksen Sekunder)
   * `#6862BC` (Warna Tombol & Heading)
   * `#F9F6F0` (Warna Latar Utama)
   * `#FBFAF4` (Warna Kartu Menu)
   * `#1E5875` (Warna Teks & Navigasi)
   * Fonts: Pairings Google Fonts `Great Vibes` (Representasi Brittany Font) untuk judul/heading kaligrafi, dan `Lora`/`Times New Roman` untuk isi teks yang anggun.
