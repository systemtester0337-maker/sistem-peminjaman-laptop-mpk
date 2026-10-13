# Sistem Pengurusan Peminjaman Laptop MPK

Sistem berasaskan web yang lengkap, berfungsi sepenuhnya, moden, dan mesra pengguna untuk menguruskan rekod peminjaman laptop bagi **Majlis Perbandaran Kemaman (MPK)**.

Dibina menggunakan **Python (Flask)** dan **SQLite3** dengan antaramuka pengguna (UI) responsif sepenuhnya dalam **Bahasa Melayu**.

---

## 1. Ciri-ciri Utama (Implemented Features)

- **Papan Pemuka (Dashboard):**
  - Statistik masa nyata: Jumlah Rekod Peminjaman, Jumlah Laptop Dipinjam, Bilangan Jabatan Terlibat, dan Peminjaman Bulan Ini.
  - Senarai 5 aktiviti peminjaman terkini.
  - Graf visual kekerapan peminjaman mengikut jabatan.
  - Tindakan pantas untuk mendaftar peminjaman terus dari papan pemuka.

- **Tambah Rekod Peminjaman (Create):**
  - Borang modal pendaftaran yang intuitif dengan cadangan automatik (*datalist*) untuk model laptop dan jabatan.
  - Pemilih tarikh (*date picker*) interaktif dengan tarikh semasa ditetapkan secara automatik.
  - Pengesahan data input pada bahagian klien (*frontend*) dan pelayan (*backend*).

- **Lihat Rekod (Read):**
  - Jadual paparan tersusun yang memaparkan ID, Nama Laptop, Nama Jabatan, Tarikh Peminjaman, dan Tujuan.
  - Penunjuk jumlah rekod dan status aktif.
  - Paparan keadaan kosong (*empty state*) sekiranya tiada rekod dijumpai.

- **Kemaskini Rekod (Update):**
  - Borang modal kemaskini yang memuatkan maklumat rekod sedia ada secara automatik.
  - Mengemaskini rekod dalam pangkalan data berserta cap masa `updated_at`.

- **Padam Rekod (Delete):**
  - Dialog pengesahan padam (*modal confirmation*) sebelum pemadaman dilakukan untuk mengelakkan kehilangan data tidak sengaja.
  - Memaparkan ringkasan rekod yang bakal dipadam.

- **Carian dan Tapisan Pantas (Search & Filter):**
  - Carian kata kunci masa nyata mengikut nama laptop, nama jabatan, atau tujuan.
  - Penapisan rekod mengikut tarikh peminjaman (*date picker*).
  - Butang set semula (*Reset*) untuk mengosongkan carian dan penapis dengan satu klik.

- **Ketahanan Data (Data Persistence):**
  - Semua rekod disimpan secara kekal dalam fail pangkalan data SQLite (`peminjaman.db`). Data kekal tersimpan walaupun aplikasi dimulakan semula atau pelayar dimuat semula.

- **Reka Bentuk UI Responsif:**
  - Antaramuka moden dengan tema warna profesional.
  - Navigasi bar sisi (*sidebar*) yang boleh dilipat pada peranti mudah alih dan tablet.
  - Notifikasi terapung (*toast notifications*) untuk status kejayaan dan ralat.

---

## 2. Struktur Projek (Project Structure)

```text
Sistem Pengurusan Peminjaman Laptop/
│
├── app.py                  # Pelayan aplikasi Flask & API RESTful (CRUD)
├── database.py             # Pengendali sambungan SQLite, operasi CRUD & statistik
├── schema.sql              # Skema DDL jadual peminjaman_laptop dan indeks
├── run.py                  # Skrip pelancar mudah untuk memulakan pelayan
├── requirements.txt        # Senarai kebergantungan Python (Flask)
├── test_app.py             # Ujian unit & integrasi automatik
├── README.md               # Dokumentasi lengkap sistem
│
├── static/
│   ├── css/
│   │   └── style.css       # Helaian gaya CSS moden dan reka bentuk responsif
│   └── js/
│       └── app.js          # Logik aplikasi frontend (fetch API, modal, carian, toast)
│
└── templates/
    └── index.html          # Templat utama HTML5 (Bahasa Melayu, susun atur responsif)
```

---

## 3. Skema Pangkalan Data (Database Schema)

Jadual utama: `peminjaman_laptop`

| Nama Lajur | Jenis Data | Penerangan |
| :--- | :--- | :--- |
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | ID unik dijana secara automatik |
| `nama_laptop` | `TEXT NOT NULL` | Nama atau model laptop yang dipinjam |
| `nama_jabatan` | `TEXT NOT NULL` | Nama jabatan / unit peminjam |
| `tarikh_peminjaman`| `TEXT NOT NULL` | Tarikh peminjaman (format `YYYY-MM-DD`) |
| `tujuan` | `TEXT NOT NULL` | Tujuan atau sebab peminjaman |
| `created_at` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Cap masa rekod dicipta |
| `updated_at` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Cap masa rekod terakhir dikemaskini |

