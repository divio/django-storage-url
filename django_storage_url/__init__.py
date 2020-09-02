from .backends import get_storage_class, register_storage_class
from .base import (
    dsn_configured_storage,
    dsn_configured_storage_class,
    get_storage,
)


# for __version__ see setup.py

__all__ = [
    "dsn_configured_storage",
    "dsn_configured_storage_class",
    "register_storage_class",
    "get_storage_class",
    "get_storage",
]
