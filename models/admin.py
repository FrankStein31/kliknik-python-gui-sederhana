"""
Admin Class - Superclass untuk Autentikasi
Author: Klinik Management System
Date: 16 Desember 2025

Class ini adalah superclass yang menangani:
- Login/Logout
- Create user (register)
- Delete user (untuk cascade delete pasien)
"""

import mysql.connector
from mysql.connector import Error

class Admin:
    """
    Superclass untuk sistem autentikasi
    Digunakan oleh Pasien dan Dokter sebagai subclass
    """
    
    def __init__(self, username=None, password=None, role=None):
        """
        Inisialisasi Admin
        
        Args:
            username (str): Username untuk login
            password (str): Password untuk login
            role (str): Role user ('pasien' atau 'dokter')
        """
        self.username = username
        self.password = password
        self.role = role
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
    
    @staticmethod
    def login(username, password):
        """
        Login user dan return data user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            dict: Data user jika berhasil, None jika gagal
        """
        try:
            admin = Admin()
            conn = admin.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return user
        except Error as e:
            print(f"Error login: {e}")
            return None
    
    @staticmethod
    def create_user(username, password, role):
        """
        Membuat user baru di tabel admin
        
        Args:
            username (str): Username baru
            password (str): Password
            role (str): Role ('pasien' atau 'dokter')
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            admin = Admin()
            conn = admin.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "INSERT INTO admin (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, role))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Error as e:
            print(f"Error create user: {e}")
            return False
    
    @staticmethod
    def delete_user(username):
        """
        Menghapus user dari tabel admin
        Akan CASCADE delete ke pasien/dokter
        
        Args:
            username (str): Username yang akan dihapus
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            admin = Admin()
            conn = admin.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "DELETE FROM admin WHERE username = %s"
            cursor.execute(query, (username,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Error as e:
            print(f"Error delete user: {e}")
            return False
    
    @staticmethod
    def check_username_exists(username):
        """
        Cek apakah username sudah digunakan
        
        Args:
            username (str): Username yang akan dicek
            
        Returns:
            bool: True jika sudah ada, False jika belum
        """
        try:
            admin = Admin()
            conn = admin.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM admin WHERE username = %s"
            cursor.execute(query, (username,))
            count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return count > 0
        except Error as e:
            print(f"Error check username: {e}")
            return False
    
    @staticmethod
    def update_password(username, new_password):
        """
        Update password user
        
        Args:
            username (str): Username
            new_password (str): Password baru
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            admin = Admin()
            conn = admin.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "UPDATE admin SET password = %s WHERE username = %s"
            cursor.execute(query, (new_password, username))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Error as e:
            print(f"Error update password: {e}")
            return False
