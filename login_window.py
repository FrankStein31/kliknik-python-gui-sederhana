"""
Window Login - Menghubungkan UI Login dengan Backend
"""
from PyQt5.QtWidgets import QWidget, QMessageBox, QDesktopWidget
from PyQt5.QtCore import pyqtSignal, Qt
from ui_login import Ui_LoginDokter
from admin import Admin


class LoginWindow(QWidget):
    # Signal untuk emit ketika login berhasil
    login_success = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginDokter()
        self.ui.setupUi(self)
        
        # Set window properties
        self.setWindowTitle("Login - Sistem Informasi Klinik")
        
        # Auto-resize window untuk fit screen (80% dari screen size)
        self.resize_window()
        
        # Center window
        self.center_window()
        
        # Connect button ke fungsi
        self.ui.btnLogin.clicked.connect(self.do_login)
        self.ui.txtPassword.returnPressed.connect(self.do_login)
        self.ui.txtUsername.returnPressed.connect(self.do_login)
        
        # Hide register link (tidak digunakan)
        self.ui.lblRegister.hide()
        self.ui.lblRegisterLink.hide()
    
    def resize_window(self):
        """Resize window agar fit dengan screen"""
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.7)  # 70% dari lebar layar
        height = int(screen.height() * 0.7)  # 70% dari tinggi layar
        self.resize(width, height)
    
    def center_window(self):
        """Posisikan window di tengah layar"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def do_login(self):
        """Proses login"""
        username = self.ui.txtUsername.text().strip()
        password = self.ui.txtPassword.text().strip()
        
        # Validasi input
        if not username or not password:
            QMessageBox.warning(self, "Peringatan", "Username dan password harus diisi!")
            return
        
        # Proses login
        admin = Admin(username, password)
        result = admin.login()
        
        print(f"DEBUG - Login result: {result}")  # Debug output
        
        if result["status"]:
            # Login berhasil
            QMessageBox.information(
                self, 
                "Login Berhasil", 
                f"Selamat datang, {result['username']}!\nRole: {result['role']}"
            )
            
            # Emit signal dengan data user
            print(f"DEBUG - Emitting login_success signal with: {result}")  # Debug output
            self.login_success.emit(result)
            
            # Clear form
            self.ui.txtUsername.clear()
            self.ui.txtPassword.clear()
            
            # Close login window
            self.close()
        else:
            # Login gagal
            QMessageBox.critical(
                self, 
                "Login Gagal", 
                result.get("message", "Username atau password salah!")
            )
            self.ui.txtPassword.clear()
            self.ui.txtPassword.setFocus()
