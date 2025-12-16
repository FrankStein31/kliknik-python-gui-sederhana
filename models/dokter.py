"""
Dokter Class - Subclass dari Admin
Author: Klinik Management System
Date: 16 Desember 2025

Class ini menangani:
- Update profil dokter (TIDAK ADA DELETE!)
- Get data dokter
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Import Admin sebagai superclass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.admin import Admin

class Dokter(Admin):
    """
    Subclass dari Admin untuk data dokter
    Inherit authentication dari Admin
    TIDAK ADA METHOD DELETE! (Dokter tidak bisa hapus akun sendiri)
    """
    
    def __init__(self, nip=None, nama=None, no_telp=None, alamat=None, spesialisasi=None, username=None, password=None):
        """
        Inisialisasi Dokter
        
        Args:
            nip (str): NIP dokter
            nama (str): Nama lengkap dokter
            no_telp (str): Nomor telepon
            alamat (str): Alamat lengkap
            spesialisasi (str): Spesialisasi dokter
            username (str): Username untuk login
            password (str): Password untuk login
        """
        # Call parent constructor
        super().__init__(username, password, 'dokter')
        
        self.nip = nip
        self.nama = nama
        self.no_telp = no_telp
        self.alamat = alamat
        self.spesialisasi = spesialisasi
    
    def update_profil(self):
        """
        Update data profil dokter
        
        Returns:
            tuple: (bool, str) - (status, message)
        """
        try:
            conn = self.get_connection()
            if not conn:
                return False, "Gagal koneksi database"
            
            cursor = conn.cursor()
            query = """
                UPDATE dokter 
                SET nama = %s, no_telp = %s, alamat = %s, spesialisasi = %s 
                WHERE username = %s
            """
            cursor.execute(query, (self.nama, self.no_telp, self.alamat, self.spesialisasi, self.username))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                return True, "Profil berhasil diupdate"
            else:
                return False, "Data tidak ditemukan"
                
        except Error as e:
            print(f"Error update profil dokter: {e}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_by_username(username):
        """
        Get data dokter berdasarkan username
        
        Args:
            username (str): Username dokter
            
        Returns:
            dict: Data dokter atau None
        """
        try:
            dokter = Dokter()
            conn = dokter.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM dokter WHERE username = %s"
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get dokter: {e}")
            return None
    
    @staticmethod
    def get_by_nip(nip):
        """
        Get data dokter berdasarkan NIP
        
        Args:
            nip (str): NIP dokter
            
        Returns:
            dict: Data dokter atau None
        """
        try:
            dokter = Dokter()
            conn = dokter.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM dokter WHERE nip = %s"
            cursor.execute(query, (nip,))
            data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get dokter by NIP: {e}")
            return None
    
    @staticmethod
    def get_all():
        """
        Get semua data dokter
        
        Returns:
            list: List of dict data dokter
        """
        try:
            dokter = Dokter()
            conn = dokter.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM dokter ORDER BY nama"
            cursor.execute(query)
            data = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return data
            
        except Error as e:
            print(f"Error get all dokter: {e}")
            return []
