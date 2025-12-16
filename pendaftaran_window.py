"""
Window Pendaftaran Pasien - Menghubungkan UI Pendaftaran dengan Backend
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QDesktopWidget, QPushButton
from PyQt5.QtCore import QDate, Qt, pyqtSignal
from ui_pendaftaran import Ui_FormDaftarPasien
from daftar import Pendaftaran
from pasien import Pasien
from dokter import Dokter


class PendaftaranWindow(QWidget):
    # Signal untuk logout
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.ui = Ui_FormDaftarPasien()
        self.ui.setupUi(self)
        self.user_data = user_data
        
        # Set window properties
        self.setWindowTitle("Pendaftaran Pasien - Sistem Informasi Klinik")
        
        # Auto-resize window - LEBIH BESAR
        self.resize_window()
        
        # Center window
        self.center_window()
        
        # Maximize window agar semua elemen terlihat
        self.showMaximized()
        
        # Set user info di sidebar
        self.ui.lblUserName.setText(user_data["username"])
        self.ui.lblUserRole.setText(user_data["role"].title())
        
        # Tambah tombol logout ke sidebar
        self.add_logout_button()
        
        # Set default date
        self.ui.dateTglLahir.setDate(QDate.currentDate())
        
        # Pastikan tombol daftar visible dan accessible
        self.ui.btnDaftar.setVisible(True)
        self.ui.btnBatal.setVisible(True)
        self.ui.btnDaftar.setEnabled(True)
        self.ui.btnBatal.setEnabled(True)
        
        # Force update layout
        self.ui.btnDaftar.raise_()
        self.ui.btnBatal.raise_()
        
        # Connect buttons
        self.ui.btnDaftar.clicked.connect(self.daftar_pasien)
        self.ui.btnBatal.clicked.connect(self.clear_form)
        self.ui.btnMenuProfil.clicked.connect(self.show_profil)
        self.ui.btnMenuPendaftaran.clicked.connect(self.show_pendaftaran)
        
        # Ubah menu profil menjadi multi menu
        self.ui.btnMenuProfil.setText("📋 Menu Lainnya")
        self.ui.btnMenuProfil.clicked.disconnect()
        self.ui.btnMenuProfil.clicked.connect(self.show_menu_lainnya)
    
    def resize_window(self):
        """Resize window agar fit dengan screen dan semua elemen terlihat"""
        screen = QDesktopWidget().screenGeometry()
        # Gunakan ukuran yang lebih besar atau maksimal
        width = max(int(screen.width() * 0.9), 1200)  # Min 1200px atau 90% layar
        height = max(int(screen.height() * 0.85), 700)  # Min 700px atau 85% layar
        self.resize(width, height)
    
    def center_window(self):
        """Posisikan window di tengah layar"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def add_logout_button(self):
        """Tambah tombol logout di sidebar"""
        btnLogout = QPushButton("🚪 Logout")
        btnLogout.setMinimumSize(0, 50)
        btnLogout.setStyleSheet("""
            QPushButton {
                background: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
                padding-left: 15px;
                font-weight: bold;
                font-size: 11pt;
                margin: 15px;
            }
            QPushButton:hover {
                background: #C0392B;
            }
            QPushButton:pressed {
                background: #A93226;
            }
        """)
        btnLogout.clicked.connect(self.logout)
        
        # Tambahkan ke layout sidebar (sebelum spacer terakhir)
        self.ui.sidebarLayout.insertWidget(self.ui.sidebarLayout.count() - 1, btnLogout)
        
    def daftar_pasien(self):
        """Proses pendaftaran pasien"""
        # Ambil data dari form
        nik = self.ui.txtNIK.text().strip()
        nama = self.ui.txtNama.text().strip()
        tgl_lahir = self.ui.dateTglLahir.date().toString("yyyy-MM-dd")
        jk_index = self.ui.cmbJenisKelamin.currentIndex()
        jk = self.ui.cmbJenisKelamin.currentText()
        no_telp = self.ui.txtNoTelp.text().strip()
        keluhan = self.ui.txtKeluhan.toPlainText().strip()
        
        # Validasi input
        if not nik or len(nik) != 16:
            QMessageBox.warning(self, "Peringatan", "NIK harus 16 digit!")
            return
        
        if not nama:
            QMessageBox.warning(self, "Peringatan", "Nama harus diisi!")
            return
        
        if jk_index == 0:
            QMessageBox.warning(self, "Peringatan", "Pilih jenis kelamin!")
            return
        
        if not no_telp:
            QMessageBox.warning(self, "Peringatan", "Nomor telepon harus diisi!")
            return
        
        if not keluhan:
            QMessageBox.warning(self, "Peringatan", "Keluhan harus diisi!")
            return
        
        # Simpan pendaftaran
        pendaftaran = Pendaftaran(nik, nama, tgl_lahir, jk, no_telp, keluhan)
        result = pendaftaran.insert_pendaftaran()
        
        if result is True:
            QMessageBox.information(
                self, 
                "Berhasil", 
                "Pendaftaran berhasil disimpan!\n\nSilakan menunggu untuk dipanggil."
            )
            self.clear_form()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan pendaftaran:\n{result}")
    
    def clear_form(self):
        """Bersihkan form"""
        self.ui.txtNIK.clear()
        self.ui.txtNama.clear()
        self.ui.dateTglLahir.setDate(QDate.currentDate())
        self.ui.cmbJenisKelamin.setCurrentIndex(0)
        self.ui.txtNoTelp.clear()
        self.ui.txtKeluhan.clear()
        self.ui.txtNIK.setFocus()
    
    def show_profil(self):
        """Tampilkan profil pasien"""
        from profil_window import ProfilPasienWindow
        self.profil_window = ProfilPasienWindow(self.user_data)
        # Connect logout signal dari profil window ke parent logout signal
        if hasattr(self.profil_window, 'logout_signal') and hasattr(self, 'logout_signal'):
            self.profil_window.logout_signal.connect(self.logout_signal.emit)
        self.profil_window.show()
        self.close()
    
    def show_menu_lainnya(self):
        """Tampilkan menu lainnya"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Menu Lainnya")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        btn_profil = QPushButton("👤 Profil Saya")
        btn_profil.setMinimumHeight(50)
        btn_profil.setStyleSheet("""
            QPushButton {
                background: #3498DB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #5DADE2;
            }
        """)
        btn_profil.clicked.connect(lambda: [dialog.close(), self.show_profil()])
        layout.addWidget(btn_profil)
        
        btn_dokter = QPushButton("👨‍⚕️ Lihat Data Dokter")
        btn_dokter.setMinimumHeight(50)
        btn_dokter.setStyleSheet("""
            QPushButton {
                background: #27AE60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #2ECC71;
            }
        """)
        btn_dokter.clicked.connect(lambda: [dialog.close(), self.show_data_dokter()])
        layout.addWidget(btn_dokter)
        
        btn_hasil = QPushButton("📋 Lihat Hasil Periksa")
        btn_hasil.setMinimumHeight(50)
        btn_hasil.setStyleSheet("""
            QPushButton {
                background: #E67E22;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #F39C12;
            }
        """)
        btn_hasil.clicked.connect(lambda: [dialog.close(), self.show_hasil_periksa()])
        layout.addWidget(btn_hasil)
        
        btn_close = QPushButton("❌ Tutup")
        btn_close.setMinimumHeight(50)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #95A5A6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #BDC3C7;
            }
        """)
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def show_data_dokter(self):
        """Tampilkan data dokter"""
        from data_dokter_window import DataDokterWindow
        self.dokter_window = DataDokterWindow(self.user_data)
        self.dokter_window.show()
        self.close()
    
    def show_hasil_periksa(self):
        """Tampilkan hasil periksa dan data pendaftaran"""
        from data_pendaftaran_pasien_window import DataPendaftaranPasienWindow
        self.hasil_window = DataPendaftaranPasienWindow(self.user_data)
        # Connect logout signal dari hasil window ke parent
        if hasattr(self.hasil_window, 'logout_signal'):
            self.hasil_window.logout_signal.connect(self.logout_signal.emit)
        self.hasil_window.show()
        self.close()
    
    def show_pendaftaran(self):
        """Refresh pendaftaran"""
        pass
    
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
                print("DEBUG - Calling app.on_logout() from PendaftaranWindow")
                app.on_logout()
            else:
                # Fallback jika MainApp tidak ada
                self.logout_signal.emit()
