-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 16, 2025 at 01:38 PM
-- Server version: 8.0.30
-- PHP Version: 8.3.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bismillah`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('dokter','pasien') COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'dokter1', '123', 'dokter', '2025-12-16 13:33:03'),
(2, 'dokter2', '123', 'dokter', '2025-12-16 13:33:03'),
(3, 'pasien1', '123', 'pasien', '2025-12-16 13:33:03'),
(4, 'pasien2', '123', 'pasien', '2025-12-16 13:33:03');

-- --------------------------------------------------------

--
-- Table structure for table `dokter`
--

CREATE TABLE `dokter` (
  `nip` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no_telp` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alamat` text COLLATE utf8mb4_unicode_ci,
  `spesialisasi` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `dokter`
--

INSERT INTO `dokter` (`nip`, `nama`, `no_telp`, `alamat`, `spesialisasi`, `username`, `created_at`) VALUES
('DOK001', 'Dr. Ahmad Fauzi, Sp.PD', '081234567890', 'Jl. Merdeka No. 123, Jakarta', 'Penyakit Dalam', 'dokter1', '2025-12-16 13:33:03'),
('DOK002', 'Dr. Siti Nurhaliza, Sp.A', '081234567891', 'Jl. Kebon Jeruk No. 45, Jakarta', 'Anak', 'dokter2', '2025-12-16 13:33:03');

-- --------------------------------------------------------

--
-- Table structure for table `pasien`
--

CREATE TABLE `pasien` (
  `nik` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no_telp` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alamat` text COLLATE utf8mb4_unicode_ci,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pasien`
--

INSERT INTO `pasien` (`nik`, `nama`, `no_telp`, `alamat`, `username`, `created_at`) VALUES
('1234567890123456', 'Budi Santoso', '081234567899', 'Jl. Kebon Jeruk No. 45, Jakarta', 'pasien1', '2025-12-16 13:33:28'),
('1234567890123457', 'Ani Wijaya', '081234567898', 'Jl. Gatot Subroto No. 12, Jakarta', 'pasien2', '2025-12-16 13:33:28');

-- --------------------------------------------------------

--
-- Table structure for table `pemeriksaan`
--

