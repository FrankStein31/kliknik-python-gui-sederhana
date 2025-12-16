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

    
    def __init__(self, username, password):

        # Call parent constructor
        super().__init__(username, password, role="admin")
    
    def login(self):

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

        cursor.execute("SELECT * FROM admin")
        return cursor.fetchall()
    
    @staticmethod
    def get_by_username(username):

        cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        return cursor.fetchone()
    
    @staticmethod
    def update_password(username, new_password):

        sql = "UPDATE admin SET password=%s WHERE username=%s"
        try:
            cursor.execute(sql, (new_password, username))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal update password: {err}"
    
    @staticmethod
    def create_user(username, password, role):

        sql = "INSERT INTO admin (username, password, role) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (username, password, role))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal membuat user: {err}"
    
    def __str__(self):
        return f"Admin(username={self.username})"

