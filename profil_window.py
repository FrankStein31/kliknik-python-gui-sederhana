"""
Window Profil - Untuk Dokter dan Pasien
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame, QDesktopWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from dokter import Dokter
from pasien import Pasien


class ProfilDokterWindow(QWidget):
    # Signal untuk logout
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Profil Dokter - Sistem Informasi Klinik")
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
        header = QLabel("👤 Profil Dokter")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #2E86DE;")
        layout.addWidget(header)
        
        # Form frame
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 30px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Fields
        self.nip_input = self.create_field(form_layout, "NIP:")
        self.nama_input = self.create_field(form_layout, "Nama:")
        self.no_tlp_input = self.create_field(form_layout, "No. Telepon:")
        self.alamat_input = self.create_field(form_layout, "Alamat:")
        
        layout.addWidget(form_frame)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_load = QPushButton("🔄 Muat Data")
        btn_load.setMinimumHeight(50)
        btn_load.setStyleSheet(self.get_button_style("#3498DB"))
        btn_load.clicked.connect(self.load_data)
        btn_layout.addWidget(btn_load)
        
        btn_save = QPushButton("💾 Simpan")
        btn_save.setMinimumHeight(50)
        btn_save.setStyleSheet(self.get_button_style("#27AE60"))
        btn_save.clicked.connect(self.save_data)
        btn_layout.addWidget(btn_save)
        
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
        
        # Auto load data
        self.load_data()
    
    def create_field(self, parent_layout, label_text):
        """Helper untuk membuat field"""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 11, QFont.Bold))
        label.setStyleSheet("color: #2C3E50;")
        parent_layout.addWidget(label)
        
        input_field = QLineEdit()
        input_field.setMinimumHeight(45)
        input_field.setFont(QFont("Arial", 11))
        input_field.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                padding: 10px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border-color: #2E86DE;
            }
        """)
        parent_layout.addWidget(input_field)
        
        return input_field
    
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
    
    def load_data(self):
        """Load data dokter berdasarkan username"""
        # Untuk demo, kita gunakan NIP dari input atau username
        # Dalam implementasi real, harus ada relasi admin -> dokter
        data = Dokter.get_all()
        if data:
            # Ambil dokter pertama atau sesuai dengan user
            d = data[0]
            self.nip_input.setText(str(d[0]))
            self.nama_input.setText(str(d[1]))
            self.no_tlp_input.setText(str(d[2]))
            self.alamat_input.setText(str(d[3]))
            QMessageBox.information(self, "Berhasil", "Data berhasil dimuat!")
        else:
            QMessageBox.warning(self, "Info", "Belum ada data profil. Silakan isi dan simpan.")
    
    def save_data(self):
        """Simpan/update data dokter"""
        nip = self.nip_input.text().strip()
        nama = self.nama_input.text().strip()
        no_tlp = self.no_tlp_input.text().strip()
        alamat = self.alamat_input.text().strip()
        
        if not nip or not nama:
            QMessageBox.warning(self, "Peringatan", "NIP dan Nama harus diisi!")
            return
        
        # Cek apakah sudah ada
        existing = Dokter.get_by_nip(nip)
        
        if existing:
            # Update
            result = Dokter.update(nip, nama, no_tlp, alamat)
        else:
            # Insert
            dokter = Dokter(nip, nama, no_tlp, alamat)
            result = dokter.insert()
        
        if result is True:
            QMessageBox.information(self, "Berhasil", "Data profil berhasil disimpan!")
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan:\n{result}")
    
    def resize_window(self):
        """Resize window agar fit dengan screen"""
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.6)  # 60% dari lebar layar
        height = int(screen.height() * 0.7)  # 70% dari tinggi layar
        self.resize(width, height)
    
    def center_window(self):
        """Posisikan window di tengah layar"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def go_back(self):
        """Kembali ke menu utama"""
        from pemeriksaan_window import PemeriksaanWindow
        self.main_window = PemeriksaanWindow(self.user_data)
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
                print("DEBUG - Calling app.on_logout() from ProfilDokterWindow")
                app.on_logout()
            else:
                # Fallback jika MainApp tidak ada
                self.logout_signal.emit()


class ProfilPasienWindow(QWidget):
    # Signal untuk logout
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Profil Pasien - Sistem Informasi Klinik")
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
        header = QLabel("👤 Profil Pasien")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #2E86DE;")
        layout.addWidget(header)
        
        # Form frame
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 30px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Fields
        self.nik_input = self.create_field(form_layout, "NIK:")
        self.nama_input = self.create_field(form_layout, "Nama:")
        self.no_tlp_input = self.create_field(form_layout, "No. Telepon:")
        self.alamat_input = self.create_field(form_layout, "Alamat:")
        
        # Password fields
        password_label = QLabel("🔒 Ubah Password Login")
        password_label.setFont(QFont("Arial", 12, QFont.Bold))
        password_label.setStyleSheet("color: #E74C3C; margin-top: 10px;")
        form_layout.addWidget(password_label)
        
        self.password_input = self.create_field(form_layout, "Password Baru (kosongkan jika tidak diubah):")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(form_frame)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        btn_load = QPushButton("🔄 Muat Data")
        btn_load.setMinimumHeight(50)
        btn_load.setStyleSheet(self.get_button_style("#3498DB"))
        btn_load.clicked.connect(self.load_data)
        btn_layout.addWidget(btn_load)
        
        btn_save = QPushButton("💾 Simpan")
        btn_save.setMinimumHeight(50)
        btn_save.setStyleSheet(self.get_button_style("#27AE60"))
        btn_save.clicked.connect(self.save_data)
        btn_layout.addWidget(btn_save)
        
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
        
        # Auto load data
        self.load_data()
    
    def create_field(self, parent_layout, label_text):
        """Helper untuk membuat field"""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 11, QFont.Bold))
        label.setStyleSheet("color: #2C3E50;")
        parent_layout.addWidget(label)
        
        input_field = QLineEdit()
        input_field.setMinimumHeight(45)
        input_field.setFont(QFont("Arial", 11))
        input_field.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                padding: 10px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border-color: #2E86DE;
            }
        """)
        parent_layout.addWidget(input_field)
        
        return input_field
    
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
    
    def load_data(self):
        """Load data pasien"""
        data = Pasien.get_all()
        if data:
            # Ambil pasien pertama atau sesuai dengan user
            p = data[0]
            self.nik_input.setText(str(p[0]))
            self.nama_input.setText(str(p[1]))
            self.no_tlp_input.setText(str(p[2]))
            self.alamat_input.setText(str(p[3]))
            QMessageBox.information(self, "Berhasil", "Data berhasil dimuat!")
        else:
            QMessageBox.warning(self, "Info", "Belum ada data profil. Silakan isi dan simpan.")
    
    def save_data(self):
        """Simpan/update data pasien"""
        nik = self.nik_input.text().strip()
        nama = self.nama_input.text().strip()
        no_tlp = self.no_tlp_input.text().strip()
        alamat = self.alamat_input.text().strip()
        new_password = self.password_input.text().strip()
        
        if not nik or not nama:
            QMessageBox.warning(self, "Peringatan", "NIK dan Nama harus diisi!")
            return
        
        if len(nik) != 16:
            QMessageBox.warning(self, "Peringatan", "NIK harus 16 digit!")
            return
        
        # Cek apakah sudah ada
        existing = Pasien.get_by_nik(nik)
        
        if existing:
            # Update
            result = Pasien.update(nik, nama, no_tlp, alamat)
        else:
            # Insert
            pasien = Pasien(nik, nama, no_tlp, alamat)
            result = pasien.insert()
        
        # Update password jika diisi
        password_updated = False
        if new_password:
            from admin import Admin
            password_result = Admin.update_password(self.user_data["username"], new_password)
            if password_result is True:
                password_updated = True
            else:
                QMessageBox.warning(self, "Peringatan", f"Gagal update password:\n{password_result}")
        
        if result is True:
            msg = "Data profil berhasil disimpan!"
            if password_updated:
                msg += "\n\nPassword login juga berhasil diubah!"
            QMessageBox.information(self, "Berhasil", msg)
            self.password_input.clear()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan:\n{result}")
    
    def resize_window(self):
        """Resize window agar fit dengan screen"""
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.6)  # 60% dari lebar layar
        height = int(screen.height() * 0.7)  # 70% dari tinggi layar
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
                print("DEBUG - Calling app.on_logout() from ProfilPasienWindow")
                app.on_logout()
            else:
                # Fallback jika MainApp tidak ada
                self.logout_signal.emit()
