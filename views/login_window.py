"""
LoginWindow - Form Login Pasien & Dokter
Author: Klinik Management System
Date: 16 Desember 2025

Window ini untuk login pasien dan dokter
Routing berdasarkan role:
- pasien → DashboardPasienWindow
- dokter → PemeriksaanDokterWindow
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys
import os

# Import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.admin import Admin

class LoginWindow(QWidget):
    """Window untuk login pasien dan dokter"""
    
    # Signals
    login_success = pyqtSignal(dict)  # Emit user data
    show_register = pyqtSignal()  # Emit untuk show register window
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle("Login - Sistem Klinik")
        self.setGeometry(100, 100, 450, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLabel {
                color: #333;
                font-size: 11pt;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 11pt;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                padding: 12px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton#btnLogin {
                background-color: #2196F3;
                color: white;
            }
            QPushButton#btnLogin:hover {
                background-color: #1976D2;
            }
            QPushButton#btnRegister {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#btnRegister:hover {
                background-color: #45a049;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 40, 50, 40)
        
        # Header
        header = QLabel("🏥 SISTEM KLINIK")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont('Arial', 20, QFont.Bold))
        header.setStyleSheet("color: #2196F3; margin-bottom: 10px;")
        main_layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Silakan login untuk melanjutkan")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 10pt; margin-bottom: 20px;")
        main_layout.addWidget(subtitle)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line)
        
        # Username
        lbl_username = QLabel("Username:")
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Masukkan username")
        main_layout.addWidget(lbl_username)
        main_layout.addWidget(self.txt_username)
        
        # Password
        lbl_password = QLabel("Password:")
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Masukkan password")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.returnPressed.connect(self.login)  # Enter untuk login
        main_layout.addWidget(lbl_password)
        main_layout.addWidget(self.txt_password)
        
        # Login button
        self.btn_login = QPushButton("🔐 LOGIN")
        self.btn_login.setObjectName("btnLogin")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.login)
        main_layout.addWidget(self.btn_login)
        
        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line2)
        
        # Register info
        register_info = QLabel("Belum punya akun?")
        register_info.setAlignment(Qt.AlignCenter)
        register_info.setStyleSheet("color: #666; font-size: 10pt;")
        main_layout.addWidget(register_info)
        
        # Register button
        self.btn_register = QPushButton("📝 DAFTAR SEKARANG")
        self.btn_register.setObjectName("btnRegister")
        self.btn_register.setCursor(Qt.PointingHandCursor)
        self.btn_register.clicked.connect(self.open_register)
        main_layout.addWidget(self.btn_register)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def login(self):
        """Proses login"""
        username = self.txt_username.text().strip()
        password = self.txt_password.text()
        
        # Validasi
        if not username or not password:
            QMessageBox.warning(self, "Validasi", 
                              "Username dan Password wajib diisi!")
            return
        
        # Proses login
        user = Admin.login(username, password)
        
        if user:
            # Login berhasil
            role = user['role']
            
            if role == 'pasien':
                QMessageBox.information(self, "Login Berhasil", 
                                      f"Selamat datang, Pasien!\n\nAnda akan diarahkan ke Dashboard Pendaftaran.")
            else:  # dokter
                QMessageBox.information(self, "Login Berhasil", 
                                      f"Selamat datang, Dokter!\n\nAnda akan diarahkan ke Form Pemeriksaan.")
            
            # Emit signal dengan data user
            self.login_success.emit(user)
            
            # Clear form
            self.txt_username.clear()
            self.txt_password.clear()
            
            # Hide login window
            self.hide()
        else:
            # Login gagal
            QMessageBox.critical(self, "Login Gagal", 
                               "Username atau Password salah!\n\nSilakan coba lagi.")
            self.txt_password.clear()
            self.txt_password.setFocus()
    
    def open_register(self):
        """Buka register window"""
        self.show_register.emit()
        self.hide()
    
    def show_window(self):
        """Tampilkan login window"""
        self.show()
        self.txt_username.setFocus()
    
    def closeEvent(self, event):
        """Override close event"""
        reply = QMessageBox.question(self, 'Keluar', 
                                    'Apakah Anda yakin ingin keluar dari aplikasi?',
                                    QMessageBox.Yes | QMessageBox.No, 
                                    QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.deleteLater()
            event.accept()
        else:
            event.ignore()
