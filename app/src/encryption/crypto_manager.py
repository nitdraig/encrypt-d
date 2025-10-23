"""
Encryption and Decryption Manager
Uses AES-256 in GCM mode for robust security
"""

import os
import shutil
import json
from pathlib import Path
from typing import Optional, Tuple, Callable
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag
from core.security_logger import get_logger
from core.permissions import (
    set_restricted_permissions,
    set_restricted_permissions_recursive,
)
from core.secure_string import SecurePassword, clear_string_from_memory
import secrets


def secure_delete_file(file_path: Path, passes: int = 3) -> bool:
    """
    Securely deletes a file by overwriting it multiple times

    Args:
        file_path: Path to file to delete
        passes: Number of overwrite passes (default 3)

    Returns:
        bool: Success status
    """
    try:
        if not file_path.exists() or not file_path.is_file():
            return True

        file_size = file_path.stat().st_size

        with open(file_path, "r+b") as f:
            # Overwrite with random data
            for _ in range(passes):
                f.seek(0)
                f.write(secrets.token_bytes(file_size))
                f.flush()
                os.fsync(f.fileno())

            # Final overwrite with zeros
            f.seek(0)
            f.write(b"\x00" * file_size)
            f.flush()
            os.fsync(f.fileno())

        # Delete file
        os.remove(file_path)
        return True

    except Exception as e:
        print(f"Error securely deleting {file_path}: {e}")
        return False


def secure_delete_directory(dir_path: Path, passes: int = 3) -> bool:
    """
    Securely deletes a directory and all its contents

    Args:
        dir_path: Path to directory to delete
        passes: Number of overwrite passes for each file

    Returns:
        bool: Success status
    """
    try:
        if not dir_path.exists():
            return True

        # Securely delete all files
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                file_path = Path(root) / file
                secure_delete_file(file_path, passes)

            # Remove empty directories
            for dir_name in dirs:
                dir_to_remove = Path(root) / dir_name
                try:
                    dir_to_remove.rmdir()
                except:
                    pass

        # Remove root directory
        shutil.rmtree(dir_path, ignore_errors=True)
        return True

    except Exception as e:
        print(f"Error securely deleting directory {dir_path}: {e}")
        return False


