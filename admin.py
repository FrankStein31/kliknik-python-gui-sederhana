"""
Admin Class - Subclass dari User untuk admin system
Mengelola autentikasi dan user management
"""
import mysql.connector
from user import User

# ==========================
# KONEKSI DATABASE
# ==========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bismillah"
)

cursor = db.cursor()


class Admin(User):
    """
    Admin class - subclass dari User.
    Bertanggung jawab untuk autentikasi dan manajemen user.
    
    Inheritance hierarchy:
    User (parent/superclass)
      └── Admin (child/subclass)
    """
    
    def __init__(self, username, password):
        """
        Constructor untuk Admin class
        
        Args:
            username (str): Username admin
            password (str): Password admin
        """
        # Call parent constructor
        super().__init__(username, password, role="admin")
    
    def login(self):
        """
        Override login method dari parent class User.
        Tetap menggunakan logic yang sama namun spesifik untuk admin.
        
        Returns:
            dict: Status login dan data user
        """
        sql = """
        SELECT id_admin, username, role
        FROM admin
        WHERE username=%s AND password=%s
        """
        cursor.execute(sql, (self.username, self.password))
        data = cursor.fetchone()

        if data:
            return {
                "status": True,
                "id": data[0],
                "username": data[1],
                "role": data[2]
            }
        return {"status": False, "message": "Username atau password salah"}
    
    @staticmethod
    def get_all():
        """
        Ambil semua data admin dari database
        
        Returns:
            list: List of admin records
        """
        cursor.execute("SELECT * FROM admin")
        return cursor.fetchall()
    
    @staticmethod
    def get_by_username(username):
        """
        Ambil data admin berdasarkan username.
        Inherited dari parent class User namun di-override untuk clarity.
        
        Args:
            username (str): Username yang dicari
            
        Returns:
            tuple: Data admin dari database
        """
        cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        return cursor.fetchone()
    
    @staticmethod
    def update_password(username, new_password):
        """
        Update password admin.
        Inherited dari parent class User.
        
        Args:
            username (str): Username yang akan diupdate
            new_password (str): Password baru
            
        Returns:
            bool/str: True jika berhasil, error message jika gagal
        """
        sql = "UPDATE admin SET password=%s WHERE username=%s"
        try:
            cursor.execute(sql, (new_password, username))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal update password: {err}"
    
    @staticmethod
    def create_user(username, password, role):
        """
        Buat user admin baru (untuk registrasi pasien/dokter).
        
        Args:
            username (str): Username baru
            password (str): Password baru
            role (str): Role user (admin/dokter/pasien)
            
        Returns:
            bool/str: True jika berhasil, error message jika gagal
        """
        sql = "INSERT INTO admin (username, password, role) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (username, password, role))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal membuat user: {err}"
    
    def __str__(self):
        """String representation of Admin object"""
        return f"Admin(username={self.username})"

