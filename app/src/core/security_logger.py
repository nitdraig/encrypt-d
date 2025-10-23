"""
Security logging module for audit trails and intrusion detection
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Optional
import json
from core.permissions import set_restricted_permissions


class SecurityLogger:
    """
    Centralized security logging system for audit trails

    Logs all security-relevant events:
    - Authentication attempts (success/failure)
    - Encryption/decryption operations
    - Access to encrypted data
    - Configuration changes
    - Errors and exceptions
    """

    # Log levels for security events
    CRITICAL = "CRITICAL"  # Security breach, data corruption
    WARNING = "WARNING"  # Failed authentication, suspicious activity
    INFO = "INFO"  # Successful operations
    DEBUG = "DEBUG"  # Detailed debug information

    def __init__(self, log_dir: Path):
        """
        Initialize security logger

        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create separate log files
        self.auth_log = log_dir / "auth.log"
        self.crypto_log = log_dir / "crypto.log"
        self.security_log = log_dir / "security.log"

        # Initialize Python loggers
        self._init_loggers()

    def _init_loggers(self):
        """Initialize Python logging infrastructure with rotation"""

        # Common formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Max log file size: 5 MB
        max_bytes = 5 * 1024 * 1024
        # Keep 5 backup files
        backup_count = 5

        # Authentication logger
        self.auth_logger = logging.getLogger("encrypt_d.auth")
        self.auth_logger.setLevel(logging.INFO)
        auth_handler = RotatingFileHandler(
            self.auth_log,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        auth_handler.setFormatter(formatter)
        self.auth_logger.addHandler(auth_handler)

        # Crypto operations logger
        self.crypto_logger = logging.getLogger("encrypt_d.crypto")
        self.crypto_logger.setLevel(logging.INFO)
        crypto_handler = RotatingFileHandler(
            self.crypto_log,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        crypto_handler.setFormatter(formatter)
        self.crypto_logger.addHandler(crypto_handler)

        # General security logger
        self.security_logger = logging.getLogger("encrypt_d.security")
        self.security_logger.setLevel(logging.INFO)
        security_handler = RotatingFileHandler(
            self.security_log,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        security_handler.setFormatter(formatter)
        self.security_logger.addHandler(security_handler)

        # Set restrictive permissions on log files
        set_restricted_permissions(self.auth_log)
        set_restricted_permissions(self.crypto_log)
        set_restricted_permissions(self.security_log)

    # Authentication Events

    def log_login_success(self):
        """Log successful authentication"""
        self.auth_logger.info("Login successful")

    def log_login_failed(self, attempts_remaining: int):
        """Log failed authentication attempt"""
        self.auth_logger.warning(
            f"Login failed | Attempts remaining: {attempts_remaining}"
        )

    def log_account_locked(self):
        """Log account lockout due to failed attempts"""
        self.auth_logger.critical("Account locked due to failed login attempts")

    def log_password_changed(self):
        """Log password change"""
        self.auth_logger.info("Master password changed successfully")

    def log_account_reset(self):
        """Log account/vault reset"""
        self.auth_logger.critical("Account reset - all data destroyed")

    # Encryption/Decryption Events

    def log_folder_encrypted(self, folder_name: str, folder_id: str):
        """Log folder encryption"""
        self.crypto_logger.info(
            f"Folder encrypted | Name: {folder_name} | ID: {folder_id}"
        )

    def log_folder_decrypted(self, folder_name: str, folder_id: str):
        """Log folder decryption"""
        self.crypto_logger.info(
            f"Folder decrypted | Name: {folder_name} | ID: {folder_id}"
        )

    def log_folder_deleted(self, folder_name: str, folder_id: str):
        """Log encrypted folder deletion"""
        self.crypto_logger.warning(
            f"Encrypted folder deleted | Name: {folder_name} | ID: {folder_id}"
        )

    def log_decryption_failed(self, folder_id: str, reason: str):
        """Log failed decryption attempt"""
        self.crypto_logger.warning(
            f"Decryption failed | ID: {folder_id} | Reason: {reason}"
        )

    # Security Events

    def log_invalid_path(self, path: str, reason: str):
        """Log invalid path detection"""
        self.security_logger.warning(
            f"Invalid path blocked | Path: {path} | Reason: {reason}"
        )

    def log_disk_space_error(self, required_mb: float, available_mb: float):
        """Log insufficient disk space"""
        self.security_logger.warning(
            f"Insufficient disk space | Required: {required_mb:.1f}MB | Available: {available_mb:.1f}MB"
        )

    def log_corruption_detected(self, folder_id: str):
        """Log data corruption detection"""
        self.security_logger.critical(f"Data corruption detected | ID: {folder_id}")

    def log_metadata_error(self, error: str):
        """Log metadata-related errors"""
        self.security_logger.critical(f"Metadata error | Details: {error}")

    def log_exception(self, operation: str, exception: str):
        """Log unexpected exceptions"""
        self.security_logger.critical(f"Exception in {operation} | Error: {exception}")

    def log_app_started(self):
        """Log application start"""
        self.security_logger.info("Application started")

    def log_app_closed(self):
        """Log application close"""
        self.security_logger.info("Application closed")

    # Utility methods

    def get_recent_events(
        self, log_file: str = "security", max_lines: int = 100
    ) -> list:
        """
        Get recent log events

        Args:
            log_file: Which log file to read (auth, crypto, security)
            max_lines: Maximum number of lines to return

        Returns:
            List of log entries (most recent first)
        """
        try:
            log_map = {
                "auth": self.auth_log,
                "crypto": self.crypto_log,
                "security": self.security_log,
            }

            log_path = log_map.get(log_file, self.security_log)

            if not log_path.exists():
                return []

            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Return most recent entries first
            return lines[-max_lines:][::-1]

        except Exception as e:
            return [f"Error reading logs: {e}"]


# Global logger instance (initialized by application)
_global_logger: Optional[SecurityLogger] = None


def init_security_logger(log_dir: Path):
    """
    Initialize the global security logger

    Args:
        log_dir: Directory for log files
    """
    global _global_logger
    _global_logger = SecurityLogger(log_dir)


def get_logger() -> Optional[SecurityLogger]:
    """Get the global security logger instance"""
    return _global_logger
