"""
__init__.py untuk package views
"""

from .register_window import RegisterWindow
from .login_window import LoginWindow
from .dashboard_pasien import DashboardPasienWindow
from .profil_pasien import ProfilPasienWindow
from .pemeriksaan_dokter import PemeriksaanDokterWindow
from .profil_dokter import ProfilDokterWindow

__all__ = [
    'RegisterWindow',
    'LoginWindow', 
    'DashboardPasienWindow',
    'ProfilPasienWindow',
    'PemeriksaanDokterWindow',
    'ProfilDokterWindow'
]
