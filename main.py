"""
Main Application - Sistem Klinik
Author: Klinik Management System
Date: 16 Desember 2025

Main controller untuk routing 6 windows:
1. RegisterWindow
2. LoginWindow
3. DashboardPasienWindow
4. ProfilPasienWindow (dengan DELETE AKUN)
5. PemeriksaanDokterWindow
6. ProfilDokterWindow (tanpa DELETE)
"""

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QObject

# Import semua windows
from views.register_window import RegisterWindow
from views.login_window import LoginWindow
from views.dashboard_pasien import DashboardPasienWindow
from views.profil_pasien import ProfilPasienWindow
from views.pemeriksaan_dokter import PemeriksaanDokterWindow
from views.profil_dokter import ProfilDokterWindow

class MainApp(QObject):
    """Main Application Controller"""
    
    def __init__(self):
        super().__init__()
        
        # Current active window
        self.current_window = None
        
        # User data
        self.current_user = None
        
        # Initialize login window
        self.show_login()
    
    def show_login(self):
        """Tampilkan login window"""
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = LoginWindow()
        self.current_window.login_success.connect(self.on_login_success)
        self.current_window.show_register.connect(self.show_register)
        self.current_window.show_window()
    
    def show_register(self):
        """Tampilkan register window"""
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = RegisterWindow()
        self.current_window.back_to_login.connect(self.show_login)
        self.current_window.show()
    
    def on_login_success(self, user_data):
        """
        Handle login success
        Route berdasarkan role:
        - pasien → DashboardPasienWindow
        - dokter → PemeriksaanDokterWindow
        """
        self.current_user = user_data
        role = user_data['role']
        
        if role == 'pasien':
            self.show_dashboard_pasien(user_data)
        elif role == 'dokter':
            self.show_pemeriksaan_dokter(user_data)
        else:
            QMessageBox.critical(None, "Error", f"Role tidak valid: {role}")
            self.show_login()
    
    def show_dashboard_pasien(self, user_data):
        """Tampilkan dashboard pasien"""
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = DashboardPasienWindow(user_data)
        self.current_window.show_profil.connect(self.show_profil_pasien)
        self.current_window.logout_signal.connect(self.on_logout)
        self.current_window.show()
    
    def show_profil_pasien(self, username):
        """Tampilkan profil pasien"""
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = ProfilPasienWindow(username)
        self.current_window.back_to_dashboard.connect(self.show_dashboard_pasien)
        self.current_window.account_deleted.connect(self.on_account_deleted)
        self.current_window.show()
    
    def show_pemeriksaan_dokter(self, user_data):
        """Tampilkan form pemeriksaan dokter"""
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = PemeriksaanDokterWindow(user_data)
        self.current_window.show_profil.connect(self.show_profil_dokter)
        self.current_window.logout_signal.connect(self.on_logout)
        self.current_window.show()
    
    def show_profil_dokter(self, username):
        """Tampilkan profil dokter"""
        if self.current_window:
            self.current_window.close()
            self.current_window.deleteLater()
        
        self.current_window = ProfilDokterWindow(username)
        self.current_window.back_to_pemeriksaan.connect(self.show_pemeriksaan_dokter)
        self.current_window.show()
    
    def on_logout(self):
        """Handle logout"""
        self.current_user = None
        self.show_login()
    
    def on_account_deleted(self):
        """Handle account deleted (pasien delete akun)"""
        QMessageBox.information(None, "Akun Dihapus", 
                              "Akun Anda telah dihapus.\n\n"
                              "Anda akan diarahkan ke halaman login.")
        self.current_user = None
        self.show_login()

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Sistem Klinik")
    app.setOrganizationName("Klinik Management")
    
    # Create main app controller
    main_app = MainApp()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
