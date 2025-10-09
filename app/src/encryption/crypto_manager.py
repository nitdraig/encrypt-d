"""
Encryption and Decryption Manager
Uses AES-256 in GCM mode for robust security
"""

import os
import shutil
import json
from pathlib import Path
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


class CryptoManager:
    """Manages encryption and decryption of folders"""

    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = vault_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict:
        """Loads metadata of encrypted folders"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"folders": []}
        return {"folders": []}

    def _save_metadata(self):
        """Saves metadata of encrypted folders"""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

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

            if not source_path.exists():
                return False, "La carpeta no existe"

            if not source_path.is_dir():
                return False, "The path is not a folder"

            # Generate unique ID for this folder
            folder_id = secrets.token_hex(16)
            encrypted_folder = self.vault_dir / folder_id
            encrypted_folder.mkdir(exist_ok=True)

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

            # Don't delete original automatically for security
            return True, f"Folder encrypted successfully. ID: {folder_id}"

        except Exception as e:
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
                except Exception:
                    return False, "Incorrect password"

                # Restore file to original location within the folder
                original_rel_path = file_info["original_path"]
                output_file = output_dir / original_rel_path
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, "wb") as f:
                    f.write(decrypted_data)

            return True, f"Folder decrypted at: {output_dir}"

        except Exception as e:
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

            # Delete encrypted files
            encrypted_folder = self.vault_dir / folder_id
            if encrypted_folder.exists():
                shutil.rmtree(encrypted_folder)

            self._save_metadata()

            return True, "Folder permanently deleted"

        except Exception as e:
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
            except:
                pass

    def destroy_all_data(self):
        """Destroys all encrypted data (auto-destruction function)"""
        try:
            # Delete all encrypted folders
            if self.vault_dir.exists():
                shutil.rmtree(self.vault_dir)

            # Recreate empty directory
            self.vault_dir.mkdir(parents=True, exist_ok=True)

            # Clear metadata
            self.metadata = {"folders": []}
            self._save_metadata()

            return True
        except:
            return False