CREATE TABLE `pemeriksaan` (
  `id_pemeriksaan` int NOT NULL,
  `id_pendaftaran` int NOT NULL,
  `nik` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nip_dokter` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `diagnosa` text COLLATE utf8mb4_unicode_ci,
  `resep` text COLLATE utf8mb4_unicode_ci,
  `biaya_dokter` decimal(10,2) DEFAULT '0.00',
  `biaya_obat` decimal(10,2) DEFAULT '0.00',
  `total_biaya` decimal(10,2) GENERATED ALWAYS AS ((`biaya_dokter` + `biaya_obat`)) STORED,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `pemeriksaan`
--
DELIMITER $$
CREATE TRIGGER `after_pemeriksaan_insert` AFTER INSERT ON `pemeriksaan` FOR EACH ROW BEGIN
    UPDATE `pendaftaran` 
    SET `status` = 'selesai' 
    WHERE `id_pendaftaran` = NEW.id_pendaftaran;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `pendaftaran`
--

CREATE TABLE `pendaftaran` (
  `id_pendaftaran` int NOT NULL,
  `nik` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tgllhr` date DEFAULT NULL,
  `jk` enum('Laki-laki','Perempuan') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `no_telp` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `keluhan` text COLLATE utf8mb4_unicode_ci,
  `status` enum('menunggu','selesai','dibatalkan') COLLATE utf8mb4_unicode_ci DEFAULT 'menunggu',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pendaftaran`
--

INSERT INTO `pendaftaran` (`id_pendaftaran`, `nik`, `nama`, `tgllhr`, `jk`, `no_telp`, `keluhan`, `status`, `created_at`) VALUES
(3, '1234567890123456', 'Budi Santoso', '1990-05-15', 'Laki-laki', '081234567899', 'Demam dan batuk sejak 3 hari', 'menunggu', '2025-12-16 13:33:51'),
(4, '1234567890123457', 'Ani Wijaya', '1995-08-22', 'Perempuan', '081234567898', 'Sakit kepala dan mual', 'menunggu', '2025-12-16 13:33:51');

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_pemeriksaan_lengkap`
-- (See below for the actual view)
--
CREATE TABLE `v_pemeriksaan_lengkap` (
`biaya_dokter` decimal(10,2)
,`biaya_obat` decimal(10,2)
,`created_at` timestamp
,`diagnosa` text
,`id_pemeriksaan` int
,`id_pendaftaran` int
,`keluhan` text
,`nama_dokter` varchar(100)
,`nama_pasien` varchar(100)
,`nik` varchar(16)
,`nip_dokter` varchar(20)
,`resep` text
,`telp_pasien` varchar(15)
,`total_biaya` decimal(10,2)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_pendaftaran_lengkap`
-- (See below for the actual view)
--
CREATE TABLE `v_pendaftaran_lengkap` (
`created_at` timestamp
,`id_pendaftaran` int
,`jk` enum('Laki-laki','Perempuan')
,`keluhan` text
,`nama` varchar(100)
,`nik` varchar(16)
,`no_telp` varchar(15)
,`status` enum('menunggu','selesai','dibatalkan')
,`status_pemeriksaan` varchar(15)
,`tgllhr` date
);

-- --------------------------------------------------------

--
-- Structure for view `v_pemeriksaan_lengkap`
--
DROP TABLE IF EXISTS `v_pemeriksaan_lengkap`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_pemeriksaan_lengkap`  AS SELECT `pm`.`id_pemeriksaan` AS `id_pemeriksaan`, `pm`.`id_pendaftaran` AS `id_pendaftaran`, `pm`.`nik` AS `nik`, `ps`.`nama` AS `nama_pasien`, `ps`.`no_telp` AS `telp_pasien`, `pf`.`keluhan` AS `keluhan`, `pm`.`nip_dokter` AS `nip_dokter`, `d`.`nama` AS `nama_dokter`, `pm`.`diagnosa` AS `diagnosa`, `pm`.`resep` AS `resep`, `pm`.`biaya_dokter` AS `biaya_dokter`, `pm`.`biaya_obat` AS `biaya_obat`, `pm`.`total_biaya` AS `total_biaya`, `pm`.`created_at` AS `created_at` FROM (((`pemeriksaan` `pm` join `pasien` `ps` on((`pm`.`nik` = `ps`.`nik`))) join `pendaftaran` `pf` on((`pm`.`id_pendaftaran` = `pf`.`id_pendaftaran`))) left join `dokter` `d` on((`pm`.`nip_dokter` = `d`.`nip`))) ORDER BY `pm`.`created_at` AS `DESCdesc` ASC  ;

-- --------------------------------------------------------

--
-- Structure for view `v_pendaftaran_lengkap`
--
DROP TABLE IF EXISTS `v_pendaftaran_lengkap`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_pendaftaran_lengkap`  AS SELECT `p`.`id_pendaftaran` AS `id_pendaftaran`, `p`.`nik` AS `nik`, `p`.`nama` AS `nama`, `p`.`tgllhr` AS `tgllhr`, `p`.`jk` AS `jk`, `p`.`no_telp` AS `no_telp`, `p`.`keluhan` AS `keluhan`, `p`.`status` AS `status`, `p`.`created_at` AS `created_at`, (case when (`pm`.`id_pemeriksaan` is not null) then 'Sudah Diperiksa' else 'Belum Diperiksa' end) AS `status_pemeriksaan` FROM (`pendaftaran` `p` left join `pemeriksaan` `pm` on((`p`.`id_pendaftaran` = `pm`.`id_pendaftaran`))) ORDER BY `p`.`created_at` AS `DESCdesc` ASC  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `idx_username` (`username`),
  ADD KEY `idx_role` (`role`);

--
-- Indexes for table `dokter`
--
ALTER TABLE `dokter`
  ADD PRIMARY KEY (`nip`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `idx_username` (`username`);

--
-- Indexes for table `pasien`
--
ALTER TABLE `pasien`
  ADD PRIMARY KEY (`nik`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `idx_username` (`username`);

--
-- Indexes for table `pemeriksaan`
--
ALTER TABLE `pemeriksaan`
  ADD PRIMARY KEY (`id_pemeriksaan`),
  ADD KEY `nip_dokter` (`nip_dokter`),
  ADD KEY `idx_pendaftaran` (`id_pendaftaran`),
  ADD KEY `idx_nik` (`nik`);

--
-- Indexes for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD PRIMARY KEY (`id_pendaftaran`),
  ADD KEY `idx_nik` (`nik`),
  ADD KEY `idx_status` (`status`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `pemeriksaan`
--
ALTER TABLE `pemeriksaan`
  MODIFY `id_pemeriksaan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  MODIFY `id_pendaftaran` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dokter`
--
ALTER TABLE `dokter`
  ADD CONSTRAINT `dokter_ibfk_1` FOREIGN KEY (`username`) REFERENCES `admin` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pasien`
--
ALTER TABLE `pasien`
  ADD CONSTRAINT `pasien_ibfk_1` FOREIGN KEY (`username`) REFERENCES `admin` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pemeriksaan`
--
ALTER TABLE `pemeriksaan`
  ADD CONSTRAINT `pemeriksaan_ibfk_1` FOREIGN KEY (`id_pendaftaran`) REFERENCES `pendaftaran` (`id_pendaftaran`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pemeriksaan_ibfk_2` FOREIGN KEY (`nik`) REFERENCES `pasien` (`nik`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pemeriksaan_ibfk_3` FOREIGN KEY (`nip_dokter`) REFERENCES `dokter` (`nip`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD CONSTRAINT `pendaftaran_ibfk_1` FOREIGN KEY (`nik`) REFERENCES `pasien` (`nik`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
