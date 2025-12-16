"""
Base User Class - Parent class untuk Admin, Dokter, dan Pasien
Menyediakan struktur dasar untuk sistem user management
"""
import mysql.connector

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


class User:
    """
    Base class untuk semua user dalam sistem.
    Ini adalah superclass yang akan di-inherit oleh Admin, Dokter, dan Pasien.
    """
    
    def __init__(self, username=None, password=None, role=None):
        """
        Constructor base class User
        
        Args:
            username (str): Username untuk login
            password (str): Password untuk login
            role (str): Role user (admin/dokter/pasien)
        """
        self.username = username
        self.password = password
        self.role = role
    
    def login(self):
        """
        Method untuk login user.
        Akan di-override oleh child classes jika diperlukan.
        
        Returns:
            dict: Data user jika berhasil, error message jika gagal
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
    def get_by_username(username):
        """
        Ambil data user berdasarkan username
        
        Args:
            username (str): Username yang dicari
            
        Returns:
            tuple: Data user dari database
        """
        cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        return cursor.fetchone()
    
    @staticmethod
    def update_password(username, new_password):
        """
        Update password user
        
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
    
    def __str__(self):
        """String representation of User object"""
        return f"User(username={self.username}, role={self.role})"
    
    def __repr__(self):
        """Official string representation of User object"""
        return self.__str__()
