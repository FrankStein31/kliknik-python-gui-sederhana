"""
Window Pemeriksaan - Menghubungkan UI Pemeriksaan dengan Backend
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QDesktopWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from ui_pemeriksaan import Ui_FormPemeriksaan
from periksa import Pemeriksaan
from daftar import Pendaftaran


class PemeriksaanWindow(QWidget):
    # Signal untuk logout
    logout_signal = pyqtSignal()
    
    def __init__(self, user_data):
        super().__init__()
        self.ui = Ui_FormPemeriksaan()
        self.ui.setupUi(self)
        self.user_data = user_data
        self.selected_id = None
        
        # Set window properties
        self.setWindowTitle("Pemeriksaan Pasien - Sistem Informasi Klinik")
        
        # Auto-resize window
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
        
        # Connect buttons
        self.ui.btnTambah.clicked.connect(self.tambah_pemeriksaan)
        self.ui.btnUpdate.clicked.connect(self.update_pemeriksaan)
        self.ui.btnHapus.clicked.connect(self.hapus_pemeriksaan)
        self.ui.btnBersih.clicked.connect(self.clear_form)
        self.ui.btnMenuProfil.clicked.connect(self.show_menu_dokter)
        self.ui.btnMenuPemeriksaan.clicked.connect(self.show_pemeriksaan)
        
        # Ubah label menu profil untuk dokter
        self.ui.btnMenuProfil.setText("� Menu Lainnya")
        
        # Connect table selection
        self.ui.tablePemeriksaan.itemSelectionChanged.connect(self.on_table_select)
        
        # Connect text changed untuk hitung total
        self.ui.txtBiayaDokter.textChanged.connect(self.hitung_total)
        self.ui.txtBiayaObat.textChanged.connect(self.hitung_total)
        
        # Make id pendaftaran field readonly and auto-generated
        self.ui.txtTglLahir.setReadOnly(True)
        self.ui.txtTglLahir.setPlaceholderText("Auto Generate ID Pendaftaran")
        
        # Connect NIK field untuk auto-load data pendaftaran
        self.ui.txtNIK.textChanged.connect(self.on_nik_changed)
        
        # Load data
        self.load_data()
        
        # Auto-generate ID Pendaftaran pertama kali
        self.generate_id_pendaftaran()
    
    def resize_window(self):
        """Resize window agar fit dengan screen dan semua elemen terlihat"""
        screen = QDesktopWidget().screenGeometry()
        # Gunakan ukuran yang lebih besar atau maksimal
        width = max(int(screen.width() * 0.95), 1300)  # Min 1300px atau 95% layar
        height = max(int(screen.height() * 0.9), 750)  # Min 750px atau 90% layar
        self.resize(width, height)
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.9)  # 90% dari lebar layar
        height = int(screen.height() * 0.85)  # 85% dari tinggi layar
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
    
    def load_data(self):
        """Load data pemeriksaan ke tabel dengan data pendaftaran"""
        try:
            # Coba ambil data dengan pendaftaran dulu
            data = Pemeriksaan.get_with_pendaftaran()
        except:
            try:
                # Fallback ke data dengan nama
                data = Pemeriksaan.get_all_with_name()
            except:
                # Fallback terakhir ke data basic
                data = Pemeriksaan.get_all()
        
        self.ui.tablePemeriksaan.setRowCount(0)
        
        for row_num, row_data in enumerate(data):
            self.ui.tablePemeriksaan.insertRow(row_num)
            
            # Sesuaikan jumlah kolom dengan data
            for col_num in range(min(len(row_data), self.ui.tablePemeriksaan.columnCount())):
                item = QTableWidgetItem(str(row_data[col_num]))
                self.ui.tablePemeriksaan.setItem(row_num, col_num, item)
        
        # Resize columns
        self.ui.tablePemeriksaan.resizeColumnsToContents()
    
    def on_table_select(self):
        """Ketika baris dipilih di tabel"""
        selected = self.ui.tablePemeriksaan.selectedItems()
        if selected:
            row = selected[0].row()
            
            # Ambil data dari tabel dengan pengecekan
            self.selected_id = self.ui.tablePemeriksaan.item(row, 0).text() if self.ui.tablePemeriksaan.item(row, 0) else ""
            nik = self.ui.tablePemeriksaan.item(row, 1).text() if self.ui.tablePemeriksaan.item(row, 1) else ""
            
            # Cek apakah ada kolom nama (kolom 2)
            if self.ui.tablePemeriksaan.columnCount() > 2 and self.ui.tablePemeriksaan.item(row, 2):
                nama = self.ui.tablePemeriksaan.item(row, 2).text()
                diagnosa_col = 3
            else:
                nama = ""
                diagnosa_col = 2
            
            diagnosa = self.ui.tablePemeriksaan.item(row, diagnosa_col).text() if self.ui.tablePemeriksaan.item(row, diagnosa_col) else ""
            
            # Isi form
            self.ui.txtNIK.setText(nik)
            if nama:
                self.ui.txtNama.setText(nama)
            self.ui.txtDiagnosa.setText(diagnosa)
    
    def tambah_pemeriksaan(self):
        """Tambah pemeriksaan baru"""
        # Ambil data dari form
        id_pendaftaran = self.ui.txtTglLahir.text().strip()
        nik = self.ui.txtNIK.text().strip()
        diagnosa = self.ui.txtDiagnosa.text().strip()
        resep = self.ui.txtResep.toPlainText().strip()
        
        try:
            biaya_dokter = float(self.ui.txtBiayaDokter.text().strip() or 0)
            biaya_obat = float(self.ui.txtBiayaObat.text().strip() or 0)
            total_biaya = biaya_dokter + biaya_obat
            total_obat = 1  # Default
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Biaya harus berupa angka!")
            return
        
        # Validasi
        if not nik:
            QMessageBox.warning(self, "Peringatan", "NIK harus diisi!")
            return
        
        if not diagnosa:
            QMessageBox.warning(self, "Peringatan", "Diagnosa harus diisi!")
            return
        
        # Simpan
        pemeriksaan = Pemeriksaan(nik, diagnosa, resep, total_biaya, total_obat)
        result = pemeriksaan.insert_pemeriksaan()
        
        if result is True:
            QMessageBox.information(self, "Berhasil", "Pemeriksaan berhasil disimpan!")
            self.clear_form()
            self.load_data()
            self.generate_id_pendaftaran()  # Generate ID baru setelah simpan
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan:\n{result}")
    
    def update_pemeriksaan(self):
        """Update pemeriksaan"""
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan diupdate!")
            return
        
        diagnosa = self.ui.txtDiagnosa.text().strip()
        resep = self.ui.txtResep.toPlainText().strip()
        
        try:
            biaya_dokter = float(self.ui.txtBiayaDokter.text().strip() or 0)
            biaya_obat = float(self.ui.txtBiayaObat.text().strip() or 0)
            total_biaya = biaya_dokter + biaya_obat
            total_obat = 1
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Biaya harus berupa angka!")
            return
        
        result = Pemeriksaan.update_pemeriksaan(
            self.selected_id, diagnosa, resep, total_biaya, total_obat
        )
        
        if result is True:
            QMessageBox.information(self, "Berhasil", "Data berhasil diupdate!")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.critical(self, "Gagal", f"Gagal update:\n{result}")
    
    def hapus_pemeriksaan(self):
        """Hapus pemeriksaan"""
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang akan dihapus!")
            return
        
        reply = QMessageBox.question(
            self, 
            "Konfirmasi", 
            "Yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = Pemeriksaan.delete_pemeriksaan(self.selected_id)
            
            if result is True:
                QMessageBox.information(self, "Berhasil", "Data berhasil dihapus!")
                self.clear_form()
                self.load_data()
            else:
                QMessageBox.critical(self, "Gagal", f"Gagal hapus:\n{result}")
    
    def clear_form(self):
        """Bersihkan form"""
        self.ui.txtNIK.clear()
        self.ui.txtNama.clear()
        self.ui.txtKeluhan.clear()
        self.ui.txtDiagnosa.clear()
        self.ui.txtResep.clear()
        self.ui.txtBiayaDokter.clear()
        self.ui.txtBiayaObat.clear()
        self.selected_id = None
        self.hitung_total()
        self.generate_id_pendaftaran()
    
    def generate_id_pendaftaran(self):
        """Generate ID pendaftaran otomatis"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        id_pendaftaran = f"REG-{timestamp}"
        self.ui.txtTglLahir.setText(id_pendaftaran)
    
    def on_nik_changed(self):
        """Auto-load data pasien/pendaftaran ketika NIK diinput"""
        nik = self.ui.txtNIK.text().strip()
        if len(nik) >= 16:  # NIK Indonesia 16 digit
            # Cari di pendaftaran
            from daftar import Pendaftaran
            data = Pendaftaran.get_by_nik(nik)
            if data and len(data) > 0:
                # Ambil data pendaftaran terakhir
                latest = data[0]
                self.ui.txtNama.setText(str(latest[1]) if len(latest) > 1 else "")
                self.ui.txtKeluhan.setText(str(latest[5]) if len(latest) > 5 else "")

    
    def hitung_total(self):
        """Hitung total biaya"""
        try:
            biaya_dokter = float(self.ui.txtBiayaDokter.text() or 0)
            biaya_obat = float(self.ui.txtBiayaObat.text() or 0)
            total = biaya_dokter + biaya_obat
            self.ui.lblTotal.setText(f"Rp {total:,.0f}")
        except:
            self.ui.lblTotal.setText("Rp 0")
    
    def show_profil(self):
        """Tampilkan profil dokter"""
        from profil_window import ProfilDokterWindow
        self.profil_window = ProfilDokterWindow(self.user_data)
        # Connect logout signal dari profil window ke parent
        if hasattr(self.profil_window, 'logout_signal'):
            self.profil_window.logout_signal.connect(self.logout_signal.emit)
        self.profil_window.show()
        self.close()
    
    def show_menu_dokter(self):
        """Tampilkan menu untuk dokter"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Menu Dokter")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        
        # Menu Profil Pribadi
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
        
        # Menu Data Pasien
        btn_pasien = QPushButton("👥 Data Pasien")
        btn_pasien.setMinimumHeight(50)
        btn_pasien.setStyleSheet("""
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
        btn_pasien.clicked.connect(lambda: [dialog.close(), self.show_data_pasien()])
        layout.addWidget(btn_pasien)
        
        # Menu Data Dokter
        btn_dokter = QPushButton("👨‍⚕️ Data Dokter")
        btn_dokter.setMinimumHeight(50)
        btn_dokter.setStyleSheet("""
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
        btn_dokter.clicked.connect(lambda: [dialog.close(), self.show_data_dokter()])
        layout.addWidget(btn_dokter)
        
        # Tombol Close
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
        """Tampilkan data dokter untuk CRUD"""
        from data_dokter_window import DataDokterWindow
        self.data_dokter_window = DataDokterWindow(self.user_data)
        self.data_dokter_window.show()
        self.close()
    
    def show_data_pasien(self):
        """Tampilkan data pasien untuk CRUD"""
        from data_pasien_window import DataPasienWindow
        self.data_pasien_window = DataPasienWindow(self.user_data)
        self.data_pasien_window.show()
        self.close()
    
    def show_pemeriksaan(self):
        """Refresh window pemeriksaan"""
        self.load_data()
    
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
                print("DEBUG - Calling app.on_logout() from PemeriksaanWindow")
                app.on_logout()
            else:
                # Fallback jika MainApp tidak ada
                self.logout_signal.emit()
