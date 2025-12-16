import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bismillah"
)

cursor = db.cursor()

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

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
        return {"status": False}
