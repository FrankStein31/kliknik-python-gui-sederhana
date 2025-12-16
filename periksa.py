"""
Pemeriksaan Class - Model untuk data pemeriksaan pasien
Mengelola CRUD operations untuk data pemeriksaan dan resep

Class ini standalone untuk mengelola data pemeriksaan medis.
"""
import mysql.connector
from datetime import datetime

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


class Pemeriksaan:
    """
    Pemeriksaan class untuk mengelola data pemeriksaan medis pasien.
    
    Class structure:
    - Standalone class untuk data pemeriksaan
    - Mengelola diagnosa, resep, dan pembayaran
    - Terintegrasi dengan data Pasien dan Pendaftaran
    
    Attributes:
        nik (str): NIK pasien yang diperiksa
        diagnosa (str): Hasil diagnosa dokter
        resep (str): Resep obat dari dokter
        total_biaya (float): Total biaya pemeriksaan dan obat
        total_obat (int): Jumlah item obat
    """
    
    def __init__(self, nik, diagnosa, resep, total_biaya, total_obat):
        """
        Constructor untuk Pemeriksaan class
        
        Args:
            nik (str): NIK pasien
            diagnosa (str): Hasil diagnosa
            resep (str): Resep obat
            total_biaya (float): Total biaya
            total_obat (int): Jumlah obat
        """
        self.nik = nik
        self.diagnosa = diagnosa
        self.resep = resep
        self.total_biaya = total_biaya
        self.total_obat = total_obat

    # ==========================
    # INSERT PEMERIKSAAN
    # ==========================
    def insert_pemeriksaan(self):
        sql = """
        INSERT INTO pemeriksaan 
        (nik, diagnosa, resep, total_biaya, total_obat)
        VALUES (%s, %s, %s, %s, %s)
        """
        val = (
            self.nik,
            self.diagnosa,
            self.resep,
            self.total_biaya,
            self.total_obat
        )

        try:
            cursor.execute(sql, val)
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal menyimpan pemeriksaan: {err}"

    # ==========================
    # TAMPILKAN SEMUA DATA
    # ==========================
    @staticmethod
    def get_all():
        """Ambil semua data pemeriksaan dengan atau tanpa join"""
        sql = """
        SELECT p.id_pemeriksaan, p.nik, p.diagnosa, p.resep, p.total_obat, p.total_biaya
        FROM pemeriksaan p
        ORDER BY p.id_pemeriksaan DESC
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_all pemeriksaan: {err}")
            return []
    
    @staticmethod
    def get_all_with_name():
        """Ambil semua data pemeriksaan dengan nama dari pasien atau pendaftaran"""
        sql = """
        SELECT p.id_pemeriksaan, p.nik, 
               COALESCE(pa.nama, 'Unknown') as nama,
               p.diagnosa, p.resep, p.total_obat, p.total_biaya
        FROM pemeriksaan p
        LEFT JOIN pasien pa ON p.nik = pa.nik
        ORDER BY p.id_pemeriksaan DESC
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_all_with_name: {err}")
            # Fallback ke query sederhana
            return Pemeriksaan.get_all()

    # ==========================
    # UPDATE PEMERIKSAAN
    # ==========================
    @staticmethod
    def update_pemeriksaan(id_pemeriksaan, diagnosa, resep, total_biaya, total_obat):
        sql = """
        UPDATE pemeriksaan SET
            diagnosa = %s,
            resep = %s,
            total_biaya = %s,
            total_obat = %s
        WHERE id_pemeriksaan = %s
        """
        val = (diagnosa, resep, total_biaya, total_obat, id_pemeriksaan)

        try:
            cursor.execute(sql, val)
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal update pemeriksaan: {err}"

    # ==========================
    # DELETE PEMERIKSAAN
    # ==========================
    @staticmethod
    def delete_pemeriksaan(id_pemeriksaan):
        sql = "DELETE FROM pemeriksaan WHERE id_pemeriksaan = %s"

        try:
            cursor.execute(sql, (id_pemeriksaan,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal hapus pemeriksaan: {err}"
    
    @staticmethod
    def get_by_nik(nik):
        """Ambil pemeriksaan berdasarkan NIK"""
        sql = """
        SELECT p.id_pemeriksaan, p.nik, 
               COALESCE(pa.nama, 'Unknown') as nama,
               p.diagnosa, p.resep, p.total_obat, p.total_biaya
        FROM pemeriksaan p
        LEFT JOIN pasien pa ON p.nik = pa.nik
        WHERE p.nik = %s
        ORDER BY p.id_pemeriksaan DESC
        """
        try:
            cursor.execute(sql, (nik,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_by_nik: {err}")
            return []
    
    @staticmethod
    def get_by_id(id_pemeriksaan):
        """Ambil pemeriksaan berdasarkan ID"""
        sql = "SELECT * FROM pemeriksaan WHERE id_pemeriksaan = %s"
        try:
            cursor.execute(sql, (id_pemeriksaan,))
            return cursor.fetchone()
        except:
            return None
    
    @staticmethod
    def get_with_pendaftaran():
        """Ambil pemeriksaan dengan data pendaftaran"""
        sql = """
        SELECT 
            p.id_pemeriksaan,
            p.nik,
            COALESCE(pa.nama, pd.nama, 'Unknown') as nama,
            pd.keluhan,
            p.diagnosa,
            p.resep,
            p.total_biaya,
            p.total_obat
        FROM pemeriksaan p
        LEFT JOIN pasien pa ON p.nik = pa.nik
        LEFT JOIN pendaftaran pd ON p.nik = pd.nik
        GROUP BY p.id_pemeriksaan, p.nik, p.diagnosa, p.resep, p.total_biaya, p.total_obat
        ORDER BY p.id_pemeriksaan DESC
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_with_pendaftaran: {err}")
            return Pemeriksaan.get_all()


# ==========================
# CONTOH PENGGUNAAN (CLI)
# ==========================
if __name__ == "__main__":
    nik = input("NIK           : ")
    diagnosa = input("Diagnosa      : ")
    resep = input("Resep         : ")
    total_biaya = float(input("Total Biaya   : "))
    total_obat = int(input("Total Obat    : "))

    periksa = Pemeriksaan(
        nik,
        diagnosa,
        resep,
        total_biaya,
        total_obat
    )

    result = periksa.insert_pemeriksaan()

    if result is True:
        print("✅ Pemeriksaan berhasil disimpan")
    else:
        print("❌", result)
