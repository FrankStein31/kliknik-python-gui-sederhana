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
        """
        Constructor untuk Pasien class
        
        Args:
            nik (str): Nomor Induk Kependudukan (16 digit)
            nama (str): Nama lengkap
            no_tlp (str): Nomor telepon
            alamat (str): Alamat lengkap
        """
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
        """
        Hapus data pasien berdasarkan NIK
        
        Args:
            nik (str): Nomor Induk Kependudukan pasien yang akan dihapus
            
        Returns:
            bool/Exception: True jika berhasil, Exception jika gagal
        """
        try:
            cursor.execute("DELETE FROM pasien WHERE nik=%s", (nik,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err
    
    def __str__(self):
        """String representation of Pasien object"""
        return f"Pasien(nik={self.nik}, nama={self.nama})"
    
    def __repr__(self):
        """Official string representation of Pasien object"""
        return self.__str__()

