"""
Skrip Sandaran (Backup) Data untuk Sistem Pengurusan Peminjaman Laptop MPK.
Kegunaan:
    python backup.py
Skrip ini akan mengeksport semua rekod peminjaman ke dalam format JSON dan CSV
dalam direktori 'backups/'.
"""

import os
import json
import csv
from datetime import datetime
import database

def create_backup():
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = os.path.join(backup_dir, f"backup_peminjaman_{timestamp}.json")
    csv_filename = os.path.join(backup_dir, f"backup_peminjaman_{timestamp}.csv")

    print("=" * 60)
    print("  MEMULAKAN PROSES SANDARAN DATA (BACKUP)")
    print("=" * 60)

    try:
        records = database.get_all_records()
        print(f"[INFO] Jumlah rekod untuk disandarkan: {len(records)}")

        # 1. Simpan fail JSON
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                "system": "Sistem Pengurusan Peminjaman Laptop MPK",
                "backup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_records": len(records),
                "records": records
            }, f, indent=2, ensure_ascii=False)
        print(f"[OK] Fail JSON berjaya disimpan: {json_filename}")

        # 2. Simpan fail CSV
        if records:
            keys = ['id', 'nama_laptop', 'nama_jabatan', 'tarikh_peminjaman', 'tujuan', 'created_at', 'updated_at']
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for r in records:
                    writer.writerow({k: r.get(k, '') for k in keys})
            print(f"[OK] Fail CSV berjaya disimpan: {csv_filename}")

        print("\n" + "=" * 60)
        print("  PROSES SANDARAN SELESAI DENGAN JAYANYA")
        print("=" * 60)
    except Exception as e:
        print(f"[RALAT] Gagal membuat sandaran data: {str(e)}")

if __name__ == '__main__':
    create_backup()
