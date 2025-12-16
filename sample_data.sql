-- ================================================
-- SAMPLE DATA UNTUK TESTING SISTEM KLINIK
-- ================================================

-- 1. BERSIHKAN DATA LAMA (OPTIONAL)
-- DELETE FROM pemeriksaan;
-- DELETE FROM pendaftaran;
-- DELETE FROM pasien;
-- DELETE FROM dokter;
-- DELETE FROM admin;

-- ================================================
-- 2. DATA ADMIN (LOGIN)
-- ================================================

-- Admin Dokter
INSERT INTO admin (username, password, role) VALUES
('dokter1', '123', 'dokter'),
('dr_ahmad', 'ahmad123', 'dokter');

-- Admin Pasien  
INSERT INTO admin (username, password, role) VALUES
('pasien1', '123', 'pasien'),
('pasien_123456', '123', 'pasien');  -- Pasien dengan NIK terakhir 123456

-- ================================================
-- 3. DATA DOKTER
-- ================================================

INSERT INTO dokter (nip, nama, no_tlp, alamat) VALUES
('DOK001', 'Dr. Ahmad Fauzi, Sp.PD', '081234567890', 'Jl. Merdeka No. 123, Jakarta'),
('DOK002', 'Dr. Siti Nurhaliza, Sp.A', '081234567891', 'Jl. Sudirman No. 45, Jakarta'),
('DOK003', 'Dr. Budi Santoso, Sp.OG', '081234567892', 'Jl. Gatot Subroto No. 78, Bandung');

-- ================================================
-- 4. DATA PASIEN
-- ================================================

INSERT INTO pasien (nik, nama, no_tlp, alamat) VALUES
('1234567890123456', 'Budi Santoso', '081234567899', 'Jl. Kebon Jeruk No. 45, Jakarta Barat'),
('3201012345670001', 'Siti Rahayu', '082345678901', 'Jl. Cibadak No. 12, Bandung'),
('3273011234567002', 'Andi Wijaya', '083456789012', 'Jl. Dago No. 88, Bandung'),
('3175012345670003', 'Dewi Lestari', '084567890123', 'Jl. Tebet Raya No. 67, Jakarta Selatan');

-- ================================================
-- 5. DATA PENDAFTARAN
-- ================================================

INSERT INTO pendaftaran (nik, nama, tgllhr, jk, no_telp, keluhan) VALUES
('1234567890123456', 'Budi Santoso', '1990-05-15', 'Laki-laki', '081234567899', 'Demam tinggi sejak 3 hari, disertai batuk dan pilek'),
('3201012345670001', 'Siti Rahayu', '1985-08-22', 'Perempuan', '082345678901', 'Sakit kepala berkepanjangan dan mual'),
('3273011234567002', 'Andi Wijaya', '1992-12-10', 'Laki-laki', '083456789012', 'Nyeri dada dan sesak napas'),
('3175012345670003', 'Dewi Lestari', '1988-03-25', 'Perempuan', '084567890123', 'Sakit perut dan diare'),
('1234567890123456', 'Budi Santoso', '1990-05-15', 'Laki-laki', '081234567899', 'Kontrol kesehatan rutin');

-- ================================================
-- 6. DATA PEMERIKSAAN
-- ================================================

INSERT INTO pemeriksaan (nik, diagnosa, resep, total_biaya, total_obat) VALUES
('1234567890123456', 'Influenza (Flu)', 'Paracetamol 500mg 3x1, Amoxicillin 500mg 3x1, Vitamin C 500mg 1x1', 150000, 3),
('3201012345670001', 'Migrain', 'Ibuprofen 400mg 2x1, Antasida 3x1', 100000, 2),
('3273011234567002', 'Bronkitis Akut', 'Ambroxol 30mg 3x1, Salbutamol inhaler', 200000, 2),
('3175012345670003', 'Gastroenteritis', 'Oralit, Zinc 20mg 1x1, Probiotik 2x1', 120000, 3);

-- ================================================
-- 7. VERIFIKASI DATA
-- ================================================

-- Cek total data
SELECT 'Admin' as tabel, COUNT(*) as jumlah FROM admin
UNION ALL
SELECT 'Dokter', COUNT(*) FROM dokter
UNION ALL
SELECT 'Pasien', COUNT(*) FROM pasien
UNION ALL
SELECT 'Pendaftaran', COUNT(*) FROM pendaftaran
UNION ALL
SELECT 'Pemeriksaan', COUNT(*) FROM pemeriksaan;

-- ================================================
-- 8. QUERY BERGUNA UNTUK TESTING
-- ================================================

-- Lihat semua admin
SELECT * FROM admin;

-- Lihat semua pasien dengan username login
SELECT 
    p.*,
    CONCAT('pasien_', RIGHT(p.nik, 6)) as username_login
FROM pasien p;

-- Lihat pendaftaran lengkap dengan hasil periksa
SELECT 
    pd.nik,
    pd.nama,
    pd.tgllhr,
    pd.jk,
    pd.keluhan,
    pr.diagnosa,
    pr.resep,
    pr.total_biaya
FROM pendaftaran pd
LEFT JOIN pemeriksaan pr ON pd.nik = pr.nik
ORDER BY pd.nik DESC;

-- ================================================
-- CATATAN PENTING:
-- ================================================

-- 1. Username pasien otomatis: pasien_[6 digit terakhir NIK]
--    Contoh: NIK 1234567890123456 → username: pasien_123456
--
-- 2. Password default untuk pasien baru: 123
--    (dapat diubah oleh pasien di menu profil)
--
-- 3. Untuk testing login:
--    Dokter: username=dokter1, password=123
--    Pasien: username=pasien_123456, password=123
--
-- 4. Relasi tabel:
--    admin.username → login sistem
--    admin.role → dokter/pasien
--    pendaftaran.nik → pemeriksaan.nik
--    pasien.nik → pendaftaran.nik

-- ================================================
-- SELESAI
-- ================================================
