"""
Module storage pour InfoWatchdog.
Contient les systèmes de stockage pour les données collectées.
"""

from .base_storage import BaseStorage
from .airtable_storage import AirtableStorage

__all__ = [
    'BaseStorage',
    'AirtableStorage'
]