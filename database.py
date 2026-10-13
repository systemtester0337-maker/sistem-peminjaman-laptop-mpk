import os
import sqlite3
import urllib.parse
from datetime import datetime

# Muat tetapan dari pembolehubah persekitaran (environment variables)
DATABASE_URL = os.environ.get('DATABASE_URL')
IS_POSTGRES = bool(DATABASE_URL and (DATABASE_URL.startswith('postgres://') or DATABASE_URL.startswith('postgresql://')))

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'peminjaman.db')

def get_db_connection():
    """Membuka sambungan ke pangkalan data (PostgreSQL untuk Cloud/Production atau SQLite untuk Tempatan)."""
    if IS_POSTGRES:
        import pg8000.dbapi
        import ssl
        parsed = urllib.parse.urlparse(DATABASE_URL)
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        conn = pg8000.dbapi.connect(
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            ssl_context=ssl_ctx
        )
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def _format_row(cursor, row):
    """Menukar baris kepada kamus (dictionary) dan memformat jenis datetime."""
    if row is None:
        return None
    if isinstance(row, sqlite3.Row):
        d = dict(row)
        for k, v in d.items():
            if hasattr(v, 'strftime'):
                d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        return d
    columns = [col[0] for col in cursor.description]
    res = {}
    for col, val in zip(columns, row):
        if hasattr(val, 'strftime'):
            res[col] = val.strftime("%Y-%m-%d %H:%M:%S")
        else:
            res[col] = val
    return res

def _execute_query(cursor, sql, params=None):
    """Menjalankan pertanyaan SQL dengan menyesuaikan pengganti parameter (? vs %s)."""
    params = params or []
    if IS_POSTGRES:
        pg_sql = sql.replace('?', '%s')
        cursor.execute(pg_sql, params)
    else:
        cursor.execute(sql, params)

def init_db():
    """Menyediakan skema pangkalan data secara automatik."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if IS_POSTGRES:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS peminjaman_laptop (
                id SERIAL PRIMARY KEY,
                nama_laptop VARCHAR(255) NOT NULL,
                nama_jabatan VARCHAR(255) NOT NULL,
                tarikh_peminjaman VARCHAR(50) NOT NULL,
                tujuan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_laptop ON peminjaman_laptop(nama_laptop);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jabatan ON peminjaman_laptop(nama_jabatan);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarikh ON peminjaman_laptop(tarikh_peminjaman);")
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM peminjaman_laptop")
        count = cursor.fetchone()[0]
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS peminjaman_laptop (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_laptop TEXT NOT NULL,
                nama_jabatan TEXT NOT NULL,
                tarikh_peminjaman TEXT NOT NULL,
                tujuan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_laptop ON peminjaman_laptop(nama_laptop);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jabatan ON peminjaman_laptop(nama_jabatan);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tarikh ON peminjaman_laptop(tarikh_peminjaman);")
        conn.commit()

        cursor.execute("SELECT COUNT(*) AS count FROM peminjaman_laptop")
        count = cursor.fetchone()['count']

    if count == 0:
        seed_sample_data(conn)

    conn.close()

def seed_sample_data(conn):
    """Menyemai data contoh permulaan berkaitan MPK."""
    sample_records = [
        (
            "Dell Latitude 5420",
            "Bahagian Teknologi Maklumat MPK",
            datetime.now().strftime("%Y-%m-%d"),
            "Penyelenggaraan pelayan dan konfigurasi rangkaian sistem MPK"
        ),
        (
            "Lenovo ThinkPad T14",
            "Jabatan Khidmat Pengurusan MPK",
            datetime.now().strftime("%Y-%m-%d"),
            "Sesi temuduga dan urusan pentadbiran kakitangan majlis"
        ),
        (
            "HP ProBook 450 G8",
            "Jabatan Kewangan MPK",
            datetime.now().strftime("%Y-%m-%d"),
            "Penyediaan laporan perakaunan dan kutipan cukai taksiran"
        ),
        (
            "Apple MacBook Air M2",
            "Unit Komunikasi Korporat MPK",
            datetime.now().strftime("%Y-%m-%d"),
            "Penyuntingan video liputan program komuniti dan hebahan rasmi MPK"
        ),
        (
            "Acer TravelMate P2",
            "Jabatan Penguatkuasaan & Keselamatan MPK",
            datetime.now().strftime("%Y-%m-%d"),
            "Operasi pemantauan luar dan penguatkuasaan lesen perbandaran"
        )
    ]
    cursor = conn.cursor()
    insert_sql = """
        INSERT INTO peminjaman_laptop (nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan)
        VALUES (?, ?, ?, ?)
    """
    for rec in sample_records:
        _execute_query(cursor, insert_sql, list(rec))
    conn.commit()

def get_all_records(search=None, date_filter=None):
    """Mendapatkan senarai rekod dengan sokongan carian dan tapisan tarikh."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM peminjaman_laptop WHERE 1=1"
    params = []

    if search:
        search_pattern = f"%{search.strip()}%"
        query += " AND (nama_laptop LIKE ? OR nama_jabatan LIKE ? OR tujuan LIKE ?)"
        params.extend([search_pattern, search_pattern, search_pattern])

    if date_filter:
        query += " AND tarikh_peminjaman = ?"
        params.append(date_filter.strip())

    query += " ORDER BY id DESC"

    _execute_query(cursor, query, params)
    rows = cursor.fetchall()
    records = [_format_row(cursor, r) for r in rows]
    conn.close()
    return records

