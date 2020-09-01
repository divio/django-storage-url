from .base import (
    dsn_configured_storage,
    dsn_configured_storage_class,
    get_storage,
)
from .backends import register_storage_class, get_storage_class

__version__ = "0.4.0"

__all__ = [
    "dsn_configured_storage",
    "dsn_configured_storage_class",
    "register_storage_class",
    "get_storage_class",
    "get_storage",
]
