"""
Window Data Pendaftaran & Hasil Periksa untuk Pasien
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QDesktopWidget, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from daftar import Pendaftaran
from periksa import Pemeriksaan


class DataPendaftaranPasienWindow(QWidget):
    # Signal untuk logout
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Data Pendaftaran & Hasil Periksa - Sistem Informasi Klinik")
        self.setStyleSheet("background: #F5F7FA;")
        
        # Auto-resize window
        self.resize_window()
        
        # Center window
        self.center_window()
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("📋 Data Pendaftaran & Hasil Pemeriksaan")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #2E86DE;")
        header_layout.addWidget(header)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Info section
        info_label = QLabel("Berikut adalah riwayat pendaftaran dan hasil pemeriksaan Anda:")
        info_label.setFont(QFont("Arial", 11))
        info_label.setStyleSheet("color: #7F8C8D; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Table Pendaftaran
        pendaftaran_label = QLabel("📝 Riwayat Pendaftaran")
        pendaftaran_label.setFont(QFont("Arial", 14, QFont.Bold))
        pendaftaran_label.setStyleSheet("color: #27AE60; margin-top: 10px;")
        layout.addWidget(pendaftaran_label)
        
        self.table_pendaftaran = QTableWidget()
        self.table_pendaftaran.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                gridline-color: #E8E8E8;
            }
            QHeaderView::section {
                background: #27AE60;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.table_pendaftaran.setAlternatingRowColors(True)
        self.table_pendaftaran.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table_pendaftaran)
        
        # Table Pemeriksaan
        pemeriksaan_label = QLabel("🏥 Hasil Pemeriksaan")
        pemeriksaan_label.setFont(QFont("Arial", 14, QFont.Bold))
        pemeriksaan_label.setStyleSheet("color: #E74C3C; margin-top: 20px;")
        layout.addWidget(pemeriksaan_label)
        
        self.table_pemeriksaan = QTableWidget()
        self.table_pemeriksaan.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                gridline-color: #E8E8E8;
            }
            QHeaderView::section {
                background: #E74C3C;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.table_pemeriksaan.setAlternatingRowColors(True)
        self.table_pemeriksaan.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table_pemeriksaan)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_refresh = QPushButton("🔄 Refresh Data")
        btn_refresh.setMinimumHeight(50)
        btn_refresh.setStyleSheet(self.get_button_style("#3498DB"))
        btn_refresh.clicked.connect(self.load_all_data)
        btn_layout.addWidget(btn_refresh)
        
        btn_back = QPushButton("⬅ Kembali")
        btn_back.setMinimumHeight(50)
        btn_back.setStyleSheet(self.get_button_style("#95A5A6"))
        btn_back.clicked.connect(self.go_back)
        btn_layout.addWidget(btn_back)
        
        btn_logout = QPushButton("🚪 Logout")
        btn_logout.setMinimumHeight(50)
        btn_logout.setStyleSheet(self.get_button_style("#E74C3C"))
        btn_logout.clicked.connect(self.logout)
        btn_layout.addWidget(btn_logout)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Load data
        self.load_all_data()
    
    def get_button_style(self, color):
        """Helper untuk style button"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 11pt;
            }}
            QPushButton:hover {{
                background: {color}dd;
            }}
        """
    
    def load_all_data(self):
        """Load semua data pendaftaran dan pemeriksaan"""
        self.load_pendaftaran()
        self.load_pemeriksaan()
    
    def load_pendaftaran(self):
        """Load data pendaftaran"""
        data = Pendaftaran.get_all()
        
        # Setup table
        if data:
            self.table_pendaftaran.setColumnCount(6)
            self.table_pendaftaran.setHorizontalHeaderLabels([
                "NIK", "Nama", "Tgl Lahir", "Jenis Kelamin", "No. Telp", "Keluhan"
            ])
        
        self.table_pendaftaran.setRowCount(0)
        
        for row_num, row_data in enumerate(data):
            self.table_pendaftaran.insertRow(row_num)
            
            for col_num in range(min(len(row_data), self.table_pendaftaran.columnCount())):
                item = QTableWidgetItem(str(row_data[col_num]))
                self.table_pendaftaran.setItem(row_num, col_num, item)
        
        # Auto resize
        self.table_pendaftaran.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pendaftaran.resizeColumnsToContents()
    
    def load_pemeriksaan(self):
        """Load data pemeriksaan"""
        try:
            data = Pemeriksaan.get_all_with_name()
        except:
            data = Pemeriksaan.get_all()
        
        # Setup table
        if data and len(data) > 0:
            num_cols = len(data[0])
            self.table_pemeriksaan.setColumnCount(num_cols)
            
            if num_cols >= 7:
                self.table_pemeriksaan.setHorizontalHeaderLabels([
                    "ID", "NIK", "Nama", "Diagnosa", "Resep", "Jml Obat", "Total Biaya"
                ])
            else:
                self.table_pemeriksaan.setHorizontalHeaderLabels([
                    "ID", "NIK", "Diagnosa", "Resep", "Jml Obat", "Total Biaya"
                ])
        
        self.table_pemeriksaan.setRowCount(0)
        
        for row_num, row_data in enumerate(data):
            self.table_pemeriksaan.insertRow(row_num)
            
            for col_num in range(min(len(row_data), self.table_pemeriksaan.columnCount())):
                item = QTableWidgetItem(str(row_data[col_num]))
                self.table_pemeriksaan.setItem(row_num, col_num, item)
        
        # Auto resize
        self.table_pemeriksaan.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pemeriksaan.resizeColumnsToContents()
    
    def resize_window(self):
        """Resize window agar fit dengan screen"""
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.8)  # 80% dari lebar layar
        height = int(screen.height() * 0.8)  # 80% dari tinggi layar
        self.resize(width, height)
    
    def center_window(self):
        """Posisikan window di tengah layar"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def go_back(self):
        """Kembali ke menu utama"""
        from pendaftaran_window import PendaftaranWindow
        self.main_window = PendaftaranWindow(self.user_data)
        self.main_window.show()
        self.close()
    
    def logout(self):
        """Logout dan kembali ke login"""
        reply = QMessageBox.question(
            self,
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Gunakan MainApp singleton untuk handle logout
            from main import MainApp
            app = MainApp.get_instance()
            if app:
                print("DEBUG - Calling app.on_logout() from DataPendaftaranPasienWindow")
                app.on_logout()
            else:
                # Fallback jika MainApp tidak ada
                self.logout_signal.emit()
