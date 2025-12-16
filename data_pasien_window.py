"""
Window Data Pasien - Untuk Dokter CRUD Data Pasien
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QFrame, QTableWidget, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from pasien import Pasien
from admin import Admin


class DataPasienWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.selected_nik = None
        
        self.setWindowTitle("Data Pasien - Dokter")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background: #F5F7FA;")
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header = QLabel("👥 Data Pasien - CRUD")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #2E86DE;")
        main_layout.addWidget(header)
        
        # Content Layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Left Panel - Form
        form_frame = QFrame()
        form_frame.setMaximumWidth(400)
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Form Title
        form_title = QLabel("📝 Form Pasien")
        form_title.setFont(QFont("Arial", 14, QFont.Bold))
        form_title.setStyleSheet("color: #2E86DE;")
        form_layout.addWidget(form_title)
        
        # NIK
        self.nik_label = QLabel("NIK (16 digit):")
        self.nik_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(self.nik_label)
        
        self.nik_input = QLineEdit()
        self.nik_input.setPlaceholderText("Masukkan NIK 16 digit")
        self.nik_input.setMaxLength(16)
        self.nik_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.nik_input)
        
        # Nama
        self.nama_label = QLabel("Nama Lengkap:")
        self.nama_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(self.nama_label)
        
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Masukkan nama lengkap")
        self.nama_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.nama_input)
        
        # No Telepon
        self.telp_label = QLabel("No. Telepon:")
        self.telp_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(self.telp_label)
        
        self.telp_input = QLineEdit()
        self.telp_input.setPlaceholderText("Contoh: 081234567890")
        self.telp_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.telp_input)
        
        # Alamat
        self.alamat_label = QLabel("Alamat:")
        self.alamat_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(self.alamat_label)
        
        self.alamat_input = QTextEdit()
        self.alamat_input.setPlaceholderText("Masukkan alamat lengkap")
        self.alamat_input.setMaximumHeight(80)
        self.alamat_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.alamat_input)
        
        # Password Default (untuk registrasi admin)
        self.password_label = QLabel("Password Login (Default):")
        self.password_label.setFont(QFont("Arial", 10, QFont.Bold))
        form_layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password untuk login (default: 123)")
        self.password_input.setText("123")
        self.password_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.password_input)
        
        # Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_tambah = QPushButton("➕ Tambah Pasien")
        self.btn_tambah.setMinimumHeight(45)
        self.btn_tambah.setStyleSheet(self.get_button_style("#27AE60"))
        self.btn_tambah.clicked.connect(self.tambah_pasien)
        btn_layout.addWidget(self.btn_tambah)
        
        self.btn_update = QPushButton("✏️ Update Pasien")
        self.btn_update.setMinimumHeight(45)
        self.btn_update.setStyleSheet(self.get_button_style("#F39C12"))
        self.btn_update.clicked.connect(self.update_pasien)
        btn_layout.addWidget(self.btn_update)
        
        self.btn_hapus = QPushButton("🗑️ Hapus Pasien")
        self.btn_hapus.setMinimumHeight(45)
        self.btn_hapus.setStyleSheet(self.get_button_style("#E74C3C"))
        self.btn_hapus.clicked.connect(self.hapus_pasien)
        btn_layout.addWidget(self.btn_hapus)
        
        self.btn_clear = QPushButton("🔄 Bersihkan")
        self.btn_clear.setMinimumHeight(45)
        self.btn_clear.setStyleSheet(self.get_button_style("#95A5A6"))
        self.btn_clear.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.btn_clear)
        
        form_layout.addLayout(btn_layout)
        
        # Back Button
        self.btn_back = QPushButton("⬅ Kembali")
        self.btn_back.setMinimumHeight(45)
        self.btn_back.setStyleSheet(self.get_button_style("#34495E"))
        self.btn_back.clicked.connect(self.go_back)
        form_layout.addWidget(self.btn_back)
        
        content_layout.addWidget(form_frame)
        
        # Right Panel - Table
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
        
        # Table Title
        table_title = QLabel("📊 Daftar Pasien Terdaftar")
        table_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_title.setStyleSheet("color: #2E86DE;")
        table_layout.addWidget(table_title)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cari berdasarkan NIK atau Nama...")
        self.search_input.setStyleSheet(self.get_input_style())
        self.search_input.textChanged.connect(self.search_data)
        table_layout.addWidget(self.search_input)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["NIK", "Nama", "No. Telepon", "Alamat"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
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
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.table.itemSelectionChanged.connect(self.on_table_select)
        table_layout.addWidget(self.table)
        
        content_layout.addWidget(table_frame)
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
    
    def get_input_style(self):
        """Style untuk input"""
        return """
            QLineEdit, QTextEdit {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                padding: 10px;
                color: #2C3E50;
                font-size: 10pt;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #2E86DE;
            }
        """
    
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
        """Load data pasien ke tabel"""
        data = Pasien.get_all()
        self.table.setRowCount(0)
        
        for row_num, row_data in enumerate(data):
            self.table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_num, col_num, item)
    
    def on_table_select(self):
        """Ketika baris dipilih"""
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            self.selected_nik = self.table.item(row, 0).text()
            self.nik_input.setText(self.table.item(row, 0).text())
            self.nama_input.setText(self.table.item(row, 1).text())
            self.telp_input.setText(self.table.item(row, 2).text())
            self.alamat_input.setText(self.table.item(row, 3).text())
            self.nik_input.setReadOnly(True)  # NIK tidak bisa diubah saat update
    
    def tambah_pasien(self):
        """Tambah pasien baru"""
        nik = self.nik_input.text().strip()
        nama = self.nama_input.text().strip()
        no_tlp = self.telp_input.text().strip()
        alamat = self.alamat_input.toPlainText().strip()
        password = self.password_input.text().strip()
        
        # Validasi
        if not nik or len(nik) != 16:
            QMessageBox.warning(self, "Peringatan", "NIK harus 16 digit!")
            return
        
        if not nama:
            QMessageBox.warning(self, "Peringatan", "Nama harus diisi!")
            return
        
        # Cek apakah NIK sudah ada
        if Pasien.get_by_nik(nik):
            QMessageBox.warning(self, "Peringatan", "NIK sudah terdaftar!")
            return
        
        # Insert ke table pasien
        pasien = Pasien(nik, nama, no_tlp, alamat)
        result = pasien.insert()
        
        if result is True:
            # Buat akun admin untuk login
            username = f"pasien_{nik[-6:]}"  # Username: pasien_[6 digit terakhir NIK]
            admin_result = Admin.create_user(username, password, "pasien")
            
            if admin_result is True:
                QMessageBox.information(
                    self, 
                    "Berhasil", 
                    f"Pasien berhasil ditambahkan!\n\n"
                    f"Username: {username}\n"
                    f"Password: {password}\n\n"
                    f"Pasien dapat login dengan kredensial di atas."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Berhasil Sebagian",
                    f"Data pasien tersimpan, tapi gagal membuat akun login:\n{admin_result}"
                )
            
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menambahkan pasien:\n{result}")
    
    def update_pasien(self):
        """Update data pasien"""
        if not self.selected_nik:
            QMessageBox.warning(self, "Peringatan", "Pilih pasien yang akan diupdate!")
            return
        
        nik = self.nik_input.text().strip()
        nama = self.nama_input.text().strip()
        no_tlp = self.telp_input.text().strip()
        alamat = self.alamat_input.toPlainText().strip()
        
        if not nama:
            QMessageBox.warning(self, "Peringatan", "Nama harus diisi!")
            return
        
        result = Pasien.update(nik, nama, no_tlp, alamat)
        
        if result is True:
            QMessageBox.information(self, "Berhasil", "Data pasien berhasil diupdate!")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal update:\n{result}")
    
    def hapus_pasien(self):
        """Hapus pasien"""
        if not self.selected_nik:
            QMessageBox.warning(self, "Peringatan", "Pilih pasien yang akan dihapus!")
            return
        
        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin menghapus pasien ini?\n\n"
            "Data pendaftaran dan pemeriksaan terkait juga akan terhapus!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = Pasien.delete(self.selected_nik)
            
            if result is True:
                QMessageBox.information(self, "Berhasil", "Data pasien berhasil dihapus!")
                self.clear_form()
                self.load_data()
            else:
                QMessageBox.critical(self, "Gagal", f"Gagal hapus:\n{result}")
    
    def clear_form(self):
        """Bersihkan form"""
        self.nik_input.clear()
        self.nama_input.clear()
        self.telp_input.clear()
        self.alamat_input.clear()
        self.password_input.setText("123")
        self.selected_nik = None
        self.nik_input.setReadOnly(False)
    
    def search_data(self):
        """Search data pasien"""
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
        """Kembali ke menu pemeriksaan"""
        from pemeriksaan_window import PemeriksaanWindow
        self.main_window = PemeriksaanWindow(self.user_data)
        self.main_window.show()
        self.close()
