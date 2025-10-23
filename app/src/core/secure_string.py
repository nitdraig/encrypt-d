"""
Secure string handling for passwords and sensitive data
Provides memory protection and automatic cleanup
"""

import ctypes
import array
import secrets
from typing import Optional, Callable


class SecureString:
    """
    A secure string class that:
    - Stores sensitive data in a mutable array
    - Overwrites memory on deletion
    - Provides context manager support
    - Minimizes exposure time
    """

    def __init__(self, initial_value: str = ""):
        """
        Initialize secure string

        Args:
            initial_value: Initial string value (will be copied and cleared)
        """
        # Use array of integers (unicode code points) for mutability
        if initial_value:
            self._data = array.array("u", initial_value)
        else:
            self._data = array.array("u")

        # Flag to track if cleared
        self._cleared = False

    def set(self, value: str):
        """
        Set the secure string value

        Args:
            value: New string value
        """
        # Clear existing data first
        self.clear()

        # Set new value
        self._data = array.array("u", value)
        self._cleared = False

    def get(self) -> str:
        """
        Get the string value

        WARNING: This creates a temporary string in memory.
        Use with_value() context manager when possible.

        Returns:
            The string value
        """
        if self._cleared:
            raise ValueError("SecureString has been cleared")

        return self._data.tounicode()

    def with_value(self, callback: Callable[[str], any]) -> any:
        """
        Execute a callback with the string value
        The value is immediately cleared from local scope after use

        Args:
            callback: Function that takes the string value

        Returns:
            Result of callback
        """
        if self._cleared:
            raise ValueError("SecureString has been cleared")

        try:
            value = self._data.tounicode()
            result = callback(value)

            # Clear the local value variable
            if "value" in locals():
                value = "\0" * len(value)
                del value

            return result
        except Exception as e:
            raise e

    def clear(self):
        """Securely clear the string from memory"""
        if not self._cleared and len(self._data) > 0:
            # Overwrite with zeros
            for i in range(len(self._data)):
                self._data[i] = "\0"

            # Clear the array
            self._data = array.array("u")
            self._cleared = True

    def __del__(self):
        """Ensure cleanup on deletion"""
        self.clear()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - clear on exit"""
        self.clear()
        return False

    def __len__(self) -> int:
        """Return length of stored string"""
        if self._cleared:
            return 0
        return len(self._data)

    def __bool__(self) -> bool:
        """Check if string has content"""
        return not self._cleared and len(self._data) > 0


class SecurePassword:
    """
    Specialized secure string for password handling
    Provides additional security features specific to passwords
    """

    def __init__(self, password: str = ""):
        """
        Initialize secure password

        Args:
            password: Initial password value
        """
        self._secure_str = SecureString(password)
        # Store a salted hash for verification without exposing password
        self._verification_hash = (
            self._create_verification_hash(password) if password else None
        )

    def _create_verification_hash(self, password: str) -> bytes:
        """Create a hash for password verification"""
        import hashlib

        salt = secrets.token_bytes(16)
        hash_val = hashlib.sha256(salt + password.encode()).digest()
        return salt + hash_val

    def verify(self, password: str) -> bool:
        """
        Verify if a password matches without exposing stored password

        Args:
            password: Password to verify

        Returns:
            True if password matches
        """
        if not self._verification_hash:
            return False

        import hashlib

        salt = self._verification_hash[:16]
        stored_hash = self._verification_hash[16:]
        test_hash = hashlib.sha256(salt + password.encode()).digest()

        return secrets.compare_digest(test_hash, stored_hash)

    def set(self, password: str):
        """
        Set new password

        Args:
            password: New password value
        """
        self._secure_str.set(password)
        self._verification_hash = self._create_verification_hash(password)

    def derive_key(self, salt: bytes, iterations: int = 100000) -> bytes:
        """
        Derive a cryptographic key from the password

        Args:
            salt: Salt for key derivation
            iterations: Number of PBKDF2 iterations

        Returns:
            Derived key (32 bytes)
        """
        import hashlib

        def _derive(password: str) -> bytes:
            return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)

        return self._secure_str.with_value(_derive)

    def use_password(self, callback: Callable[[str], any]) -> any:
        """
        Execute a callback with the password value

        Args:
            callback: Function that uses the password

        Returns:
            Result of callback
        """
        return self._secure_str.with_value(callback)

    def clear(self):
        """Clear the password from memory"""
        self._secure_str.clear()
        self._verification_hash = None

    def is_set(self) -> bool:
        """Check if password is set"""
        return bool(self._secure_str)

    def __del__(self):
        """Ensure cleanup on deletion"""
        self.clear()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.clear()
        return False


def clear_string_from_memory(s: str):
    """
    Attempt to clear a string from memory

    Note: This is best-effort as Python's memory management
    makes this difficult. Use SecureString class instead when possible.

    Args:
        s: String to clear
    """
    try:
        # Try to overwrite the string's internal buffer
        # This doesn't always work due to Python's string interning
        if s:
            # Get the address of the string object
            str_address = id(s)
            str_size = len(s)

            # Create a ctypes string buffer at that address
            # WARNING: This is highly platform-dependent and may not work
            try:
                ctypes.memset(str_address, 0, str_size)
            except:
                pass  # Best effort
    except:
        pass  # Best effort
