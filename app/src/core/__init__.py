"""
Core Module
Contains configuration and shared utilities
"""

from .config import *

__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "APP_DATA_DIR",
    "CONFIG_FILE",
    "AUTH_FILE",
    "VAULT_DIR",
    "MAX_LOGIN_ATTEMPTS",
    "SALT_SIZE",
    "KEY_ITERATIONS",
    "CHUNK_SIZE",
    "FILE_ATTRIBUTE_HIDDEN",
    "FILE_ATTRIBUTE_SYSTEM",
]
