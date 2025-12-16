"""
__init__.py untuk package models
"""

from .admin import Admin
from .pasien import Pasien
from .dokter import Dokter
from .pendaftaran import Pendaftaran
from .pemeriksaan import Pemeriksaan

__all__ = ['Admin', 'Pasien', 'Dokter', 'Pendaftaran', 'Pemeriksaan']