### Skrip SQL (`schema.sql`):
```sql
CREATE TABLE IF NOT EXISTS peminjaman_laptop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_laptop TEXT NOT NULL,
    nama_jabatan TEXT NOT NULL,
    tarikh_peminjaman TEXT NOT NULL,
    tujuan TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_laptop ON peminjaman_laptop(nama_laptop);
CREATE INDEX IF NOT EXISTS idx_jabatan ON peminjaman_laptop(nama_jabatan);
CREATE INDEX IF NOT EXISTS idx_tarikh ON peminjaman_laptop(tarikh_peminjaman);
```

---

## 4. Keperluan Sistem & Pemasangan

### Keperluan:
- **Python 3.8** atau lebih baharu (Diuji pada Python 3.14).
- Pakej **Flask**.

### Langkah-langkah Pemasangan:

1. **Buka Terminal / PowerShell** di dalam direktori projek:
   ```powershell
   cd "c:\Users\Dell\Downloads\Sistem Pengurusan Peminjaman Laptop"
   ```

2. **Pasang Kebergantungan (Dependencies):**
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi:**
   Anda boleh menjalankan pelayan melalui salah satu arahan berikut:
   ```powershell
   python run.py
   ```
   *atau*
   ```powershell
   python app.py
   ```

4. **Buka Aplikasi di Pelayar Web:**
   Buka pelayar web kegemaran anda (Chrome, Edge, Firefox) dan layari:
   ```
   http://127.0.0.1:5000
   ```

---

## 5. Menjalankan Ujian Automatik (Testing)

Projek ini dilengkapi dengan set ujian automatik yang merangkumi semua operasi CRUD, tapisan, dan pengesahan borang.

Jalankan arahan berikut:
```powershell
python test_app.py
```

Output yang berjaya:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.444s

OK

[OK] Ujian Papan Pemuka Berjaya:  5 rekod dikesan.
[OK] Ujian Dapatkan Rekod Berjaya: Jumlah rekod = 5
[OK] Ujian Tambah Rekod Berjaya: ID #6
[OK] Ujian Pengesahan Borang Berjaya: Mesej ralat dikembalikan dengan betul.
[OK] Ujian Kemaskini Rekod Berjaya untuk ID #6
[OK] Ujian Carian dan Tapisan Tarikh Berjaya.
[OK] Ujian Padam Rekod Berjaya untuk ID #6
```

---

## 6. Titik Akhir API RESTful (API Endpoints)

| Kaedah | Endpoint | Penerangan |
| :--- | :--- | :--- |
| `GET` | `/` | Memaparkan antaramuka web utama |
| `GET` | `/api/dashboard/stats` | Mendapatkan statistik ringkasan dan aktiviti terkini |
| `GET` | `/api/records` | Senarai semua rekod (menyokong parameter `?search=` dan `?date=`) |
| `GET` | `/api/records/<id>` | Mendapatkan butiran satu rekod tertentu |
| `GET` | `/health` | Pemeriksaan kesihatan aplikasi bagi platform Cloud hosting |
| `POST` | `/api/records` | Mendaftar permohonan peminjaman baharu |
| `PUT` | `/api/records/<id>` | Mengemaskini maklumat rekod sedia ada |
| `DELETE`| `/api/records/<id>` | Memadamkan rekod peminjaman |

---

## 7. Penempatan Cloud (Production Deployment)

Sistem ini telah dilengkapi dengan konfigurasi pengeluaran sedia ada:
- **Pelayan WSGI Pengeluaran:** `gunicorn` (ditetapkan dalam `Procfile`)
- **Sokongan Pangkalan Data Dual-Engine:** SQLite (tempatan) dan Cloud PostgreSQL (pengeluaran kekal)
- **Konfigurasi Cloud:** `render.yaml`, `runtime.txt`, `.env.example`

### Langkah Penempatan ke Render.com (Percuma & Kekal):
1. Muat naik kod projek ke akaun **GitHub**.
2. Daftar akaun percuma di [Render.com](https://render.com).
3. Sambungkan akaun GitHub anda dan pilih repositori projek ini.
4. Render akan membaca fail `render.yaml` dan `Procfile` secara automatik.
5. Sediakan pangkalan data PostgreSQL percuma (contohnya di [Neon.tech](https://neon.tech) atau Render PostgreSQL) dan masukkan URL ke dalam pembolehubah persekitaran `DATABASE_URL`.
6. Klik **Deploy** — aplikasi akan menerima URL awam HTTPS secara automatik (contoh: `https://sistem-peminjaman-laptop-mpk.onrender.com`).

---

## 8. Penyelenggaraan, Migrasi & Sandaran Data (Backup)

- **Menjalankan Migrasi Data:**
  ```powershell
  python migrate.py
  ```
  Membina jadual secara automatik dan memindahkan rekod tempatan ke pangkalan data cloud.

- **Membuat Salinan Sandaran (Backup):**
  ```powershell
  python backup.py
  ```
  Mengeksport semua rekod secara automatik ke dalam folder `backups/` dalam format **JSON** dan **CSV** berserta cap masa.

