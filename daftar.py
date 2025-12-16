import mysql.connector
from datetime import datetime

# Koneksi database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bismillah"
)

cursor = db.cursor()


class Pendaftaran:
    def __init__(self, nik, nama, tgllhr, jk, no_telp, keluhan):
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
