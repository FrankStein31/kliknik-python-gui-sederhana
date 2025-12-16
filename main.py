"""
SISTEM INFORMASI KLINIK - GUI VERSION
Main Entry Point
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from login_window import LoginWindow
from pemeriksaan_window import PemeriksaanWindow
from pendaftaran_window import PendaftaranWindow


class MainApp(QObject):
    # Singleton instance
    _instance = None
    
    # Signal untuk logout yang bisa diakses dari window lain
    logout_requested = pyqtSignal()
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        return cls._instance
    
    def __init__(self):
        super().__init__()
        MainApp._instance = self  # Set singleton
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.main_window = None
        self.user_data = None
        
    def show_login(self):
        """Tampilkan window login"""
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self, user_data):
        """Handler ketika login berhasil"""
        print(f"DEBUG - on_login_success called with: {user_data}")  # Debug output
        self.user_data = user_data
        
        # Tutup login window
        if self.login_window:
            self.login_window.close()
        
        # Buka window sesuai role
        print(f"DEBUG - User role: {user_data['role']}")  # Debug output
        if user_data["role"] == "dokter":
            print("DEBUG - Creating PemeriksaanWindow")  # Debug output
            self.main_window = PemeriksaanWindow(user_data)
            # Connect logout signal
            if hasattr(self.main_window, 'logout_signal'):
                self.main_window.logout_signal.connect(self.on_logout)
        else:  # pasien
            print("DEBUG - Creating PendaftaranWindow")  # Debug output
            self.main_window = PendaftaranWindow(user_data)
            # Connect logout signal
            if hasattr(self.main_window, 'logout_signal'):
                self.main_window.logout_signal.connect(self.on_logout)
        
        print("DEBUG - Showing main window")  # Debug output
        self.main_window.show()
    
    def on_logout(self):
        """Handler ketika user logout"""
        print("DEBUG - on_logout called")  # Debug output
        
        # Tutup main window
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        
        # Tampilkan login window lagi
        self.show_login()
    
    def run(self):
        """Jalankan aplikasi"""
        self.show_login()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = MainApp()
    app.run()
