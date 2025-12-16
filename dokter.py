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


class Dokter:
    def __init__(self, nip=None, nama=None, no_tlp=None, alamat=None):
        self.nip = nip
        self.nama = nama
        self.no_tlp = no_tlp
        self.alamat = alamat

    # ==========================
    # INSERT DOKTER
    # ==========================
    def insert(self):
        sql = """
        INSERT INTO dokter (nip, nama, no_tlp, alamat)
        VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (self.nip, self.nama, self.no_tlp, self.alamat))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err

    # ==========================
    # AMBIL SEMUA DOKTER
    # ==========================
    @staticmethod
    def get_all():
        cursor.execute("SELECT * FROM dokter")
        return cursor.fetchall()

    # ==========================
    # AMBIL DOKTER BY NIP
    # ==========================
    @staticmethod
    def get_by_nip(nip):
        cursor.execute("SELECT * FROM dokter WHERE nip=%s", (nip,))
        return cursor.fetchone()

    # ==========================
    # UPDATE DOKTER
    # ==========================
    @staticmethod
    def update(nip, nama, no_tlp, alamat):
        sql = """
        UPDATE dokter
        SET nama=%s, no_tlp=%s, alamat=%s
        WHERE nip=%s
        """
        try:
            cursor.execute(sql, (nama, no_tlp, alamat, nip))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err

    # ==========================
    # DELETE DOKTER
    # ==========================
    @staticmethod
    def delete(nip):
        try:
            cursor.execute("DELETE FROM dokter WHERE nip=%s", (nip,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err
