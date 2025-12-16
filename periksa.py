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
    def __init__(self, nik, diagnosa, resep, total_biaya, total_obat):
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
        sql = """
        SELECT p.id_pemeriksaan, p.nik, d.nama,
               p.diagnosa, p.resep,
               p.total_obat, p.total_biaya
        FROM pemeriksaan p
        JOIN pendaftaran d ON p.nik = d.nik
        ORDER BY p.id_pemeriksaan DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()

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
