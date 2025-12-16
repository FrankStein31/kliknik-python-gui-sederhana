"""
PemeriksaanDokterWindow - Form Pemeriksaan untuk Dokter
Author: Klinik Management System
Date: 16 Desember 2025

Window ini untuk:
- Lihat daftar pendaftaran (status: menunggu)
- Input hasil pemeriksaan
- CRUD pemeriksaan
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QFrame, QSplitter, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys
import os

# Import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.dokter import Dokter
from models.pendaftaran import Pendaftaran
from models.pemeriksaan import Pemeriksaan

class PemeriksaanDokterWindow(QWidget):
    """Window pemeriksaan untuk dokter"""
    
    # Signals
    show_profil = pyqtSignal(str)  # Emit username
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.username = user_data['username']
        
        # Get data dokter
        self.dokter_data = Dokter.get_by_username(self.username)
        
        if not self.dokter_data:
            QMessageBox.critical(None, "Error", "Data dokter tidak ditemukan!")
            return
        
        self.nip = self.dokter_data['nip']
        self.nama = self.dokter_data['nama']
        
        # Current selected pendaftaran
        self.selected_pendaftaran = None
        
        self.init_ui()
        self.load_pendaftaran()
    
    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle(f"Pemeriksaan Dokter - {self.nama}")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
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
                padding: 10px 15px;
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
            QPushButton#btnRefresh {
                background-color: #FF9800;
                color: white;
            }
            QPushButton#btnRefresh:hover {
                background-color: #F57C00;
            }
            QTableWidget {
                border: 1px solid #ddd;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #000;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
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
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        header = QLabel(f"👨‍⚕️ Form Pemeriksaan: {self.nama}")
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setStyleSheet("color: #2196F3;")
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
        
        # Splitter horizontal untuk tabel dan form
        splitter = QSplitter(Qt.Horizontal)
        
        # === KIRI: TABEL PENDAFTARAN ===
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # Title + Refresh
        title_layout = QHBoxLayout()
        table_title = QLabel("📋 DAFTAR PENDAFTARAN (Menunggu)")
        table_title.setFont(QFont('Arial', 11, QFont.Bold))
        table_title.setStyleSheet("color: #2196F3;")
        title_layout.addWidget(table_title)
        
        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setObjectName("btnRefresh")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_pendaftaran)
        title_layout.addWidget(self.btn_refresh)
        
        left_layout.addLayout(title_layout)
        
        self.table_pendaftaran = QTableWidget()
        self.table_pendaftaran.setColumnCount(5)
        self.table_pendaftaran.setHorizontalHeaderLabels([
            "ID", "Nama", "NIK", "Keluhan", "Tanggal"
        ])
        self.table_pendaftaran.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_pendaftaran.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_pendaftaran.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_pendaftaran.itemSelectionChanged.connect(self.on_select_pendaftaran)
        left_layout.addWidget(self.table_pendaftaran)
        
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)
        
        # === KANAN: FORM PEMERIKSAAN ===
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        form_title = QLabel("📝 FORM PEMERIKSAAN")
        form_title.setFont(QFont('Arial', 11, QFont.Bold))
        form_title.setStyleSheet("color: #4CAF50;")
        right_layout.addWidget(form_title)
        
        # Data Pasien (readonly)
        group_pasien = QGroupBox("Data Pasien")
        pasien_layout = QVBoxLayout()
        pasien_layout.setSpacing(8)
        
        lbl_id = QLabel("ID Pendaftaran:")
        self.txt_id = QLineEdit()
        self.txt_id.setReadOnly(True)
        pasien_layout.addWidget(lbl_id)
        pasien_layout.addWidget(self.txt_id)
        
        lbl_nama_pasien = QLabel("Nama Pasien:")
        self.txt_nama_pasien = QLineEdit()
        self.txt_nama_pasien.setReadOnly(True)
        pasien_layout.addWidget(lbl_nama_pasien)
        pasien_layout.addWidget(self.txt_nama_pasien)
        
        lbl_nik_pasien = QLabel("NIK:")
        self.txt_nik_pasien = QLineEdit()
        self.txt_nik_pasien.setReadOnly(True)
        pasien_layout.addWidget(lbl_nik_pasien)
        pasien_layout.addWidget(self.txt_nik_pasien)
        
        lbl_keluhan_pasien = QLabel("Keluhan:")
        self.txt_keluhan_pasien = QTextEdit()
        self.txt_keluhan_pasien.setReadOnly(True)
        self.txt_keluhan_pasien.setMaximumHeight(60)
        pasien_layout.addWidget(lbl_keluhan_pasien)
        pasien_layout.addWidget(self.txt_keluhan_pasien)
        
        group_pasien.setLayout(pasien_layout)
        right_layout.addWidget(group_pasien)
        
        # Form Input Pemeriksaan
        group_periksa = QGroupBox("Hasil Pemeriksaan")
        periksa_layout = QVBoxLayout()
        periksa_layout.setSpacing(8)
        
        lbl_diagnosa = QLabel("Diagnosa:")
        self.txt_diagnosa = QTextEdit()
        self.txt_diagnosa.setPlaceholderText("Masukkan diagnosa penyakit...")
        self.txt_diagnosa.setMaximumHeight(80)
        periksa_layout.addWidget(lbl_diagnosa)
        periksa_layout.addWidget(self.txt_diagnosa)
        
        lbl_resep = QLabel("Resep Obat:")
        self.txt_resep = QTextEdit()
        self.txt_resep.setPlaceholderText("Masukkan resep obat...")
        self.txt_resep.setMaximumHeight(80)
        periksa_layout.addWidget(lbl_resep)
        periksa_layout.addWidget(self.txt_resep)
        
        # Biaya
        biaya_layout = QHBoxLayout()
        
        # Biaya Dokter
        biaya_dokter_layout = QVBoxLayout()
        lbl_biaya_dokter = QLabel("Biaya Dokter (Rp):")
        self.txt_biaya_dokter = QLineEdit()
        self.txt_biaya_dokter.setPlaceholderText("0")
        self.txt_biaya_dokter.textChanged.connect(self.calculate_total)
        biaya_dokter_layout.addWidget(lbl_biaya_dokter)
        biaya_dokter_layout.addWidget(self.txt_biaya_dokter)
        biaya_layout.addLayout(biaya_dokter_layout)
        
        # Biaya Obat
        biaya_obat_layout = QVBoxLayout()
        lbl_biaya_obat = QLabel("Biaya Obat (Rp):")
        self.txt_biaya_obat = QLineEdit()
        self.txt_biaya_obat.setPlaceholderText("0")
        self.txt_biaya_obat.textChanged.connect(self.calculate_total)
        biaya_obat_layout.addWidget(lbl_biaya_obat)
        biaya_obat_layout.addWidget(self.txt_biaya_obat)
        biaya_layout.addLayout(biaya_obat_layout)
        
        periksa_layout.addLayout(biaya_layout)
        
        # Total Biaya (readonly, auto-calculate)
        lbl_total = QLabel("TOTAL BIAYA:")
        lbl_total.setFont(QFont('Arial', 11, QFont.Bold))
        self.txt_total = QLineEdit()
        self.txt_total.setReadOnly(True)
        self.txt_total.setStyleSheet("font-size: 14pt; font-weight: bold; color: #f44336;")
        periksa_layout.addWidget(lbl_total)
        periksa_layout.addWidget(self.txt_total)
        
        group_periksa.setLayout(periksa_layout)
        right_layout.addWidget(group_periksa)
        
        # Button Simpan
        self.btn_simpan = QPushButton("💾 SIMPAN PEMERIKSAAN")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setCursor(Qt.PointingHandCursor)
        self.btn_simpan.clicked.connect(self.simpan_pemeriksaan)
        self.btn_simpan.setEnabled(False)  # Disabled sampai ada pendaftaran dipilih
        right_layout.addWidget(self.btn_simpan)
        
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        
        # Set splitter sizes
        splitter.setSizes([500, 700])
        
        main_layout.addWidget(splitter)
        
        self.setLayout(main_layout)
    
    def load_pendaftaran(self):
        """Load daftar pendaftaran yang menunggu"""
        data = Pendaftaran.get_all_menunggu()
        
        self.table_pendaftaran.setRowCount(len(data))
        
        for row, item in enumerate(data):
            self.table_pendaftaran.setItem(row, 0, QTableWidgetItem(str(item['id_pendaftaran'])))
            self.table_pendaftaran.setItem(row, 1, QTableWidgetItem(item['nama']))
            self.table_pendaftaran.setItem(row, 2, QTableWidgetItem(item['nik']))
            self.table_pendaftaran.setItem(row, 3, QTableWidgetItem(item['keluhan'] or '-'))
            self.table_pendaftaran.setItem(row, 4, QTableWidgetItem(str(item['created_at'])))
    
    def on_select_pendaftaran(self):
        """Event ketika pendaftaran dipilih"""
        selected_rows = self.table_pendaftaran.selectedItems()
        
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        
        id_pendaftaran = int(self.table_pendaftaran.item(row, 0).text())
        self.selected_pendaftaran = Pendaftaran.get_by_id(id_pendaftaran)
        
        if self.selected_pendaftaran:
            # Load ke form
            self.txt_id.setText(str(self.selected_pendaftaran['id_pendaftaran']))
            self.txt_nama_pasien.setText(self.selected_pendaftaran['nama'])
            self.txt_nik_pasien.setText(self.selected_pendaftaran['nik'])
            self.txt_keluhan_pasien.setText(self.selected_pendaftaran['keluhan'] or '')
            
            # Clear form input
            self.txt_diagnosa.clear()
            self.txt_resep.clear()
            self.txt_biaya_dokter.setText("0")
            self.txt_biaya_obat.setText("0")
            self.txt_total.setText("Rp 0")
            
            # Enable button simpan
            self.btn_simpan.setEnabled(True)
    
    def calculate_total(self):
        """Calculate total biaya otomatis"""
        try:
            biaya_dokter = float(self.txt_biaya_dokter.text() or 0)
            biaya_obat = float(self.txt_biaya_obat.text() or 0)
            total = biaya_dokter + biaya_obat
            self.txt_total.setText(f"Rp {total:,.0f}")
        except ValueError:
            self.txt_total.setText("Rp 0")
    
    def simpan_pemeriksaan(self):
        """Simpan hasil pemeriksaan"""
        if not self.selected_pendaftaran:
            QMessageBox.warning(self, "Validasi", "Pilih pendaftaran terlebih dahulu!")
            return
        
        diagnosa = self.txt_diagnosa.toPlainText().strip()
        resep = self.txt_resep.toPlainText().strip()
        
        # Validasi
        if not diagnosa:
            QMessageBox.warning(self, "Validasi", "Diagnosa wajib diisi!")
            return
        
        try:
            biaya_dokter = float(self.txt_biaya_dokter.text() or 0)
            biaya_obat = float(self.txt_biaya_obat.text() or 0)
        except ValueError:
            QMessageBox.warning(self, "Validasi", "Biaya harus berupa angka!")
            return
        
        # Konfirmasi
        total = biaya_dokter + biaya_obat
        reply = QMessageBox.question(self, 'Konfirmasi', 
                                    f'Simpan pemeriksaan untuk:\n\n'
                                    f'Pasien: {self.selected_pendaftaran["nama"]}\n'
                                    f'Diagnosa: {diagnosa}\n'
                                    f'Total Biaya: Rp {total:,.0f}\n\n'
                                    f'Lanjutkan?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.No:
            return
        
        # Simpan
        pemeriksaan = Pemeriksaan(
            id_pendaftaran=self.selected_pendaftaran['id_pendaftaran'],
            nik=self.selected_pendaftaran['nik'],
            nip_dokter=self.nip,
            diagnosa=diagnosa,
            resep=resep,
            biaya_dokter=biaya_dokter,
            biaya_obat=biaya_obat
        )
        
        success, message, id_pemeriksaan = pemeriksaan.simpan()
        
        if success:
            QMessageBox.information(self, "Berhasil", 
                                  f"{message}\n\nID Pemeriksaan: {id_pemeriksaan}\n\n"
                                  f"Status pendaftaran otomatis berubah menjadi 'selesai'.")
            
            # Clear form
            self.selected_pendaftaran = None
            self.txt_id.clear()
            self.txt_nama_pasien.clear()
            self.txt_nik_pasien.clear()
            self.txt_keluhan_pasien.clear()
            self.txt_diagnosa.clear()
            self.txt_resep.clear()
            self.txt_biaya_dokter.setText("0")
            self.txt_biaya_obat.setText("0")
            self.txt_total.setText("Rp 0")
            
            # Disable button
            self.btn_simpan.setEnabled(False)
            
            # Reload tabel
            self.load_pendaftaran()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan pemeriksaan!\n{message}")
    
    def open_profil(self):
        """Buka profil dokter"""
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
