"""
Skrip Migrasi Pangkalan Data untuk Sistem Pengurusan Peminjaman Laptop MPK.
Kegunaan:
    python migrate.py
Skrip ini akan:
1. Membina jadual peminjaman_laptop dan indeks dalam pangkalan data sasaran.
2. Sekiranya DATABASE_URL (PostgreSQL) digunakan dan rekod sedia ada ada dalam peminjaman.db (SQLite),
   rekod tersebut akan dipindahkan (migrated) secara automatik ke PostgreSQL.
"""

import os
import sqlite3
import database

def run_migration():
    print("=" * 60)
    print("  MEMULAKAN MIGRASI PANGKALAN DATA")
    print("=" * 60)

    if database.IS_POSTGRES:
        print("[INFO] Mod Pangkalan Data: Cloud PostgreSQL")
        print("[INFO] URL: Disambungkan melalui DATABASE_URL")
    else:
        print("[INFO] Mod Pangkalan Data: Tempatan SQLite (peminjaman.db)")

    # 1. Mulakan pembinaan skema
    print("\n[1/2] Membina jadual dan indeks...")
    database.init_db()
    print("[OK] Skema pangkalan data berjaya disahkan/dibina.")

    # 2. Pindahkan data tempatan ke PostgreSQL jika berkaitan
    if database.IS_POSTGRES and os.path.exists(database.DB_PATH):
        print("\n[2/2] Memeriksa data SQLite tempatan untuk dipindahkan ke PostgreSQL...")
        try:
            sqlite_conn = sqlite3.connect(database.DB_PATH)
            sqlite_conn.row_factory = sqlite3.Row
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute("SELECT * FROM peminjaman_laptop ORDER BY id ASC")
            local_records = sqlite_cursor.fetchall()
            sqlite_conn.close()

            if local_records:
                print(f"[INFO] Dijumpai {len(local_records)} rekod dalam fail SQLite tempatan.")
                pg_conn = database.get_db_connection()
                pg_cursor = pg_conn.cursor()
                
                # Semak jumlah rekod sedia ada dalam PostgreSQL
                pg_cursor.execute("SELECT COUNT(*) FROM peminjaman_laptop")
                current_pg_count = pg_cursor.fetchone()[0]

                if current_pg_count == 0:
                    print("[INFO] Memindahkan rekod ke PostgreSQL...")
                    for r in local_records:
                        database._execute_query(
                            pg_cursor,
                            """
                            INSERT INTO peminjaman_laptop (nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            [r['nama_laptop'], r['nama_jabatan'], r['tarikh_peminjaman'], r['tujuan'], r['created_at'], r['updated_at']]
                        )
                    pg_conn.commit()
                    print(f"[OK] Berjaya memindahkan {len(local_records)} rekod ke Cloud PostgreSQL!")
                else:
                    print(f"[INFO] Cloud PostgreSQL sudah mempunyai {current_pg_count} rekod. Tiada pemindahan diperlukan.")
                pg_conn.close()
        except Exception as e:
            print(f"[RALAT] Ralat semasa memindahkan data: {str(e)}")
    else:
        print("\n[2/2] Tiada fail pemindahan diperlukan.")

    print("\n" + "=" * 60)
    print("  MIGRASI SELESAI DENGAN JAYANYA")
    print("=" * 60)

if __name__ == '__main__':
    run_migration()
