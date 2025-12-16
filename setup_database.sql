-- ============================================
-- SQL UNTUK MEMBUAT STRUKTUR DATABASE KLINIK
-- ============================================

-- Buat database (jika belum ada)
CREATE DATABASE IF NOT EXISTS bismillah;
USE bismillah;

-- ============================================
-- 1. TABLE ADMIN (untuk login)
-- ============================================
CREATE TABLE IF NOT EXISTS admin (
    id_admin INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('dokter', 'pasien') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 2. TABLE DOKTER (profil dokter)
-- ============================================
CREATE TABLE IF NOT EXISTS dokter (
    nip VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    no_tlp VARCHAR(15),
    alamat TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 3. TABLE PASIEN (profil pasien)
-- ============================================
CREATE TABLE IF NOT EXISTS pasien (
    nik VARCHAR(16) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    no_tlp VARCHAR(15),
    alamat TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 4. TABLE PENDAFTARAN (tanpa id_pendaftaran)
-- ============================================
CREATE TABLE IF NOT EXISTS pendaftaran (
    nik VARCHAR(16) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    tgllhr DATE,
    jk VARCHAR(10),
    no_telp VARCHAR(15),
    keluhan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nik, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 5. TABLE PEMERIKSAAN
-- ============================================
CREATE TABLE IF NOT EXISTS pemeriksaan (
    id_pemeriksaan INT PRIMARY KEY AUTO_INCREMENT,
    nik VARCHAR(16) NOT NULL,
    diagnosa TEXT,
    resep TEXT,
    total_biaya DECIMAL(10,2),
    total_obat INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Data Admin untuk login
INSERT INTO admin (username, password, role) VALUES
('dokter1', '123', 'dokter'),
('pasien1', '123', 'pasien'),
('admin', 'admin123', 'dokter')
ON DUPLICATE KEY UPDATE password=VALUES(password);

-- Data Dokter
INSERT INTO dokter (nip, nama, no_tlp, alamat) VALUES
('DOK001', 'Dr. Ahmad Fauzi, Sp.PD', '081234567890', 'Jl. Merdeka No. 123, Jakarta'),
('DOK002', 'Dr. Siti Nurhaliza, Sp.A', '081234567891', 'Jl. Kebon Jeruk No. 45, Jakarta'),
('DOK003', 'Dr. Budi Santoso, Sp.OG', '081234567892', 'Jl. Sudirman No. 78, Jakarta')
ON DUPLICATE KEY UPDATE nama=VALUES(nama), no_tlp=VALUES(no_tlp), alamat=VALUES(alamat);

-- Data Pasien
INSERT INTO pasien (nik, nama, no_tlp, alamat) VALUES
('1234567890123456', 'Budi Santoso', '081234567899', 'Jl. Kebon Jeruk No. 45, Jakarta'),
('1234567890123457', 'Ani Wijaya', '081234567898', 'Jl. Gatot Subroto No. 12, Jakarta'),
('1234567890123458', 'Citra Dewi', '081234567897', 'Jl. Thamrin No. 99, Jakarta')
ON DUPLICATE KEY UPDATE nama=VALUES(nama), no_tlp=VALUES(no_tlp), alamat=VALUES(alamat);

-- Data Pendaftaran (sample)
INSERT INTO pendaftaran (nik, nama, tgllhr, jk, no_telp, keluhan) VALUES
('1234567890123456', 'Budi Santoso', '1990-05-15', 'Laki-laki', '081234567899', 'Demam dan batuk sejak 3 hari'),
('1234567890123457', 'Ani Wijaya', '1995-08-22', 'Perempuan', '081234567898', 'Sakit kepala dan mual'),
('1234567890123458', 'Citra Dewi', '1988-12-10', 'Perempuan', '081234567897', 'Flu dan pilek')
ON DUPLICATE KEY UPDATE nama=VALUES(nama);

-- Data Pemeriksaan (sample)
INSERT INTO pemeriksaan (nik, diagnosa, resep, total_biaya, total_obat) VALUES
('1234567890123456', 'ISPA (Infeksi Saluran Pernapasan Akut)', 'Paracetamol 3x1, Amoxicillin 3x500mg', 150000, 2),
('1234567890123457', 'Migrain', 'Ibuprofen 3x400mg, Vitamin B Complex 1x1', 120000, 2),
('1234567890123458', 'Influenza', 'Paracetamol 3x1, Vitamin C 2x1', 100000, 2);

-- ============================================
-- VERIFIKASI DATA
-- ============================================
SELECT '=== DATA ADMIN ===' as info;
SELECT * FROM admin;

SELECT '=== DATA DOKTER ===' as info;
SELECT * FROM dokter;

SELECT '=== DATA PASIEN ===' as info;
SELECT * FROM pasien;

SELECT '=== DATA PENDAFTARAN ===' as info;
SELECT * FROM pendaftaran;

SELECT '=== DATA PEMERIKSAAN ===' as info;
SELECT * FROM pemeriksaan;
