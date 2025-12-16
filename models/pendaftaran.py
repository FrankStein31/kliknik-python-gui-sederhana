"""
Pendaftaran Class
Author: Klinik Management System
Date: 16 Desember 2025

Class ini menangani:
- Pasien daftar untuk pemeriksaan
- Get daftar pendaftaran (untuk dokter)
- Get riwayat pendaftaran (untuk pasien)
"""

import mysql.connector
from mysql.connector import Error

class Pendaftaran:
    """
    Class untuk mengelola pendaftaran pemeriksaan
    """
    
    def __init__(self, nik=None, nama=None, tgllhr=None, jk=None, no_telp=None, keluhan=None):
        """
        Inisialisasi Pendaftaran
        
        Args:
            nik (str): NIK pasien
            nama (str): Nama pasien
            tgllhr (date): Tanggal lahir
            jk (str): Jenis kelamin ('Laki-laki' atau 'Perempuan')
            no_telp (str): Nomor telepon
            keluhan (str): Keluhan pasien
        """
        self.nik = nik
        self.nama = nama
        self.tgllhr = tgllhr
        self.jk = jk
        self.no_telp = no_telp
        self.keluhan = keluhan
        
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
    
    def daftar(self):
        """
        Insert pendaftaran baru
        
        Returns:
            tuple: (bool, str, int) - (status, message, id_pendaftaran)
        """
        try:
            # Validasi data wajib
            if not all([self.nik, self.nama, self.tgllhr, self.jk, self.keluhan]):
                return False, "Semua field wajib diisi", None
            
            conn = self.get_connection()
            if not conn:
                return False, "Gagal koneksi database", None
            
            cursor = conn.cursor()
            query = """
                INSERT INTO pendaftaran (nik, nama, tgllhr, jk, no_telp, keluhan, status) 
                VALUES (%s, %s, %s, %s, %s, %s, 'menunggu')
            """
            cursor.execute(query, (self.nik, self.nama, self.tgllhr, self.jk, self.no_telp, self.keluhan))
            conn.commit()
            
            id_pendaftaran = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return True, "Pendaftaran berhasil", id_pendaftaran
            
        except Error as e:
            print(f"Error daftar: {e}")
            return False, f"Error: {str(e)}", None
    
    @staticmethod
    def get_all_menunggu():
        """
        Get semua pendaftaran dengan status 'menunggu'
        Untuk ditampilkan di form pemeriksaan dokter
        
        Returns:
            list: List of dict pendaftaran
        """
        try:
            pendaftaran = Pendaftaran()
            conn = pendaftaran.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT * FROM pendaftaran 
                WHERE status = 'menunggu' 
                ORDER BY created_at ASC
            """
            cursor.execute(query)
            data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pendaftaran menunggu: {e}")
            return []
    
    @staticmethod
    def get_by_nik(nik):
        """
        Get riwayat pendaftaran berdasarkan NIK
        Untuk ditampilkan di dashboard pasien
        
        Args:
            nik (str): NIK pasien
            
        Returns:
            list: List of dict pendaftaran
        """
        try:
            pendaftaran = Pendaftaran()
            conn = pendaftaran.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT * FROM pendaftaran 
                WHERE nik = %s 
                ORDER BY created_at DESC
            """
            cursor.execute(query, (nik,))
            data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pendaftaran by NIK: {e}")
            return []
    
    @staticmethod
    def get_by_id(id_pendaftaran):
        """
        Get data pendaftaran berdasarkan ID
        
        Args:
            id_pendaftaran (int): ID pendaftaran
            
        Returns:
            dict: Data pendaftaran atau None
        """
        try:
            pendaftaran = Pendaftaran()
            conn = pendaftaran.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM pendaftaran WHERE id_pendaftaran = %s"
            cursor.execute(query, (id_pendaftaran,))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pendaftaran by ID: {e}")
            return None
    
    @staticmethod
    def update_status(id_pendaftaran, status):
        """
        Update status pendaftaran
        
        Args:
            id_pendaftaran (int): ID pendaftaran
            status (str): Status baru ('menunggu', 'selesai', 'dibatalkan')
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            pendaftaran = Pendaftaran()
            conn = pendaftaran.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "UPDATE pendaftaran SET status = %s WHERE id_pendaftaran = %s"
            cursor.execute(query, (status, id_pendaftaran))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
            
        except Error as e:
            print(f"Error update status: {e}")
            return False
    
    @staticmethod
    def hapus_pendaftaran(id_pendaftaran):
        """
        Hapus pendaftaran dari database (hard delete)
        Untuk dokter yang ingin menghapus pendaftaran
        
        Args:
            id_pendaftaran (int): ID pendaftaran yang akan dihapus
            
        Returns:
            tuple: (bool, str) - (status, message)
        """
        try:
            pendaftaran = Pendaftaran()
            conn = pendaftaran.get_connection()
            if not conn:
                return False, "Gagal koneksi database"
            
            cursor = conn.cursor()
            query = "DELETE FROM pendaftaran WHERE id_pendaftaran = %s"
            cursor.execute(query, (id_pendaftaran,))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Pendaftaran berhasil dihapus dari database"
            else:
                return False, "Pendaftaran tidak ditemukan"
                
        except Error as e:
            print(f"Error hapus pendaftaran: {e}")
            return False, f"Error: {str(e)}"
