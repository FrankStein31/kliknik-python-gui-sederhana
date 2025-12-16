"""
ProfilPasienWindow - Profil Pasien dengan CRUD
Author: Klinik Management System
Date: 16 Desember 2025

Window ini untuk:
- READ: Lihat profil pasien
- UPDATE: Edit profil pasien
- DELETE: Hapus akun (CASCADE DELETE semua data)
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QFrame, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys
import os

# Import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.pasien import Pasien
from models.admin import Admin

class ProfilPasienWindow(QWidget):
    """Window profil untuk pasien dengan fitur DELETE AKUN"""
    
    # Signals
    back_to_dashboard = pyqtSignal(dict)  # Kembali ke dashboard
    account_deleted = pyqtSignal()  # Akun dihapus, kembali ke login
    
    def __init__(self, username):
        super().__init__()
        self.username = username
        
        # Get data pasien dan admin
        self.pasien_data = Pasien.get_by_username(username)
        
        if not self.pasien_data:
            QMessageBox.critical(None, "Error", "Data pasien tidak ditemukan!")
            return
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle(f"Profil Pasien - {self.pasien_data['nama']}")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                color: #333;
                font-size: 10pt;
            }
            QLineEdit, QTextEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                font-size: 10pt;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #2196F3;
            }
            QLineEdit:read-only {
                background-color: #f0f0f0;
                color: #666;
            }
            QPushButton {
                padding: 12px;
                font-size: 10pt;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton#btnSimpan {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#btnSimpan:hover {
                background-color: #45a049;
            }
            QPushButton#btnDelete {
                background-color: #f44336;
                color: white;
            }
            QPushButton#btnDelete:hover {
                background-color: #da190b;
            }
            QPushButton#btnBack {
                background-color: #757575;
                color: white;
            }
            QPushButton#btnBack:hover {
                background-color: #616161;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 5px;
                color: #2196F3;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("👤 PROFIL PASIEN")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont('Arial', 18, QFont.Bold))
        header.setStyleSheet("color: #2196F3; margin-bottom: 10px;")
        main_layout.addWidget(header)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line)
        
        # === DATA DIRI ===
        group_data = QGroupBox("Data Diri")
        data_layout = QVBoxLayout()
        data_layout.setSpacing(10)
        
        # NIK (readonly)
        lbl_nik = QLabel("NIK:")
        self.txt_nik = QLineEdit()
        self.txt_nik.setReadOnly(True)
        data_layout.addWidget(lbl_nik)
        data_layout.addWidget(self.txt_nik)
        
        # Nama
        lbl_nama = QLabel("Nama Lengkap:")
        self.txt_nama = QLineEdit()
        data_layout.addWidget(lbl_nama)
        data_layout.addWidget(self.txt_nama)
        
        # No Telepon
        lbl_telp = QLabel("No. Telepon:")
        self.txt_telp = QLineEdit()
        self.txt_telp.setPlaceholderText("Contoh: 081234567890")
        data_layout.addWidget(lbl_telp)
        data_layout.addWidget(self.txt_telp)
        
        # Alamat
        lbl_alamat = QLabel("Alamat:")
        self.txt_alamat = QTextEdit()
        self.txt_alamat.setMaximumHeight(80)
        data_layout.addWidget(lbl_alamat)
        data_layout.addWidget(self.txt_alamat)
        
        group_data.setLayout(data_layout)
        main_layout.addWidget(group_data)
        
        # === AKUN ===
        group_akun = QGroupBox("Informasi Akun")
        akun_layout = QVBoxLayout()
        akun_layout.setSpacing(10)
        
        # Username (readonly)
        lbl_username = QLabel("Username:")
        self.txt_username = QLineEdit()
        self.txt_username.setReadOnly(True)
        akun_layout.addWidget(lbl_username)
        akun_layout.addWidget(self.txt_username)
        
        # Password baru (optional)
        lbl_password = QLabel("Password Baru (kosongkan jika tidak ingin mengubah):")
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText("Minimal 6 karakter")
        akun_layout.addWidget(lbl_password)
        akun_layout.addWidget(self.txt_password)
        
        # Konfirmasi password
        lbl_confirm = QLabel("Konfirmasi Password Baru:")
        self.txt_confirm = QLineEdit()
        self.txt_confirm.setEchoMode(QLineEdit.Password)
        self.txt_confirm.setPlaceholderText("Ulangi password baru")
        akun_layout.addWidget(lbl_confirm)
        akun_layout.addWidget(self.txt_confirm)
        
        group_akun.setLayout(akun_layout)
        main_layout.addWidget(group_akun)
        
        # === BUTTONS ===
        btn_layout = QHBoxLayout()
        
        self.btn_back = QPushButton("⬅ Kembali")
        self.btn_back.setObjectName("btnBack")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.go_back)
        btn_layout.addWidget(self.btn_back)
        
        self.btn_delete = QPushButton("🗑 HAPUS AKUN")
        self.btn_delete.setObjectName("btnDelete")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.clicked.connect(self.delete_account)
        btn_layout.addWidget(self.btn_delete)
        
        self.btn_simpan = QPushButton("💾 SIMPAN")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.clicked.connect(self.simpan)
        btn_layout.addWidget(self.btn_simpan)
        
        main_layout.addLayout(btn_layout)
        
        # Warning text untuk delete
        warning = QLabel("⚠ PERINGATAN: Menghapus akun akan menghapus SEMUA data pendaftaran dan pemeriksaan Anda secara permanen!")
        warning.setAlignment(Qt.AlignCenter)
        warning.setWordWrap(True)
        warning.setStyleSheet("color: #f44336; font-size: 9pt; font-weight: bold; background-color: #ffebee; padding: 10px; border-radius: 5px;")
        main_layout.addWidget(warning)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def load_data(self):
        """Load data pasien ke form"""
        self.txt_nik.setText(self.pasien_data['nik'])
        self.txt_nama.setText(self.pasien_data['nama'])
        self.txt_telp.setText(self.pasien_data.get('no_telp', '') or '')
        self.txt_alamat.setText(self.pasien_data.get('alamat', '') or '')
        self.txt_username.setText(self.username)
    
    def simpan(self):
        """Simpan perubahan profil"""
        nama = self.txt_nama.text().strip()
        no_telp = self.txt_telp.text().strip()
        alamat = self.txt_alamat.toPlainText().strip()
        password_baru = self.txt_password.text()
        confirm = self.txt_confirm.text()
        
        # Validasi
        if not nama:
            QMessageBox.warning(self, "Validasi", "Nama wajib diisi!")
            return
        
        # Validasi password jika diisi
        if password_baru:
            if len(password_baru) < 6:
                QMessageBox.warning(self, "Validasi", "Password minimal 6 karakter!")
                return
            
            if password_baru != confirm:
                QMessageBox.warning(self, "Validasi", "Password dan konfirmasi tidak cocok!")
                return
        
        # Konfirmasi
        reply = QMessageBox.question(self, 'Konfirmasi', 
                                    'Simpan perubahan profil?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.No:
            return
        
        # Update profil
        pasien = Pasien(
            nik=self.pasien_data['nik'],
            nama=nama,
            no_telp=no_telp,
            alamat=alamat,
            username=self.username
        )
        
        success, message = pasien.update_profil()
        
        if success:
            # Update password jika diisi
            if password_baru:
                Admin.update_password(self.username, password_baru)
                QMessageBox.information(self, "Berhasil", 
                                      "Profil dan password berhasil diperbarui!")
            else:
                QMessageBox.information(self, "Berhasil", message)
            
            # Clear password fields
            self.txt_password.clear()
            self.txt_confirm.clear()
            
            # Reload data
            self.pasien_data = Pasien.get_by_username(self.username)
            self.load_data()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal update profil!\n{message}")
    
    def delete_account(self):
        """Hapus akun pasien (CASCADE DELETE)"""
        # Konfirmasi pertama
        reply1 = QMessageBox.warning(self, 'PERINGATAN!', 
                                    f'Anda akan menghapus akun:\n\n'
                                    f'NIK: {self.pasien_data["nik"]}\n'
                                    f'Nama: {self.pasien_data["nama"]}\n\n'
                                    f'Semua data pendaftaran dan pemeriksaan Anda\n'
                                    f'akan DIHAPUS PERMANEN!\n\n'
                                    f'Apakah Anda yakin?',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        
        if reply1 == QMessageBox.No:
            return
        
        # Konfirmasi kedua (double confirmation)
        reply2 = QMessageBox.critical(self, 'KONFIRMASI TERAKHIR!', 
                                     f'Ini adalah konfirmasi terakhir!\n\n'
                                     f'Akun Anda AKAN DIHAPUS PERMANEN!\n\n'
                                     f'Yakin ingin melanjutkan?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        
        if reply2 == QMessageBox.No:
            return
        
        # Proses delete
        pasien = Pasien(
            nik=self.pasien_data['nik'],
            nama=self.pasien_data['nama'],
            username=self.username
        )
        
        success, message = pasien.delete_akun()
        
        if success:
            QMessageBox.information(self, "Akun Dihapus", 
                                  f"{message}\n\n"
                                  f"Semua data Anda telah dihapus.\n"
                                  f"Terima kasih telah menggunakan layanan kami.")
            
            # Emit signal account deleted (kembali ke login)
            self.account_deleted.emit()
            self.close()
            self.deleteLater()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menghapus akun!\n{message}")
    
    def go_back(self):
        """Kembali ke dashboard"""
        # Emit signal dengan user data
        user_data = {
            'username': self.username,
            'role': 'pasien'
        }
        self.back_to_dashboard.emit(user_data)
        self.close()
        self.deleteLater()
    
    def closeEvent(self, event):
        """Override close event"""
        self.deleteLater()
        event.accept()
