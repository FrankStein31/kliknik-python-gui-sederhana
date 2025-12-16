"""
Window Data Dokter - Untuk Pasien Lihat Data Dokter
"""
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFrame, QTableWidget, QHeaderView
from PyQt5.QtGui import QFont
from dokter import Dokter


class DataDokterWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        
        self.setWindowTitle("Data Dokter")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background: #F5F7FA;")
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("👨‍⚕️ Daftar Dokter")
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
        
        # Table Frame
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setSpacing(15)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari berdasarkan NIP atau Nama Dokter...")
        self.search_input.setMinimumHeight(45)
        self.search_input.setStyleSheet("""
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
        """)
        self.search_input.textChanged.connect(self.search_data)
        table_layout.addWidget(self.search_input)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["NIP", "Nama Dokter", "No. Telepon", "Alamat"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
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
        """)
        table_layout.addWidget(self.table)
        
        main_layout.addWidget(table_frame)
        self.setLayout(main_layout)
    
    def get_button_style(self, color):
        """Style untuk button"""
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
    
    def load_data(self):
        """Load data dokter ke tabel"""
        data = Dokter.get_all()
        self.table.setRowCount(0)
        
        if not data:
            self.table.insertRow(0)
            item = QTableWidgetItem("Belum ada data dokter")
            item.setFont(QFont("Arial", 11))
            self.table.setItem(0, 0, item)
            self.table.setSpan(0, 0, 1, 4)
            return
        
        for row_num, row_data in enumerate(data):
            self.table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFont(QFont("Arial", 10))
                self.table.setItem(row_num, col_num, item)
    
    def search_data(self):
        """Search data dokter"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)
    
    def go_back(self):
        """Kembali ke menu pendaftaran"""
        from pendaftaran_window import PendaftaranWindow
        self.main_window = PendaftaranWindow(self.user_data)
        self.main_window.show()
        self.close()