def get_record_by_id(record_id):
    """Mendapatkan rekod tertentu mengikut ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    _execute_query(cursor, "SELECT * FROM peminjaman_laptop WHERE id = ?", [record_id])
    row = cursor.fetchone()
    record = _format_row(cursor, row)
    conn.close()
    return record

def create_record(nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan):
    """Menambah rekod peminjaman baharu."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if IS_POSTGRES:
        _execute_query(
            cursor,
            """
            INSERT INTO peminjaman_laptop (nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            RETURNING id
            """,
            [nama_laptop.strip(), nama_jabatan.strip(), tarikh_peminjaman.strip(), tujuan.strip(), now, now]
        )
        new_id = cursor.fetchone()[0]
    else:
        _execute_query(
            cursor,
            """
            INSERT INTO peminjaman_laptop (nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [nama_laptop.strip(), nama_jabatan.strip(), tarikh_peminjaman.strip(), tujuan.strip(), now, now]
        )
        new_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return get_record_by_id(new_id)

def update_record(record_id, nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan):
    """Mengemaskini maklumat rekod peminjaman sedia ada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _execute_query(
        cursor,
        """
        UPDATE peminjaman_laptop
        SET nama_laptop = ?, nama_jabatan = ?, tarikh_peminjaman = ?, tujuan = ?, updated_at = ?
        WHERE id = ?
        """,
        [nama_laptop.strip(), nama_jabatan.strip(), tarikh_peminjaman.strip(), tujuan.strip(), now, record_id]
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected > 0:
        return get_record_by_id(record_id)
    return None

def delete_record(record_id):
    """Memadamkan rekod peminjaman mengikut ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    _execute_query(cursor, "DELETE FROM peminjaman_laptop WHERE id = ?", [record_id])
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def get_dashboard_stats():
    """Mengira statistik papan pemuka."""
    conn = get_db_connection()
    cursor = conn.cursor()

    _execute_query(cursor, "SELECT COUNT(*) FROM peminjaman_laptop")
    total_records = cursor.fetchone()[0]

    _execute_query(cursor, "SELECT COUNT(DISTINCT nama_laptop) FROM peminjaman_laptop")
    total_laptops = cursor.fetchone()[0]

    _execute_query(cursor, "SELECT COUNT(DISTINCT nama_jabatan) FROM peminjaman_laptop")
    total_departments = cursor.fetchone()[0]

    current_month_prefix = datetime.now().strftime("%Y-%m")
    _execute_query(
        cursor,
        "SELECT COUNT(*) FROM peminjaman_laptop WHERE tarikh_peminjaman LIKE ?",
        [f"{current_month_prefix}%"]
    )
    monthly_records = cursor.fetchone()[0]

    _execute_query(cursor, "SELECT * FROM peminjaman_laptop ORDER BY id DESC LIMIT 5")
    recent_rows = cursor.fetchall()
    recent_activities = [_format_row(cursor, r) for r in recent_rows]

    _execute_query(cursor, """
        SELECT nama_jabatan, COUNT(*) as count 
        FROM peminjaman_laptop 
        GROUP BY nama_jabatan 
        ORDER BY count DESC 
        LIMIT 5
    """)
    summary_rows = cursor.fetchall()
    department_summary = [{'nama_jabatan': r[0], 'count': r[1]} for r in summary_rows]

    conn.close()
    return {
        "total_records": total_records,
        "total_laptops": total_laptops,
        "total_departments": total_departments,
        "monthly_records": monthly_records,
        "recent_activities": recent_activities,
        "department_summary": department_summary
    }
