-- Skema Pangkalan Data: Sistem Pengurusan Peminjaman Laptop
-- Jadual: peminjaman_laptop

CREATE TABLE IF NOT EXISTS peminjaman_laptop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_laptop TEXT NOT NULL,
    nama_jabatan TEXT NOT NULL,
    tarikh_peminjaman TEXT NOT NULL,
    tujuan TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indeks untuk carian pantas mengikut nama laptop, jabatan, dan tarikh
CREATE INDEX IF NOT EXISTS idx_laptop ON peminjaman_laptop(nama_laptop);
CREATE INDEX IF NOT EXISTS idx_jabatan ON peminjaman_laptop(nama_jabatan);
CREATE INDEX IF NOT EXISTS idx_tarikh ON peminjaman_laptop(tarikh_peminjaman);