class CryptoManager:
    """Manages encryption and decryption of folders"""

    @staticmethod
    def _validate_path(
        path: Path, allow_outside_vault: bool = True
    ) -> Tuple[bool, str]:
        """
        Validates that a path is safe to use

        Args:
            path: Path to validate
            allow_outside_vault: If False, path must be within vault

        Returns:
            Tuple[bool, str]: (valid, error_message)
        """
        try:
            # Resolve to absolute path
            abs_path = path.resolve()

            # Check for directory traversal
            if ".." in str(path):
                return False, "Invalid path: directory traversal detected"

            # Check for null bytes
            path_str = str(abs_path)
            if "\x00" in path_str:
                return False, "Invalid path: null bytes detected"

            # Check path length (Windows MAX_PATH = 260)
            if len(path_str) > 250:
                return False, "Path too long (max 250 characters)"

            # Check for invalid characters (Windows)
            invalid_chars = '<>"|?*'
            if any(c in path_str for c in invalid_chars):
                return False, "Invalid characters in path"

            return True, "Valid path"

        except Exception as e:
            return False, f"Path validation error: {e}"

    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir
        self.vault_dir.mkdir(parents=True, exist_ok=True)

        # Set restrictive permissions on vault directory
        set_restricted_permissions(self.vault_dir)

        self.metadata_file = vault_dir / "metadata.enc"  # Changed to .enc
        self.metadata_key = self._derive_basic_metadata_key()
        self.metadata = self._load_metadata()

    def _derive_basic_metadata_key(self) -> bytes:
        """
        Derives a basic key for metadata encryption
        Uses machine-specific information for key derivation

        Returns:
            32-byte encryption key for metadata
        """
        import platform

        # Combine vault path + machine info for key derivation
        machine_id = platform.node() + platform.machine()
        combined = str(self.vault_dir) + machine_id

        # Use PBKDF2 for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"ENCRYPT_D_META_V1",
            iterations=100000,
        )
        return kdf.derive(combined.encode())

    def _encrypt_metadata(self, data: dict) -> bytes:
        """
        Encrypts metadata dictionary

        Args:
            data: Metadata dictionary to encrypt

        Returns:
            Encrypted metadata bytes
        """
        json_data = json.dumps(data, indent=2, ensure_ascii=False).encode()

        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(self.metadata_key)
        ciphertext = aesgcm.encrypt(nonce, json_data, None)

        return nonce + ciphertext

    def _decrypt_metadata(self, encrypted_data: bytes) -> dict:
        """
        Decrypts metadata

        Args:
            encrypted_data: Encrypted metadata bytes

        Returns:
            Decrypted metadata dictionary
        """
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]

        aesgcm = AESGCM(self.metadata_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return json.loads(plaintext.decode())

    def _load_metadata(self) -> dict:
        """Loads metadata of encrypted folders"""
        # Check for old unencrypted metadata.json and migrate
        old_metadata_file = self.vault_dir / "metadata.json"
        if old_metadata_file.exists() and not self.metadata_file.exists():
            try:
                with open(old_metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Migrate to encrypted format
                print("Migrating metadata.json to encrypted format...")
                encrypted_data = self._encrypt_metadata(data)
                with open(self.metadata_file, "wb") as f:
                    f.write(encrypted_data)
                # Remove old file
                old_metadata_file.unlink()
                return data
            except Exception as e:
                print(f"Warning: Metadata migration failed: {e}")

        # Load encrypted metadata
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "rb") as f:
                    encrypted_data = f.read()

                return self._decrypt_metadata(encrypted_data)
            except (FileNotFoundError, PermissionError):
                return {"folders": []}
            except Exception as e:
                print(f"Critical: Metadata load failed: {e}")
                raise
        return {"folders": []}

    def _save_metadata(self):
        """Saves encrypted metadata of encrypted folders"""
        try:
            # Create backup of existing metadata before overwriting
            if self.metadata_file.exists():
                self._backup_metadata()

            encrypted_data = self._encrypt_metadata(self.metadata)
            with open(self.metadata_file, "wb") as f:
                f.write(encrypted_data)

            # Set restrictive permissions on metadata file
            set_restricted_permissions(self.metadata_file)
        except Exception as e:
            print(f"Error saving metadata: {e}")
            raise

    def _backup_metadata(self):
        """Creates a backup of the current metadata file"""
        try:
            if not self.metadata_file.exists():
                return

            # Create backups directory
            backup_dir = self.vault_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            set_restricted_permissions(backup_dir)

            # Generate backup filename with timestamp
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"metadata_{timestamp}.enc.backup"

            # Copy current metadata to backup
            shutil.copy2(self.metadata_file, backup_file)
            set_restricted_permissions(backup_file)

            # Keep only last 10 backups
            self._rotate_backups(backup_dir)

        except Exception as e:
            print(f"Warning: Backup failed: {e}")

    def _rotate_backups(self, backup_dir: Path):
        """Keeps only the most recent backups"""
        try:
            # Get all backup files
            backups = sorted(backup_dir.glob("metadata_*.enc.backup"))

            # Keep only last 10 backups
            max_backups = 10
            if len(backups) > max_backups:
                for old_backup in backups[:-max_backups]:
                    try:
                        old_backup.unlink()
                    except:
                        pass
        except Exception as e:
            print(f"Warning: Backup rotation failed: {e}")

    def restore_metadata_from_backup(
        self, backup_file: Path = None
    ) -> Tuple[bool, str]:
        """
        Restores metadata from a backup file

        Args:
            backup_file: Specific backup to restore. If None, uses most recent.

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            backup_dir = self.vault_dir / "backups"

            if not backup_dir.exists():
                return False, "No backups found"

            # Find backup to restore
            if backup_file is None:
                # Use most recent backup
                backups = sorted(backup_dir.glob("metadata_*.enc.backup"))
                if not backups:
                    return False, "No backups available"
                backup_file = backups[-1]

            if not backup_file.exists():
                return False, "Backup file not found"

            # Restore backup
            shutil.copy2(backup_file, self.metadata_file)
            set_restricted_permissions(self.metadata_file)

            # Reload metadata
            self.metadata = self._load_metadata()

            return True, f"Metadata restored from {backup_file.name}"

        except Exception as e:
            return False, f"Restore failed: {e}"

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derives a 256-bit key from the password

        Uses PBKDF2-HMAC with SHA-256 for secure key derivation.

        Args:
            password: User password string
            salt: Unique salt bytes

        Returns:
            Derived encryption key (32 bytes)
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def _encrypt_file(self, file_path: Path, key: bytes) -> bytes:
        """Encrypts a file and returns the encrypted data"""
        # Generate unique nonce
        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(key)

        # Read file
        with open(file_path, "rb") as f:
            plaintext = f.read()

        # Encrypt
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        # Return nonce + ciphertext
        return nonce + ciphertext

    def _decrypt_file(self, encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypts encrypted data"""
        # Extract nonce and ciphertext
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]

        # Decrypt
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return plaintext

    def encrypt_folder(
        self, folder_path: str, password: str, folder_name: str = None
    ) -> Tuple[bool, str]:
        """
        Encrypts a complete folder

        Args:
            folder_path: Path to the folder to encrypt
            password: Password for encryption
            folder_name: Custom name (optional)

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            source_path = Path(folder_path)

            # Validate path for security
            valid, error_msg = self._validate_path(source_path)
            if not valid:
                logger = get_logger()
                if logger:
                    logger.log_invalid_path(str(source_path), error_msg)
                return False, error_msg

            if not source_path.exists():
                return False, "La carpeta no existe"

            if not source_path.is_dir():
                return False, "The path is not a folder"

            # Calculate required space and check availability
            total_size = sum(
                f.stat().st_size for f in source_path.rglob("*") if f.is_file()
            )
            required_space = int(
                total_size * 1.3
            )  # 30% overhead for encryption metadata

            # Check available disk space
            stat = shutil.disk_usage(self.vault_dir)
            if stat.free < required_space:
                size_mb = required_space / 1024 / 1024
                free_mb = stat.free / 1024 / 1024
                logger = get_logger()
                if logger:
                    logger.log_disk_space_error(size_mb, free_mb)
                return (
                    False,
                    f"Insufficient disk space. Need {size_mb:.1f}MB, have {free_mb:.1f}MB",
                )

            # Generate unique ID for this folder
            folder_id = secrets.token_hex(16)
            encrypted_folder = self.vault_dir / folder_id
            encrypted_folder.mkdir(exist_ok=True)

            # Set restrictive permissions on encrypted folder
            set_restricted_permissions(encrypted_folder)

            # Generate unique salt
            salt = secrets.token_bytes(32)

            # Derive key
            key = self._derive_key(password, salt)

            # Encrypt all files
            file_mapping = {}

            for root, dirs, files in os.walk(source_path):
                rel_root = Path(root).relative_to(source_path)

                for file in files:
                    original_file = Path(root) / file
                    rel_path = rel_root / file

                    # Generate encrypted name
                    encrypted_name = secrets.token_hex(16) + ".enc"
                    encrypted_file_path = encrypted_folder / encrypted_name

                    # Encrypt file
                    encrypted_data = self._encrypt_file(original_file, key)

                    # Save encrypted file
                    with open(encrypted_file_path, "wb") as f:
                        f.write(encrypted_data)

                    # Map original name
                    file_mapping[encrypted_name] = {
                        "original_path": str(rel_path),
                        "size": original_file.stat().st_size,
                    }

            # Save folder information
            folder_info = {
                "id": folder_id,
                "name": folder_name or source_path.name,
                "original_path": str(source_path),
                "salt": salt.hex(),
                "file_mapping": file_mapping,
                "encrypted": True,
            }

            self.metadata["folders"].append(folder_info)
            self._save_metadata()

            # Hide the encrypted folder
            self._hide_folder(encrypted_folder)

            # Log successful encryption
            logger = get_logger()
            if logger:
                logger.log_folder_encrypted(folder_info["name"], folder_id)

            # Don't delete original automatically for security
            return True, f"Folder encrypted successfully. ID: {folder_id}"

        except Exception as e:
            logger = get_logger()
            if logger:
                logger.log_exception("encrypt_folder", str(e))
            return False, f"Error al encriptar: {str(e)}"

    def decrypt_folder(
        self, folder_id: str, password: str, output_path: str = None
    ) -> Tuple[bool, str]:
        """
        Decrypts a folder

        Args:
            folder_id: ID of the encrypted folder
            password: Password for decryption
            output_path: Path where to restore (optional)

        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Search folder in metadata
            folder_info = None
            for folder in self.metadata["folders"]:
                if folder["id"] == folder_id:
                    folder_info = folder
                    break

            if not folder_info:
                return False, "Folder not found"

            encrypted_folder = self.vault_dir / folder_id

            if not encrypted_folder.exists():
                return False, "Encrypted data does not exist"

            # Derive key with saved salt
            salt = bytes.fromhex(folder_info["salt"])
            key = self._derive_key(password, salt)

            # Determine output path - create folder with original name
            if output_path:
                # Create the folder with its original name in the selected location
                folder_name = folder_info["name"]
                output_dir = Path(output_path) / folder_name
            else:
                output_dir = Path(folder_info["original_path"])

            # Validate output path for security
            valid, error_msg = self._validate_path(output_dir)
            if not valid:
                logger = get_logger()
                if logger:
                    logger.log_invalid_path(str(output_dir), error_msg)
                return False, error_msg

            output_dir.mkdir(parents=True, exist_ok=True)

            # Decrypt files
            file_mapping = folder_info["file_mapping"]

            for encrypted_name, file_info in file_mapping.items():
                encrypted_file = encrypted_folder / encrypted_name

                if not encrypted_file.exists():
                    continue

                # Read encrypted data
                with open(encrypted_file, "rb") as f:
                    encrypted_data = f.read()

                # Decrypt
                try:
                    decrypted_data = self._decrypt_file(encrypted_data, key)
                except InvalidTag:
                    return False, "Incorrect password or corrupted data"
                except Exception as e:
                    print(f"Error: Decryption failed: {e}")
                    return False, "Decryption failed - file may be corrupted"

                # Restore file to original location within the folder
                original_rel_path = file_info["original_path"]
                output_file = output_dir / original_rel_path
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, "wb") as f:
                    f.write(decrypted_data)

            # Log successful decryption
            logger = get_logger()
            if logger:
                logger.log_folder_decrypted(folder_info["name"], folder_id)

            return True, f"Folder decrypted at: {output_dir}"

        except InvalidTag:
            logger = get_logger()
            if logger:
                logger.log_decryption_failed(
                    folder_id, "Invalid password or corrupted data"
                )
            return False, "Error decrypting: Invalid password or corrupted data"
        except Exception as e:
            logger = get_logger()
            if logger:
                logger.log_exception("decrypt_folder", str(e))
            return False, f"Error decrypting: {str(e)}"

    def delete_encrypted_folder(self, folder_id: str) -> Tuple[bool, str]:
        """Permanently deletes an encrypted folder"""
        try:
            # Search and remove from metadata
            folder_info = None
            for i, folder in enumerate(self.metadata["folders"]):
                if folder["id"] == folder_id:
                    folder_info = folder
                    del self.metadata["folders"][i]
                    break

            if not folder_info:
                return False, "Folder not found"

            # Securely delete encrypted files
            encrypted_folder = self.vault_dir / folder_id
            if encrypted_folder.exists():
                if not secure_delete_directory(encrypted_folder, passes=3):
                    return False, "Error securely deleting folder"

            self._save_metadata()

            # Log folder deletion
            logger = get_logger()
            if logger:
                logger.log_folder_deleted(folder_info["name"], folder_id)

            return True, "Folder permanently deleted"

        except Exception as e:
            logger = get_logger()
            if logger:
                logger.log_exception("delete_encrypted_folder", str(e))
            return False, f"Error deleting: {str(e)}"

    def get_encrypted_folders(self) -> list:
        """Returns list of encrypted folders"""
        return self.metadata.get("folders", [])

    def _hide_folder(self, folder_path: Path):
        """Hides a folder on Windows"""
        if os.name == "nt":
            try:
                import ctypes

                # Set hidden + system attribute
                ctypes.windll.kernel32.SetFileAttributesW(
                    str(folder_path), 0x02 | 0x04  # HIDDEN | SYSTEM
                )
            except Exception as e:
                print(f"Warning: Could not hide folder: {e}")

    # Secure password-based methods (CRIT-002 fix)

    def encrypt_folder_secure(
        self, folder_path: str, secure_password: SecurePassword, folder_name: str = None
    ) -> Tuple[bool, str]:
        """
        Encrypts a folder using SecurePassword (no plaintext password in memory)

        Args:
            folder_path: Path to the folder to encrypt
            secure_password: SecurePassword object
            folder_name: Custom name (optional)

        Returns:
            Tuple[bool, str]: (success, message)
        """

        def _encrypt_with_password(password: str) -> Tuple[bool, str]:
            result = self.encrypt_folder(folder_path, password, folder_name)
            # Clear password from local scope
            clear_string_from_memory(password)
            return result

        return secure_password.use_password(_encrypt_with_password)

    def decrypt_folder_secure(
        self, folder_id: str, secure_password: SecurePassword, output_path: str = None
    ) -> Tuple[bool, str]:
        """
        Decrypts a folder using SecurePassword (no plaintext password in memory)

        Args:
            folder_id: ID of the encrypted folder
            secure_password: SecurePassword object
            output_path: Path where to restore (optional)

        Returns:
            Tuple[bool, str]: (success, message)
        """

        def _decrypt_with_password(password: str) -> Tuple[bool, str]:
            result = self.decrypt_folder(folder_id, password, output_path)
            # Clear password from local scope
            clear_string_from_memory(password)
            return result

        return secure_password.use_password(_decrypt_with_password)

    def destroy_all_data(self):
        """Destroys all encrypted data (auto-destruction function)"""
        try:
            # Securely delete all encrypted folders
            if self.vault_dir.exists():
                secure_delete_directory(self.vault_dir, passes=3)

            # Recreate empty directory
            self.vault_dir.mkdir(parents=True, exist_ok=True)

            # Clear metadata
            self.metadata = {"folders": []}
            self._save_metadata()

            return True
        except Exception as e:
            print(f"Error: Data destruction failed: {e}")
            return False
