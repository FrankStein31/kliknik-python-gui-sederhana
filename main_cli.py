"""
SISTEM INFORMASI KLINIK - CLI VERSION (BACKUP)
Versi Command Line Interface
"""
from admin import Admin
from daftar import Pendaftaran
from periksa import Pemeriksaan
from pasien import Pasien
from dokter import Dokter
import os


# ==========================
# UTILITAS
# ==========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print("=" * 50)
    print(" SISTEM INFORMASI KLINIK ")
    print("=" * 50)


# ==========================
# LOGIN
# ==========================
def login():
    while True:
        clear()
        header()
        print("--- LOGIN SISTEM ---")

        username = input("Username : ")
        password = input("Password : ")

        admin = Admin(username, password)
        result = admin.login()

        if result["status"]:
            print("\n✅ Login berhasil")
            print("Username :", result["username"])
            print("Role     :", result["role"])
            input("\nTekan ENTER untuk lanjut...")
            return result
        else:
            print("\n❌", result.get("message", "Login gagal"))
            input("Tekan ENTER untuk ulangi...")


# ==========================
# MENU UTAMA
# ==========================
def menu_utama(role):
    clear()
    header()

    if role == "dokter":
        print("1. Pemeriksaan Pasien")
        print("2. Data Dokter")
        print("3. Logout")
    else:  # pasien
        print("1. Pendaftaran Periksa")
        print("2. Data Pasien")
        print("3. Logout")


# ==========================
# MENU DOKTER
# ==========================
def menu_dokter_flow():
    while True:
        menu_utama("dokter")
        pilih = input("\nPilih Menu : ")

        if pilih == "1":
            menu_pemeriksaan()
        elif pilih == "2":
            menu_dokter()
        elif pilih == "3":
            print("\nLogout berhasil")
            input("Tekan ENTER...")
            break
        else:
            print("❌ Menu tidak tersedia")
            input("Tekan ENTER...")


# ==========================
# MENU PASIEN
# ==========================
def menu_pasien_flow():
    while True:
        menu_utama("pasien")
        pilih = input("\nPilih Menu : ")

        if pilih == "1":
            menu_pendaftaran()
        elif pilih == "2":
            menu_pasien()
        elif pilih == "3":
            print("\nLogout berhasil")
            input("Tekan ENTER...")
            break
        else:
            print("❌ Menu tidak tersedia")
            input("Tekan ENTER...")


# ==========================
# PENDAFTARAN PERIKSA (PASIEN)
# ==========================
def menu_pendaftaran():
    clear()
    header()
    print("--- PENDAFTARAN PERIKSA ---")

    nik = input("NIK              : ")
    nama = input("Nama             : ")
    tgllhr = input("Tanggal Lahir (YYYY-MM-DD): ")
    jk = input("Jenis Kelamin (Laki-laki / Perempuan): ")
    no_telp = input("No Telp          : ")
    keluhan = input("Keluhan          : ")

    daftar = Pendaftaran(nik, nama, tgllhr, jk, no_telp, keluhan)
    result = daftar.insert_pendaftaran()

    print("\n✅ Berhasil" if result is True else f"\n❌ {result}")
    input("Tekan ENTER...")


# ==========================
# PEMERIKSAAN (DOKTER)
# ==========================
def menu_pemeriksaan():
    clear()
    header()
    print("--- PEMERIKSAAN PASIEN ---")

    nik = input("NIK Pasien   : ")
    diagnosa = input("Diagnosa    : ")
    resep = input("Resep       : ")
    total_biaya = float(input("Total Biaya : "))
    total_obat = int(input("Total Obat  : "))

    periksa = Pemeriksaan(nik, diagnosa, resep, total_biaya, total_obat)
    result = periksa.insert_pemeriksaan()

    print("\n✅ Berhasil" if result is True else f"\n❌ {result}")
    input("Tekan ENTER...")


# ==========================
# DATA PASIEN (PASIEN)
# ==========================
def menu_pasien():
    clear()
    header()
    print("--- DATA PASIEN ---")

    data = Pasien.get_all()
    if not data:
        print("Belum ada data pasien")
    else:
        for p in data:
            print(f"NIK: {p[0]} | Nama: {p[1]} | Telp: {p[2]} | Alamat: {p[3]}")

    input("\nTekan ENTER...")


# ==========================
# DATA DOKTER (DOKTER)
# ==========================
def menu_dokter():
    clear()
    header()
    print("--- DATA DOKTER ---")

    data = Dokter.get_all()
    if not data:
        print("Belum ada data dokter")
    else:
        for d in data:
            print(f"NIP: {d[0]} | Nama: {d[1]} | Telp: {d[2]} | Alamat: {d[3]}")

    input("\nTekan ENTER...")


# ==========================
# PROGRAM UTAMA
# ==========================
def main():
    while True:
        user = login()
        role = user["role"]

        if role == "dokter":
            menu_dokter_flow()
        else:
            menu_pasien_flow()


# ==========================
# EKSEKUSI
# ==========================
if __name__ == "__main__":
    main()
