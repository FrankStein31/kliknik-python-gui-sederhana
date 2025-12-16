/*
SQLyog Enterprise
MySQL - 8.0.30 : Database - bismillah
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`bismillah` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `bismillah`;

/*Table structure for table `admin` */

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('dokter','pasien') NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `admin` */

insert  into `admin`(`id_admin`,`username`,`password`,`role`) values 
(1,'dokter1','123','dokter'),
(2,'pasien1','123','pasien'),
(3,'admin','admin123','dokter');

/*Table structure for table `dokter` */

DROP TABLE IF EXISTS `dokter`;

CREATE TABLE `dokter` (
  `nip` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `no_tlp` varchar(15) DEFAULT NULL,
  `alamat` text,
  PRIMARY KEY (`nip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `dokter` */

insert  into `dokter`(`nip`,`nama`,`no_tlp`,`alamat`) values 
('DOK001','Dr. Ahmad Fauzi, Sp.PD','081234567890','Jl. Merdeka No. 123, Jakarta'),
('DOK002','Dr. Siti Nurhaliza, Sp.A','081234567891','Jl. Kebon Jeruk No. 45, Jakarta'),
('DOK003','Dr. Budi Santoso, Sp.OG','081234567892','Jl. Sudirman No. 78, Jakarta');

/*Table structure for table `pasien` */

DROP TABLE IF EXISTS `pasien`;

CREATE TABLE `pasien` (
  `nik` varchar(16) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `no_tlp` varchar(15) DEFAULT NULL,
  `alamat` text,
  PRIMARY KEY (`nik`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `pasien` */

insert  into `pasien`(`nik`,`nama`,`no_tlp`,`alamat`) values 
('1234567890123456','Budi Santoso','081234567899','Jl. Kebon Jeruk No. 45, Jakarta'),
('1234567890123457','Ani Wijaya','081234567898','Jl. Gatot Subroto No. 12, Jakarta'),
('1234567890123458','Citra Dewi','081234567897','Jl. Thamrin No. 99, Jakarta');

/*Table structure for table `pemeriksaan` */

DROP TABLE IF EXISTS `pemeriksaan`;

CREATE TABLE `pemeriksaan` (
  `id_pemeriksaan` int NOT NULL AUTO_INCREMENT,
  `nik` varchar(16) NOT NULL,
  `diagnosa` text,
  `resep` text,
  `total_biaya` decimal(10,2) DEFAULT NULL,
  `total_obat` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pemeriksaan`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `pemeriksaan` */

insert  into `pemeriksaan`(`id_pemeriksaan`,`nik`,`diagnosa`,`resep`,`total_biaya`,`total_obat`,`created_at`) values 
(1,'1234567890123456','ISPA (Infeksi Saluran Pernapasan Akut)','Paracetamol 3x1, Amoxicillin 3x500mg',150000.00,2,'2025-12-16 12:56:03'),
(2,'1234567890123457','Migrain','Ibuprofen 3x400mg, Vitamin B Complex 1x1',120000.00,2,'2025-12-16 12:56:03'),
(3,'1234567890123458','Influenza','Paracetamol 3x1, Vitamin C 2x1',100000.00,2,'2025-12-16 12:56:03');

/*Table structure for table `pendaftaran` */

DROP TABLE IF EXISTS `pendaftaran`;

CREATE TABLE `pendaftaran` (
  `nik` varchar(16) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `tgllhr` date DEFAULT NULL,
  `jk` varchar(10) DEFAULT NULL,
  `no_telp` varchar(15) DEFAULT NULL,
  `keluhan` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`nik`,`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `pendaftaran` */

insert  into `pendaftaran`(`nik`,`nama`,`tgllhr`,`jk`,`no_telp`,`keluhan`,`created_at`) values 
('1234567890123456','Budi Santoso','1990-05-15','Laki-laki','081234567899','Demam dan batuk sejak 3 hari','2025-12-16 12:56:03'),
('1234567890123457','Ani Wijaya','1995-08-22','Perempuan','081234567898','Sakit kepala dan mual','2025-12-16 12:56:03'),
('1234567890123458','Citra Dewi','1988-12-10','Perempuan','081234567897','Flu dan pilek','2025-12-16 12:56:03');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
