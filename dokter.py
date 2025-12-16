"""
Dokter Class - Model untuk data dokter dalam sistem klinik
Mengelola CRUD operations untuk data dokter

Class ini standalone (tidak inherit dari User) karena merepresentasikan
data dokter di database, bukan user authentication.
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


class Dokter:
    """
    Dokter class untuk mengelola data dokter.
    
    Class structure:
    - Standalone class (tidak inherit dari class lain)
    - Fokus pada data management dokter (CRUD operations)
    - Berbeda dengan Admin yang inherit dari User untuk authentication
    
    Attributes:
        nip (str): Nomor Induk Pegawai dokter
        nama (str): Nama lengkap dokter
        no_tlp (str): Nomor telepon dokter
        alamat (str): Alamat lengkap dokter
    """
    
    def __init__(self, nip=None, nama=None, no_tlp=None, alamat=None):
        """
        Constructor untuk Dokter class
        
        Args:
            nip (str): Nomor Induk Pegawai
            nama (str): Nama lengkap
            no_tlp (str): Nomor telepon
            alamat (str): Alamat lengkap
        """
        self.nip = nip
        self.nama = nama
        self.no_tlp = no_tlp
        self.alamat = alamat

    # ==========================
    # INSERT DOKTER
    # ==========================
    def insert(self):
        """
        Insert data dokter baru ke database
        
        Returns:
            bool/Exception: True jika berhasil, Exception jika gagal
        """
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
        """
        Ambil semua data dokter dari database
        
        Returns:
            list: List of tuples berisi data dokter
        """
        cursor.execute("SELECT * FROM dokter")
        return cursor.fetchall()

    # ==========================
    # AMBIL DOKTER BY NIP
    # ==========================
    @staticmethod
    def get_by_nip(nip):
        """
        Ambil data dokter berdasarkan NIP
        
        Args:
            nip (str): Nomor Induk Pegawai dokter
            
        Returns:
            tuple: Data dokter jika ditemukan, None jika tidak
        """
        cursor.execute("SELECT * FROM dokter WHERE nip=%s", (nip,))
        return cursor.fetchone()

    # ==========================
    # UPDATE DOKTER
    # ==========================
    @staticmethod
    def update(nip, nama, no_tlp, alamat):
        """
        Update data dokter berdasarkan NIP
        
        Args:
            nip (str): Nomor Induk Pegawai dokter
            nama (str): Nama baru
            no_tlp (str): Nomor telepon baru
            alamat (str): Alamat baru
            
        Returns:
            bool/Exception: True jika berhasil, Exception jika gagal
        """
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
        """
        Hapus data dokter berdasarkan NIP
        
        Args:
            nip (str): Nomor Induk Pegawai dokter yang akan dihapus
            
        Returns:
            bool/Exception: True jika berhasil, Exception jika gagal
        """
        try:
            cursor.execute("DELETE FROM dokter WHERE nip=%s", (nip,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return err
    
    def __str__(self):
        """String representation of Dokter object"""
        return f"Dokter(nip={self.nip}, nama={self.nama})"
    
    def __repr__(self):
        """Official string representation of Dokter object"""
        return self.__str__()

