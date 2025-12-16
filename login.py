import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from ui_login import Ui_LoginDokter
from admin import Admin  # Import class Admin yang sudah ada

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginDokter()
        self.ui.setupUi(self)
        
        # Connect signals
        self.ui.btnLogin.clicked.connect(self.handle_login)
        self.ui.lblRegisterLink.mousePressEvent = self.handle_register
        self.ui.txtPassword.returnPressed.connect(self.handle_login)
        self.ui.txtUsername.returnPressed.connect(self.handle_login)
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        frame_geometry = self.frameGeometry()
        screen_center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def handle_login(self):
        """Handle login button click"""
        username = self.ui.txtUsername.text().strip()
        password = self.ui.txtPassword.text().strip()
        
        # Validation
        if not username or not password:
            self.show_message("Error", "Username dan password harus diisi!", QMessageBox.Warning)
            return
        
        # Create admin object and login
        admin = Admin(username, password)
        result = admin.login()
        
        if result["status"]:
            self.show_message(
                "Login Berhasil", 
                f"Selamat datang, {result['username']}!\nRole: {result['role']}", 
                QMessageBox.Information
            )
            
            # Open appropriate window based on role
            self.open_window_by_role(result)
            
        else:
            self.show_message(
                "Login Gagal", 
                "Username atau password salah!\nSilakan coba lagi.", 
                QMessageBox.Critical
            )
            self.ui.txtPassword.clear()
            self.ui.txtUsername.setFocus()
    
    def open_window_by_role(self, user_data):
        """Open window based on user role"""
        role = user_data['role'].lower()
        
        try:
            if role == 'dokter':
                # Import dan buka file pemeriksaan
                from pemeriksaan import PemeriksaanWindow
                self.next_window = PemeriksaanWindow(user_data)
                self.next_window.show()
                self.close()
                
            elif role == 'pasien':
                # Import dan buka file pendaftaran
                from pendaftaran import PendaftaranWindow
                self.next_window = PendaftaranWindow(user_data)
                self.next_window.show()
                self.close()
                
            elif role == 'admin':
                # Import dan buka dashboard admin
                from dashboard_admin import AdminDashboard
                self.next_window = AdminDashboard(user_data)
                self.next_window.show()
                self.close()
                
            elif role == 'apoteker':
                # Import dan buka apotek
                from apotek import ApotekWindow
                self.next_window = ApotekWindow(user_data)
                self.next_window.show()
                self.close()
                
            else:
                self.show_message(
                    "Error", 
                    f"Role '{role}' tidak dikenali!", 
                    QMessageBox.Warning
                )
                
        except ImportError as e:
            self.show_message(
                "Error", 
                f"File untuk role '{role}' belum tersedia!\n\nError: {str(e)}", 
                QMessageBox.Critical
            )
            # Jangan close window jika file tidak ada
    
    def handle_register(self, event):
        """Handle register link click"""
        self.show_message(
            "Registrasi", 
            "Fitur registrasi akan segera tersedia.\nSilakan hubungi administrator untuk membuat akun.", 
            QMessageBox.Information
        )
    
    def show_message(self, title, message, icon):
        """Show message box"""
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Show login window
    login = LoginWindow()
    login.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()