"""
Pendaftaran Class - Model untuk data pendaftaran pasien
Mengelola CRUD operations untuk pendaftaran pemeriksaan

Class ini standalone untuk mengelola proses pendaftaran pasien.
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


class Pendaftaran:
    """
    Pendaftaran class untuk mengelola data pendaftaran pasien.
    
    Class structure:
    - Standalone class untuk data pendaftaran
    - Mengelola informasi awal pasien sebelum pemeriksaan
    - Bridge antara Pasien dan Pemeriksaan
    
    Attributes:
        nik (str): NIK pasien yang mendaftar
        nama (str): Nama lengkap pasien
        tgllhr (str): Tanggal lahir pasien
        jk (str): Jenis kelamin pasien
        no_telp (str): Nomor telepon pasien
        keluhan (str): Keluhan/gejala awal pasien
    """
    
    def __init__(self, nik=None, nama=None, tgllhr=None, jk=None, no_telp=None, keluhan=None):
        """
        Constructor untuk Pendaftaran class
        
        Args:
            nik (str): NIK pasien
            nama (str): Nama lengkap
            tgllhr (str): Tanggal lahir (format: YYYY-MM-DD)
            jk (str): Jenis kelamin (L/P)
            no_telp (str): Nomor telepon
            keluhan (str): Keluhan awal
        """
        self.nik = nik
        self.nama = nama
        self.tgllhr = tgllhr
        self.jk = jk
        self.no_telp = no_telp
        self.keluhan = keluhan

    def insert_pendaftaran(self):
        sql = """
        INSERT INTO pendaftaran 
        (nik, nama, tgllhr, jk, no_telp, keluhan)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (
            self.nik,
            self.nama,
            self.tgllhr,
            self.jk,
            self.no_telp,
            self.keluhan
        )

        try:
            cursor.execute(sql, val)
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal menyimpan data: {err}"
    
    @staticmethod
    def get_all():
        """Ambil semua data pendaftaran"""
        sql = """
        SELECT nik, nama, tgllhr, jk, no_telp, keluhan
        FROM pendaftaran
        ORDER BY nik DESC
        """
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_all pendaftaran: {err}")
            return []
    
    @staticmethod
    def get_by_id(id_pendaftaran):
        """Ambil data pendaftaran berdasarkan ID"""
        sql = "SELECT * FROM pendaftaran WHERE id_pendaftaran=%s"
        try:
            cursor.execute(sql, (id_pendaftaran,))
            return cursor.fetchone()
        except:
            return None
    
    @staticmethod
    def get_by_nik(nik):
        """Ambil data pendaftaran berdasarkan NIK"""
        sql = "SELECT nik, nama, tgllhr, jk, no_telp, keluhan FROM pendaftaran WHERE nik=%s ORDER BY nik DESC"
        try:
            cursor.execute(sql, (nik,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error get_by_nik: {err}")
            return []
    
    @staticmethod
    def update(nik, nama, tgllhr, jk, no_telp, keluhan, old_nik=None):
        """Update data pendaftaran berdasarkan NIK"""
        if old_nik is None:
            old_nik = nik
        
        sql = """
        UPDATE pendaftaran 
        SET nik=%s, nama=%s, tgllhr=%s, jk=%s, no_telp=%s, keluhan=%s
        WHERE nik=%s
        """
        try:
            cursor.execute(sql, (nik, nama, tgllhr, jk, no_telp, keluhan, old_nik))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal update: {err}"
    
    @staticmethod
    def delete(nik):
        """Hapus data pendaftaran berdasarkan NIK"""
        sql = "DELETE FROM pendaftaran WHERE nik=%s"
        try:
            cursor.execute(sql, (nik,))
            db.commit()
            return True
        except mysql.connector.Error as err:
            return f"Gagal hapus: {err}"


# ==========================
# CONTOH PENGGUNAAN (CLI)
# ==========================
if __name__ == "__main__":
    nik = input("NIK              : ")
    nama = input("Nama             : ")
    tgllhr = input("Tanggal Lahir (YYYY-MM-DD): ")
    jk = input("Jenis Kelamin (Laki-laki / Perempuan): ")
    no_telp = input("No Telp          : ")
    keluhan = input("Keluhan          : ")

    daftar = Pendaftaran(
        nik,
        nama,
        tgllhr,
        jk,
        no_telp,
        keluhan
    )

    result = daftar.insert_pendaftaran()

    if result is True:
        print("✅ Pendaftaran berhasil disimpan")
    else:
        print("❌", result)
