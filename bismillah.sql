/*
Database Schema Baru - Sistem Klinik
Updated: 16 Desember 2025
*/

DROP DATABASE IF EXISTS `bismillah`;
CREATE DATABASE `bismillah` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `bismillah`;

-- =============================================
-- Table: admin (Superclass untuk User)
-- =============================================
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id_admin` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('dokter','pasien') NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_admin`),
  INDEX `idx_username` (`username`),
  INDEX `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data admin untuk dokter (sudah terdaftar)
INSERT INTO `admin` (`username`, `password`, `role`) VALUES
('dokter1', '123', 'dokter'),
('dokter2', '123', 'dokter');

-- =============================================
-- Table: pasien (Subclass dari Admin)
-- Linked via username ke admin table
-- =============================================
DROP TABLE IF EXISTS `pasien`;
CREATE TABLE `pasien` (
  `nik` VARCHAR(16) NOT NULL,
  `nama` VARCHAR(100) NOT NULL,
  `no_telp` VARCHAR(15) DEFAULT NULL,
  `alamat` TEXT,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`nik`),
  FOREIGN KEY (`username`) REFERENCES `admin`(`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample data pasien
INSERT INTO `pasien` (`nik`, `nama`, `no_telp`, `alamat`, `username`) VALUES
('1234567890123456', 'Budi Santoso', '081234567899', 'Jl. Kebon Jeruk No. 45, Jakarta', 'pasien1'),
('1234567890123457', 'Ani Wijaya', '081234567898', 'Jl. Gatot Subroto No. 12, Jakarta', 'pasien2');

-- Admin untuk pasien
INSERT INTO `admin` (`username`, `password`, `role`) VALUES
('pasien1', '123', 'pasien'),
('pasien2', '123', 'pasien');

