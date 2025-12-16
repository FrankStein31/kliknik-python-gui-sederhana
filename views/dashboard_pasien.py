"""
DashboardPasienWindow - Dashboard Pendaftaran untuk Pasien
Author: Klinik Management System
Date: 16 Desember 2025

Window ini untuk:
- Pasien daftar pemeriksaan
- Lihat riwayat pendaftaran
- Akses profil
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QFrame, QDateEdit, QComboBox, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont
import sys
import os

# Import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.pasien import Pasien
from models.pendaftaran import Pendaftaran

class DashboardPasienWindow(QWidget):
    """Window dashboard untuk pasien"""
    
    # Signals
    show_profil = pyqtSignal(str)  # Emit username
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.username = user_data['username']
        
        # Get data pasien
        self.pasien_data = Pasien.get_by_username(self.username)
        
        if not self.pasien_data:
            QMessageBox.critical(None, "Error", "Data pasien tidak ditemukan!")
            return
        
        self.nik = self.pasien_data['nik']
        self.nama = self.pasien_data['nama']
        
        self.init_ui()
        self.load_riwayat()
    
    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle(f"Dashboard Pasien - {self.nama}")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                font-size: 10pt;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                padding: 10px 15px;
                font-size: 10pt;
                font-weight: bold;
                border-radius: 5px;
                border: none;
            }
            QPushButton#btnDaftar {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#btnDaftar:hover {
                background-color: #45a049;
            }
            QPushButton#btnProfil {
                background-color: #2196F3;
                color: white;
            }
            QPushButton#btnProfil:hover {
                background-color: #1976D2;
            }
            QPushButton#btnLogout {
                background-color: #f44336;
                color: white;
            }
            QPushButton#btnLogout:hover {
                background-color: #da190b;
            }
            QTableWidget {
                border: 1px solid #ddd;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #000;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel(f"👤 Dashboard Pasien: {self.nama}")
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setStyleSheet("color: #4CAF50;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        # Buttons
        self.btn_profil = QPushButton("👤 Profil Saya")
        self.btn_profil.setObjectName("btnProfil")
        self.btn_profil.setCursor(Qt.PointingHandCursor)
        self.btn_profil.clicked.connect(self.open_profil)
        header_layout.addWidget(self.btn_profil)
        
        self.btn_logout = QPushButton("🚪 Logout")
        self.btn_logout.setObjectName("btnLogout")
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(self.btn_logout)
        
        main_layout.addLayout(header_layout)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ddd;")
        main_layout.addWidget(line)
        
        # Splitter untuk form dan tabel
        splitter = QSplitter(Qt.Vertical)
        
        # === FORM PENDAFTARAN ===
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        form_title = QLabel("📝 FORM PENDAFTARAN PEMERIKSAAN")
        form_title.setFont(QFont('Arial', 12, QFont.Bold))
        form_title.setStyleSheet("color: #4CAF50;")
        form_layout.addWidget(form_title)
        
        # Tanggal Lahir
        lbl_tgllhr = QLabel("Tanggal Lahir:")
        self.date_tgllhr = QDateEdit()
        self.date_tgllhr.setCalendarPopup(True)
        self.date_tgllhr.setDate(QDate.currentDate().addYears(-25))
        self.date_tgllhr.setDisplayFormat("dd-MM-yyyy")
        form_layout.addWidget(lbl_tgllhr)
        form_layout.addWidget(self.date_tgllhr)
        
        # Jenis Kelamin
        lbl_jk = QLabel("Jenis Kelamin:")
        self.combo_jk = QComboBox()
        self.combo_jk.addItems(["Laki-laki", "Perempuan"])
        form_layout.addWidget(lbl_jk)
        form_layout.addWidget(self.combo_jk)
        
        # No Telepon
        lbl_telp = QLabel("No. Telepon:")
        self.txt_telp = QLineEdit()
        self.txt_telp.setText(self.pasien_data.get('no_telp', ''))
        self.txt_telp.setPlaceholderText("Contoh: 081234567890")
        form_layout.addWidget(lbl_telp)
        form_layout.addWidget(self.txt_telp)
        
        # Keluhan
        lbl_keluhan = QLabel("Keluhan:")
        self.txt_keluhan = QTextEdit()
        self.txt_keluhan.setPlaceholderText("Jelaskan keluhan Anda...")
        self.txt_keluhan.setMaximumHeight(100)
        form_layout.addWidget(lbl_keluhan)
        form_layout.addWidget(self.txt_keluhan)
        
        # Button Daftar
        self.btn_daftar = QPushButton("✓ DAFTAR SEKARANG")
        self.btn_daftar.setObjectName("btnDaftar")
        self.btn_daftar.setCursor(Qt.PointingHandCursor)
        self.btn_daftar.clicked.connect(self.daftar_periksa)
        form_layout.addWidget(self.btn_daftar)
        
        form_widget.setLayout(form_layout)
        splitter.addWidget(form_widget)
        
        # === TABEL RIWAYAT ===
        table_widget = QWidget()
        table_layout = QVBoxLayout()
        
        table_title = QLabel("📋 RIWAYAT PENDAFTARAN")
        table_title.setFont(QFont('Arial', 12, QFont.Bold))
        table_title.setStyleSheet("color: #2196F3;")
        table_layout.addWidget(table_title)
        
        self.table_riwayat = QTableWidget()
        self.table_riwayat.setColumnCount(6)
        self.table_riwayat.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Keluhan", "Status", "Jenis Kelamin", "No. Telp"
        ])
        self.table_riwayat.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_riwayat.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_riwayat.setSelectionBehavior(QTableWidget.SelectRows)
        table_layout.addWidget(self.table_riwayat)
        
        table_widget.setLayout(table_layout)
        splitter.addWidget(table_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 400])
        
        main_layout.addWidget(splitter)
        
        self.setLayout(main_layout)
    
    def daftar_periksa(self):
        """Proses pendaftaran pemeriksaan"""
        tgllhr = self.date_tgllhr.date().toString("yyyy-MM-dd")
        jk = self.combo_jk.currentText()
        no_telp = self.txt_telp.text().strip()
        keluhan = self.txt_keluhan.toPlainText().strip()
        
        # Validasi
        if not keluhan:
            QMessageBox.warning(self, "Validasi", "Keluhan wajib diisi!")
            self.txt_keluhan.setFocus()
            return
        
        # Konfirmasi
        reply = QMessageBox.question(self, 'Konfirmasi', 
                                    f'Daftar pemeriksaan dengan keluhan:\n"{keluhan}"\n\nLanjutkan?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.No:
            return
        
        # Simpan pendaftaran
        pendaftaran = Pendaftaran(
            nik=self.nik,
            nama=self.nama,
            tgllhr=tgllhr,
            jk=jk,
            no_telp=no_telp,
            keluhan=keluhan
        )
        
        success, message, id_pendaftaran = pendaftaran.daftar()
        
        if success:
            QMessageBox.information(self, "Berhasil", 
                                  f"{message}\n\nID Pendaftaran: {id_pendaftaran}\n\nSilakan tunggu, dokter akan segera memeriksa Anda.")
            # Clear form
            self.txt_keluhan.clear()
            # Reload riwayat
            self.load_riwayat()
        else:
            QMessageBox.critical(self, "Gagal", f"Pendaftaran gagal!\n{message}")
    
    def load_riwayat(self):
        """Load riwayat pendaftaran"""
        data = Pendaftaran.get_by_nik(self.nik)
        
        self.table_riwayat.setRowCount(len(data))
        
        for row, item in enumerate(data):
            self.table_riwayat.setItem(row, 0, QTableWidgetItem(str(item['id_pendaftaran'])))
            self.table_riwayat.setItem(row, 1, QTableWidgetItem(str(item['created_at'])))
            self.table_riwayat.setItem(row, 2, QTableWidgetItem(item['keluhan'] or '-'))
            
            # Status dengan warna
            status_item = QTableWidgetItem(item['status'].upper())
            if item['status'] == 'menunggu':
                status_item.setBackground(Qt.yellow)
            elif item['status'] == 'selesai':
                status_item.setBackground(Qt.green)
            else:
                status_item.setBackground(Qt.lightGray)
            self.table_riwayat.setItem(row, 3, status_item)
            
            self.table_riwayat.setItem(row, 4, QTableWidgetItem(item['jk'] or '-'))
            self.table_riwayat.setItem(row, 5, QTableWidgetItem(item['no_telp'] or '-'))
    
    def open_profil(self):
        """Buka profil pasien"""
        self.show_profil.emit(self.username)
        self.close()
        self.deleteLater()
    
    def logout(self):
        """Logout"""
        reply = QMessageBox.question(self, 'Logout', 
                                    'Apakah Anda yakin ingin logout?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.logout_signal.emit()
            self.close()
            self.deleteLater()
    
    def closeEvent(self, event):
        """Override close event"""
        self.deleteLater()
        event.accept()
