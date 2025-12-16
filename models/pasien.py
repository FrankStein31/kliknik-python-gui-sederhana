"""
Pasien Class - Subclass dari Admin
Author: Klinik Management System
Date: 16 Desember 2025

Class ini menangani:
- Register pasien baru (create admin + pasien)
- Update profil pasien
- Delete akun (CASCADE: admin, pasien, pendaftaran, pemeriksaan)
- Get data pasien
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Import Admin sebagai superclass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.admin import Admin

class Pasien(Admin):
    """
    Subclass dari Admin untuk data pasien
    Inherit authentication dari Admin
    """
    
    def __init__(self, nik=None, nama=None, no_telp=None, alamat=None, username=None, password=None):
        """
        Inisialisasi Pasien
        
        Args:
            nik (str): NIK pasien (16 digit)
            nama (str): Nama lengkap pasien
            no_telp (str): Nomor telepon
            alamat (str): Alamat lengkap
            username (str): Username untuk login
            password (str): Password untuk login
        """
        # Call parent constructor
        super().__init__(username, password, 'pasien')
        
        self.nik = nik
        self.nama = nama
        self.no_telp = no_telp
        self.alamat = alamat
    
    def register(self):
        """
        Register pasien baru
        1. Create user di tabel admin
        2. Insert data ke tabel pasien
        
        Returns:
            tuple: (bool, str) - (status, message)
        """
        try:
            # Validasi NIK
            if not self.nik or len(self.nik) != 16:
                return False, "NIK harus 16 digit"
            
            # Validasi data wajib
            if not all([self.nama, self.username, self.password]):
                return False, "Nama, Username, dan Password wajib diisi"
            
            # Cek username sudah ada atau belum
            if Admin.check_username_exists(self.username):
                return False, "Username sudah digunakan"
            
            conn = self.get_connection()
            if not conn:
                return False, "Gagal koneksi database"
            
            cursor = conn.cursor()
            
            # 1. Insert ke tabel admin
            query_admin = "INSERT INTO admin (username, password, role) VALUES (%s, %s, 'pasien')"
            cursor.execute(query_admin, (self.username, self.password))
            
            # 2. Insert ke tabel pasien
            query_pasien = """
                INSERT INTO pasien (nik, nama, no_telp, alamat, username) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_pasien, (self.nik, self.nama, self.no_telp, self.alamat, self.username))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True, "Registrasi berhasil"
            
        except Error as e:
            if "Duplicate entry" in str(e):
                if "nik" in str(e).lower():
                    return False, "NIK sudah terdaftar"
                else:
                    return False, "Username sudah digunakan"
            print(f"Error register pasien: {e}")
            return False, f"Error: {str(e)}"
    
    def update_profil(self):
        """
        Update data profil pasien
        
        Returns:
            tuple: (bool, str) - (status, message)
        """
        try:
            conn = self.get_connection()
            if not conn:
                return False, "Gagal koneksi database"
            
            cursor = conn.cursor()
            query = """
                UPDATE pasien 
                SET nama = %s, no_telp = %s, alamat = %s 
                WHERE username = %s
            """
            cursor.execute(query, (self.nama, self.no_telp, self.alamat, self.username))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Profil berhasil diupdate"
            else:
                return False, "Data tidak ditemukan"
                
        except Error as e:
            print(f"Error update profil: {e}")
            return False, f"Error: {str(e)}"
    
    def delete_akun(self):
        """
        Menghapus akun pasien
        CASCADE DELETE:
        - admin (ON DELETE CASCADE)
        - pasien (PRIMARY DELETE)
        - pendaftaran (ON DELETE CASCADE)
        - pemeriksaan (ON DELETE CASCADE)
        
        Returns:
            tuple: (bool, str) - (status, message)
        """
        try:
            # Delete dari admin akan CASCADE ke pasien, pendaftaran, pemeriksaan
            success = Admin.delete_user(self.username)
            
            if success:
                return True, "Akun berhasil dihapus"
            else:
                return False, "Gagal menghapus akun"
                
        except Error as e:
            print(f"Error delete akun: {e}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_by_username(username):
        """
        Get data pasien berdasarkan username
        
        Args:
            username (str): Username pasien
            
        Returns:
            dict: Data pasien atau None
        """
        try:
            pasien = Pasien()
            conn = pasien.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM pasien WHERE username = %s"
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pasien: {e}")
            return None
    
    @staticmethod
    def get_by_nik(nik):
        """
        Get data pasien berdasarkan NIK
        
        Args:
            nik (str): NIK pasien
            
        Returns:
            dict: Data pasien atau None
        """
        try:
            pasien = Pasien()
            conn = pasien.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM pasien WHERE nik = %s"
            cursor.execute(query, (nik,))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get pasien by NIK: {e}")
            return None
    
    @staticmethod
    def check_nik_exists(nik):
        """
        Cek apakah NIK sudah terdaftar
        
        Args:
            nik (str): NIK yang akan dicek
            
        Returns:
            bool: True jika sudah ada, False jika belum
        """
        try:
            pasien = Pasien()
            conn = pasien.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM pasien WHERE nik = %s"
            cursor.execute(query, (nik,))
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return count > 0
            
        except Error as e:
            print(f"Error check NIK: {e}")
            return False
