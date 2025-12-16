"""
Pemeriksaan Class
Author: Klinik Management System
Date: 16 Desember 2025

Class ini menangani:
- Dokter input hasil pemeriksaan
- Get riwayat pemeriksaan
- Update pemeriksaan
"""

import mysql.connector
from mysql.connector import Error

class Pemeriksaan:
    """
    Class untuk mengelola pemeriksaan pasien
    """
    
    def __init__(self, id_pendaftaran=None, nik=None, nip_dokter=None, diagnosa=None, resep=None, biaya_dokter=0, biaya_obat=0):
        """
        Inisialisasi Pemeriksaan
        
        Args:
            id_pendaftaran (int): ID pendaftaran
            nik (str): NIK pasien
            nip_dokter (str): NIP dokter yang memeriksa
            diagnosa (str): Hasil diagnosa
            resep (str): Resep obat
            biaya_dokter (float): Biaya konsultasi dokter
            biaya_obat (float): Biaya obat
        """
        self.id_pendaftaran = id_pendaftaran
        self.nik = nik
        self.nip_dokter = nip_dokter
        self.diagnosa = diagnosa
        self.resep = resep
        self.biaya_dokter = biaya_dokter
        self.biaya_obat = biaya_obat
        
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'bismillah'
        }
    
    def get_connection(self):
        """Membuat koneksi ke database"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            print(f"Error koneksi database: {e}")
            return None
    
    def simpan(self):
        """
        Simpan hasil pemeriksaan baru
        Status pendaftaran akan otomatis berubah jadi 'selesai' via trigger
        
        Returns:
            tuple: (bool, str, int) - (status, message, id_pemeriksaan)
        """
        try:
            # Validasi data wajib
            if not all([self.id_pendaftaran, self.nik, self.nip_dokter, self.diagnosa]):
                return False, "Data pemeriksaan tidak lengkap", None
            
            conn = self.get_connection()
            if not conn:
                return False, "Gagal koneksi database", None
            
            cursor = conn.cursor()
            query = """
                INSERT INTO pemeriksaan 
                (id_pendaftaran, nik, nip_dokter, diagnosa, resep, biaya_dokter, biaya_obat) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                self.id_pendaftaran, 
                self.nik, 
                self.nip_dokter, 
                self.diagnosa, 
                self.resep, 
                self.biaya_dokter, 
                self.biaya_obat
            ))
            conn.commit()
            
            id_pemeriksaan = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return True, "Pemeriksaan berhasil disimpan", id_pemeriksaan
            
        except Error as e:
            print(f"Error simpan pemeriksaan: {e}")
            return False, f"Error: {str(e)}", None
    
    def update(self, id_pemeriksaan):
        """
        Update data pemeriksaan
        
        Args:
            id_pemeriksaan (int): ID pemeriksaan yang akan diupdate
            
        Returns:
            tuple: (bool, str) - (status, message)
        """
        try:
            conn = self.get_connection()
            if not conn:
                return False, "Gagal koneksi database"
            
            cursor = conn.cursor()
            query = """
                UPDATE pemeriksaan 
                SET diagnosa = %s, resep = %s, biaya_dokter = %s, biaya_obat = %s 
                WHERE id_pemeriksaan = %s
            """
            cursor.execute(query, (
                self.diagnosa, 
                self.resep, 
                self.biaya_dokter, 
                self.biaya_obat, 
                id_pemeriksaan
            ))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Pemeriksaan berhasil diupdate"
            else:
                return False, "Data tidak ditemukan"
                
        except Error as e:
            print(f"Error update pemeriksaan: {e}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_all():
        """
        Get semua data pemeriksaan dengan join ke pendaftaran dan dokter
        
        Returns:
            list: List of dict pemeriksaan
        """
        try:
            pemeriksaan = Pemeriksaan()
            conn = pemeriksaan.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    pm.*,
                    pf.nama AS nama_pasien,
                    pf.keluhan,
                    d.nama AS nama_dokter
                FROM pemeriksaan pm
                JOIN pendaftaran pf ON pm.id_pendaftaran = pf.id_pendaftaran
                LEFT JOIN dokter d ON pm.nip_dokter = d.nip
                ORDER BY pm.created_at DESC
            """
            cursor.execute(query)
            data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get all pemeriksaan: {e}")
            return []
    
    @staticmethod
    def get_by_pendaftaran(id_pendaftaran):
        """
        Get pemeriksaan berdasarkan ID pendaftaran
        
        Args:
            id_pendaftaran (int): ID pendaftaran
            
        Returns:
            dict: Data pemeriksaan atau None
        """
        try:
            pemeriksaan = Pemeriksaan()
            conn = pemeriksaan.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    pm.*,
                    pf.nama AS nama_pasien,
                    pf.keluhan,
                    d.nama AS nama_dokter
                FROM pemeriksaan pm
                JOIN pendaftaran pf ON pm.id_pendaftaran = pf.id_pendaftaran
                LEFT JOIN dokter d ON pm.nip_dokter = d.nip
                WHERE pm.id_pendaftaran = %s
            """
            cursor.execute(query, (id_pendaftaran,))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pemeriksaan by pendaftaran: {e}")
            return None
    
    @staticmethod
    def get_by_nik(nik):
        """
        Get riwayat pemeriksaan berdasarkan NIK pasien
        
        Args:
            nik (str): NIK pasien
            
        Returns:
            list: List of dict pemeriksaan
        """
        try:
            pemeriksaan = Pemeriksaan()
            conn = pemeriksaan.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    pm.*,
                    pf.keluhan,
                    d.nama AS nama_dokter
                FROM pemeriksaan pm
                JOIN pendaftaran pf ON pm.id_pendaftaran = pf.id_pendaftaran
                LEFT JOIN dokter d ON pm.nip_dokter = d.nip
                WHERE pm.nik = %s
                ORDER BY pm.created_at DESC
            """
            cursor.execute(query, (nik,))
            data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pemeriksaan by NIK: {e}")
            return []
