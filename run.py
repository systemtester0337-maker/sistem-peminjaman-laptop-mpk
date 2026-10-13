"""
Fail pelancar utama untuk Sistem Pengurusan Peminjaman Laptop.
Jalankan skrip ini dengan arahan:
    python run.py
"""

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("  Sistem Pengurusan Peminjaman Laptop MPK")
    print("  Pelayan sedang berjalan di http://127.0.0.1:5000")
    print("  Tekan CTRL+C untuk berhenti.")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
