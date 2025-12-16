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


class Pasien:
    def __init__(self, nik=None, nama=None, no_tlp=None, alamat=None):
        self.nik = nik
        self.nama = nama
        self.no_tlp = no_tlp
        self.alamat = alamat

    # ==========================
    # INSERT PASIEN
    # ==========================
    def insert(self):
        sql = """
        INSERT INTO pasien (nik, nama, no_tlp, alamat)
        VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (self.nik, self.nama, self.no_tlp, self.alamat))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err

    # ==========================
    # AMBIL SEMUA PASIEN
    # ==========================
    @staticmethod
    def get_all():
        cursor.execute("SELECT * FROM pasien")
        return cursor.fetchall()

    # ==========================
    # AMBIL PASIEN BY NIK
    # ==========================
    @staticmethod
    def get_by_nik(nik):
        cursor.execute("SELECT * FROM pasien WHERE nik = %s", (nik,))
        return cursor.fetchone()

    # ==========================
    # UPDATE PASIEN
    # ==========================
    @staticmethod
    def update(nik, nama, no_tlp, alamat):
        sql = """
        UPDATE pasien
        SET nama=%s, no_tlp=%s, alamat=%s
        WHERE nik=%s
        """
        try:
            cursor.execute(sql, (nama, no_tlp, alamat, nik))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err

    # ==========================
    # DELETE PASIEN
    # ==========================
    @staticmethod
    def delete(nik):
        try:
            cursor.execute("DELETE FROM pasien WHERE nik=%s", (nik,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err