-- =============================================
-- Table: dokter (Subclass dari Admin)
-- Linked via username ke admin table
-- =============================================
DROP TABLE IF EXISTS `dokter`;
CREATE TABLE `dokter` (
  `nip` VARCHAR(20) NOT NULL,
  `nama` VARCHAR(100) NOT NULL,
  `no_telp` VARCHAR(15) DEFAULT NULL,
  `alamat` TEXT,
  `spesialisasi` VARCHAR(100) DEFAULT NULL,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`nip`),
  FOREIGN KEY (`username`) REFERENCES `admin`(`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data dokter
INSERT INTO `dokter` (`nip`, `nama`, `no_telp`, `alamat`, `spesialisasi`, `username`) VALUES
('DOK001', 'Dr. Ahmad Fauzi, Sp.PD', '081234567890', 'Jl. Merdeka No. 123, Jakarta', 'Penyakit Dalam', 'dokter1'),
('DOK002', 'Dr. Siti Nurhaliza, Sp.A', '081234567891', 'Jl. Kebon Jeruk No. 45, Jakarta', 'Anak', 'dokter2');

-- =============================================
-- Table: pendaftaran
-- Pasien mendaftar untuk pemeriksaan
-- =============================================
DROP TABLE IF EXISTS `pendaftaran`;
CREATE TABLE `pendaftaran` (
  `id_pendaftaran` INT NOT NULL AUTO_INCREMENT,
  `nik` VARCHAR(16) NOT NULL,
  `nama` VARCHAR(100) NOT NULL,
  `tgllhr` DATE DEFAULT NULL,
  `jk` ENUM('Laki-laki','Perempuan') DEFAULT NULL,
  `no_telp` VARCHAR(15) DEFAULT NULL,
  `keluhan` TEXT,
  `status` ENUM('menunggu','selesai','dibatalkan') DEFAULT 'menunggu',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pendaftaran`),
  FOREIGN KEY (`nik`) REFERENCES `pasien`(`nik`) ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX `idx_nik` (`nik`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample pendaftaran
INSERT INTO `pendaftaran` (`nik`, `nama`, `tgllhr`, `jk`, `no_telp`, `keluhan`, `status`) VALUES
('1234567890123456', 'Budi Santoso', '1990-05-15', 'Laki-laki', '081234567899', 'Demam dan batuk sejak 3 hari', 'menunggu'),
('1234567890123457', 'Ani Wijaya', '1995-08-22', 'Perempuan', '081234567898', 'Sakit kepala dan mual', 'menunggu');

-- =============================================
-- Table: pemeriksaan
-- Dokter melakukan pemeriksaan dari pendaftaran
-- =============================================
DROP TABLE IF EXISTS `pemeriksaan`;
CREATE TABLE `pemeriksaan` (
  `id_pemeriksaan` INT NOT NULL AUTO_INCREMENT,
  `id_pendaftaran` INT NOT NULL,
  `nik` VARCHAR(16) NOT NULL,
  `nip_dokter` VARCHAR(20) DEFAULT NULL,
  `diagnosa` TEXT,
  `resep` TEXT,
  `biaya_dokter` DECIMAL(10,2) DEFAULT 0,
  `biaya_obat` DECIMAL(10,2) DEFAULT 0,
  `total_biaya` DECIMAL(10,2) GENERATED ALWAYS AS (`biaya_dokter` + `biaya_obat`) STORED,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pemeriksaan`),
  FOREIGN KEY (`id_pendaftaran`) REFERENCES `pendaftaran`(`id_pendaftaran`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`nik`) REFERENCES `pasien`(`nik`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`nip_dokter`) REFERENCES `dokter`(`nip`) ON DELETE SET NULL ON UPDATE CASCADE,
  INDEX `idx_pendaftaran` (`id_pendaftaran`),
  INDEX `idx_nik` (`nik`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample pemeriksaan
INSERT INTO `pemeriksaan` (`id_pendaftaran`, `nik`, `nip_dokter`, `diagnosa`, `resep`, `biaya_dokter`, `biaya_obat`) VALUES
(1, '1234567890123456', 'DOK001', 'ISPA (Infeksi Saluran Pernapasan Akut)', 'Paracetamol 3x1, Amoxicillin 3x500mg', 100000, 50000);

-- Update status pendaftaran yang sudah diperiksa
UPDATE `pendaftaran` SET `status` = 'selesai' WHERE `id_pendaftaran` = 1;

-- =============================================
-- Triggers untuk auto-update status pendaftaran
-- =============================================
DELIMITER $$

CREATE TRIGGER `after_pemeriksaan_insert` 
AFTER INSERT ON `pemeriksaan`
FOR EACH ROW
BEGIN
    UPDATE `pendaftaran` 
    SET `status` = 'selesai' 
    WHERE `id_pendaftaran` = NEW.id_pendaftaran;
END$$

DELIMITER ;

-- =============================================
-- Views untuk kemudahan query
-- =============================================

-- View: Daftar lengkap pendaftaran dengan status
CREATE OR REPLACE VIEW `v_pendaftaran_lengkap` AS
SELECT 
    p.id_pendaftaran,
    p.nik,
    p.nama,
    p.tgllhr,
    p.jk,
    p.no_telp,
    p.keluhan,
    p.status,
    p.created_at,
    CASE 
        WHEN pm.id_pemeriksaan IS NOT NULL THEN 'Sudah Diperiksa'
        ELSE 'Belum Diperiksa'
    END AS status_pemeriksaan
FROM pendaftaran p
LEFT JOIN pemeriksaan pm ON p.id_pendaftaran = pm.id_pendaftaran
ORDER BY p.created_at DESC;

-- View: Riwayat pemeriksaan lengkap
CREATE OR REPLACE VIEW `v_pemeriksaan_lengkap` AS
SELECT 
    pm.id_pemeriksaan,
    pm.id_pendaftaran,
    pm.nik,
    ps.nama AS nama_pasien,
    ps.no_telp AS telp_pasien,
    pf.keluhan,
    pm.nip_dokter,
    d.nama AS nama_dokter,
    pm.diagnosa,
    pm.resep,
    pm.biaya_dokter,
    pm.biaya_obat,
    pm.total_biaya,
    pm.created_at
FROM pemeriksaan pm
JOIN pasien ps ON pm.nik = ps.nik
JOIN pendaftaran pf ON pm.id_pendaftaran = pf.id_pendaftaran
LEFT JOIN dokter d ON pm.nip_dokter = d.nip
ORDER BY pm.created_at DESC;
