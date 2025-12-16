"""
RegisterWindow - Form Registrasi Pasien Baru
Author: Klinik Management System
Date: 16 Desember 2025

Window ini untuk pasien register akun baru
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import sys
import os

# Import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.pasien import Pasien

class RegisterWindow(QWidget):
    """Window untuk registrasi pasien baru"""
    
    # Signal untuk kembali ke login
    back_to_login = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle("Register - Sistem Klinik")
        self.setGeometry(100, 100, 500, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLabel {
                color: #333;
                font-size: 11pt;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 11pt;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                padding: 10px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton#btnRegister {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#btnRegister:hover {
                background-color: #45a049;
            }
            QPushButton#btnBack {
                background-color: #757575;
                color: white;
            }
            QPushButton#btnBack:hover {
                background-color: #616161;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(40, 30, 40, 30)
        
        # Header
        header = QLabel("📝 REGISTRASI PASIEN BARU")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont('Arial', 18, QFont.Bold))
        header.setStyleSheet("color: #4CAF50; margin-bottom: 10px;")
        main_layout.addWidget(header)
        
        # Info text
        info = QLabel("Silakan isi form di bawah untuk membuat akun baru")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #666; font-size: 10pt; margin-bottom: 10px;")
        main_layout.addWidget(info)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line)
        
        # Form fields
        # NIK
        lbl_nik = QLabel("NIK (16 digit):")
        self.txt_nik = QLineEdit()
        self.txt_nik.setPlaceholderText("Contoh: 3201234567890123")
        self.txt_nik.setMaxLength(16)
        main_layout.addWidget(lbl_nik)
        main_layout.addWidget(self.txt_nik)
        
        # Nama
        lbl_nama = QLabel("Nama Lengkap:")
        self.txt_nama = QLineEdit()
        self.txt_nama.setPlaceholderText("Masukkan nama lengkap")
        main_layout.addWidget(lbl_nama)
        main_layout.addWidget(self.txt_nama)
        
        # No Telepon
        lbl_telp = QLabel("No. Telepon:")
        self.txt_telp = QLineEdit()
        self.txt_telp.setPlaceholderText("Contoh: 081234567890")
        main_layout.addWidget(lbl_telp)
        main_layout.addWidget(self.txt_telp)
        
        # Alamat
        lbl_alamat = QLabel("Alamat:")
        self.txt_alamat = QTextEdit()
        self.txt_alamat.setPlaceholderText("Masukkan alamat lengkap")
        self.txt_alamat.setMaximumHeight(80)
        main_layout.addWidget(lbl_alamat)
        main_layout.addWidget(self.txt_alamat)
        
        # Username
        lbl_username = QLabel("Username (untuk login):")
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Pilih username unik")
        main_layout.addWidget(lbl_username)
        main_layout.addWidget(self.txt_username)
        
        # Password
        lbl_password = QLabel("Password:")
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Minimal 6 karakter")
        self.txt_password.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(lbl_password)
        main_layout.addWidget(self.txt_password)
        
        # Confirm Password
        lbl_confirm = QLabel("Konfirmasi Password:")
        self.txt_confirm = QLineEdit()
        self.txt_confirm.setPlaceholderText("Ulangi password")
        self.txt_confirm.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(lbl_confirm)
        main_layout.addWidget(self.txt_confirm)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_register = QPushButton("✓ DAFTAR")
        self.btn_register.setObjectName("btnRegister")
        self.btn_register.setCursor(Qt.PointingHandCursor)
        self.btn_register.clicked.connect(self.register)
        
        self.btn_back = QPushButton("← KEMBALI")
        self.btn_back.setObjectName("btnBack")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.go_back)
        
        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_register)
        
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def register(self):
        """Proses registrasi pasien baru"""
        # Ambil data dari form
        nik = self.txt_nik.text().strip()
        nama = self.txt_nama.text().strip()
        no_telp = self.txt_telp.text().strip()
        alamat = self.txt_alamat.toPlainText().strip()
        username = self.txt_username.text().strip()
        password = self.txt_password.text()
        confirm = self.txt_confirm.text()
        
        # Validasi
        if not all([nik, nama, username, password]):
            QMessageBox.warning(self, "Validasi", 
                              "NIK, Nama, Username, dan Password wajib diisi!")
            return
        
        # Validasi NIK 16 digit
        if len(nik) != 16 or not nik.isdigit():
            QMessageBox.warning(self, "Validasi", 
                              "NIK harus 16 digit angka!")
            self.txt_nik.setFocus()
            return
        
        # Validasi password minimal 6 karakter
        if len(password) < 6:
            QMessageBox.warning(self, "Validasi", 
                              "Password minimal 6 karakter!")
            self.txt_password.setFocus()
            return
        
        # Validasi konfirmasi password
        if password != confirm:
            QMessageBox.warning(self, "Validasi", 
                              "Password dan konfirmasi password tidak cocok!")
            self.txt_confirm.setFocus()
            return
        
        # Cek NIK sudah terdaftar
        if Pasien.check_nik_exists(nik):
            QMessageBox.warning(self, "NIK Sudah Terdaftar", 
                              f"NIK {nik} sudah terdaftar!\nSilakan gunakan NIK lain atau login jika sudah punya akun.")
            self.txt_nik.setFocus()
            return
        
        # Proses registrasi
        pasien = Pasien(
            nik=nik,
            nama=nama,
            no_telp=no_telp,
            alamat=alamat,
            username=username,
            password=password
        )
        
        success, message = pasien.register()
        
        if success:
            QMessageBox.information(self, "Berhasil", 
                                  f"{message}\n\nSilakan login dengan username: {username}")
            self.clear_form()
            self.go_back()  # Kembali ke login
        else:
            QMessageBox.critical(self, "Gagal", f"Registrasi gagal!\n{message}")
    
    def clear_form(self):
        """Reset semua field"""
        self.txt_nik.clear()
        self.txt_nama.clear()
        self.txt_telp.clear()
        self.txt_alamat.clear()
        self.txt_username.clear()
        self.txt_password.clear()
        self.txt_confirm.clear()
        self.txt_nik.setFocus()
    
    def go_back(self):
        """Kembali ke login window"""
        self.back_to_login.emit()
        self.close()
        self.deleteLater()
    
    def closeEvent(self, event):
        """Override close event"""
        self.deleteLater()
        event.accept()
