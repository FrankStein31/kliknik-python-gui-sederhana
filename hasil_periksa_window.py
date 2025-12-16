"""
Window Hasil Periksa - Untuk Pasien Lihat Hasil Pemeriksaan & Pendaftaran
"""
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFrame, QTableWidget, QHeaderView, QTabWidget
from PyQt5.QtGui import QFont
from periksa import Pemeriksaan
from daftar import Pendaftaran


class HasilPeriksaWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        self.setWindowTitle("Hasil Periksa & Pendaftaran")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background: #F5F7FA;")
        
        self.init_ui()
        self.load_all_data()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("📋 Riwayat Pendaftaran & Hasil Periksa")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #2E86DE;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        # Back Button
        self.btn_back = QPushButton("⬅ Kembali")
        self.btn_back.setMinimumHeight(45)
        self.btn_back.setMinimumWidth(150)
        self.btn_back.setStyleSheet(self.get_button_style("#34495E"))
        self.btn_back.clicked.connect(self.go_back)
        header_layout.addWidget(self.btn_back)
        
        main_layout.addLayout(header_layout)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #E8E8E8;
                color: #2C3E50;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QTabBar::tab:selected {
                background: #2E86DE;
                color: white;
            }
        """)
        
        # Tab 1: Pendaftaran
        self.tab_pendaftaran = QWidget()
        self.init_tab_pendaftaran()
        self.tabs.addTab(self.tab_pendaftaran, "📝 Data Pendaftaran")
        
        # Tab 2: Hasil Periksa
        self.tab_periksa = QWidget()
        self.init_tab_periksa()
        self.tabs.addTab(self.tab_periksa, "💊 Hasil Pemeriksaan")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
    
    def init_tab_pendaftaran(self):
        """Tab pendaftaran"""
        layout = QVBoxLayout(self.tab_pendaftaran)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Search
        self.search_pendaftaran = QLineEdit()
        self.search_pendaftaran.setPlaceholderText("🔍 Cari pendaftaran...")
        self.search_pendaftaran.setMinimumHeight(45)
        self.search_pendaftaran.setStyleSheet(self.get_input_style())
        self.search_pendaftaran.textChanged.connect(lambda: self.search_table(self.table_pendaftaran, self.search_pendaftaran.text()))
        layout.addWidget(self.search_pendaftaran)
        
        # Table
        self.table_pendaftaran = QTableWidget()
        self.table_pendaftaran.setColumnCount(7)
        self.table_pendaftaran.setHorizontalHeaderLabels([
            "ID", "NIK", "Nama", "Tanggal Lahir", "JK", "No. Telp", "Keluhan"
        ])
        self.table_pendaftaran.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_pendaftaran.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_pendaftaran.setAlternatingRowColors(True)
        self.table_pendaftaran.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_pendaftaran.setStyleSheet(self.get_table_style())
        layout.addWidget(self.table_pendaftaran)
    
    def init_tab_periksa(self):
        """Tab hasil periksa"""
        layout = QVBoxLayout(self.tab_periksa)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Search
        self.search_periksa = QLineEdit()
        self.search_periksa.setPlaceholderText("🔍 Cari hasil periksa...")
        self.search_periksa.setMinimumHeight(45)
        self.search_periksa.setStyleSheet(self.get_input_style())
        self.search_periksa.textChanged.connect(lambda: self.search_table(self.table_periksa, self.search_periksa.text()))
        layout.addWidget(self.search_periksa)
        
        # Table
        self.table_periksa = QTableWidget()
        self.table_periksa.setColumnCount(7)
        self.table_periksa.setHorizontalHeaderLabels([
            "ID Periksa", "NIK", "Nama", "Diagnosa", "Resep", "Jumlah Obat", "Total Biaya"
        ])
        self.table_periksa.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_periksa.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_periksa.setAlternatingRowColors(True)
        self.table_periksa.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_periksa.setStyleSheet(self.get_table_style())
        layout.addWidget(self.table_periksa)
    
    def get_input_style(self):
        """Style input"""
        return """
            QLineEdit {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                padding: 10px;
                color: #2C3E50;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #2E86DE;
            }
        """
    
    def get_table_style(self):
        """Style table"""
        return """
            QTableWidget {
                background: white;
                border: none;
                gridline-color: #E8E8E8;
            }
            QHeaderView::section {
                background: #2E86DE;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 11pt;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """
    
    def get_button_style(self, color):
        """Style button"""
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
        """Load semua data"""
        self.load_pendaftaran()
        self.load_periksa()
    
    def load_pendaftaran(self):
        """Load data pendaftaran"""
        data = Pendaftaran.get_all()
        self.table_pendaftaran.setRowCount(0)
        
        if not data:
            self.table_pendaftaran.insertRow(0)
            item = QTableWidgetItem("Belum ada data pendaftaran")
            item.setFont(QFont("Arial", 11))
            self.table_pendaftaran.setItem(0, 0, item)
            self.table_pendaftaran.setSpan(0, 0, 1, 7)
            return
        
        for row_num, row_data in enumerate(data):
            self.table_pendaftaran.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFont(QFont("Arial", 10))
                self.table_pendaftaran.setItem(row_num, col_num, item)
    
    def load_periksa(self):
        """Load data pemeriksaan"""
        data = Pemeriksaan.get_all()
        self.table_periksa.setRowCount(0)
        
        if not data:
            self.table_periksa.insertRow(0)
            item = QTableWidgetItem("Belum ada data pemeriksaan")
            item.setFont(QFont("Arial", 11))
            self.table_periksa.setItem(0, 0, item)
            self.table_periksa.setSpan(0, 0, 1, 7)
            return
        
        for row_num, row_data in enumerate(data):
            self.table_periksa.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                # Format biaya
                if col_num == 6:  # Total biaya
                    item = QTableWidgetItem(f"Rp {float(col_data):,.0f}")
                else:
                    item = QTableWidgetItem(str(col_data))
                item.setFont(QFont("Arial", 10))
                self.table_periksa.setItem(row_num, col_num, item)
    
    def search_table(self, table, search_text):
        """Search di tabel"""
        search_text = search_text.lower()
        
        for row in range(table.rowCount()):
            match = False
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            table.setRowHidden(row, not match)
    
    def go_back(self):
        """Kembali ke menu pendaftaran"""
        from pendaftaran_window import PendaftaranWindow
        self.main_window = PendaftaranWindow(self.user_data)
        self.main_window.show()
        self.close()
