"""
Authentication and Access Control Manager
Includes protection against failed attempts and auto-destruction
"""

import json
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime


class AuthManager:
    """Gestiona autenticación y seguridad de acceso"""

    def __init__(self, auth_file: Path, max_attempts: int = 3):
        self.auth_file = auth_file
        self.max_attempts = max_attempts
        self.auth_data = self._load_auth_data()

    def _load_auth_data(self) -> dict:
        """Carga datos de autenticación"""
        if self.auth_file.exists():
            try:
                with open(self.auth_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self._create_default_auth_data()
        return self._create_default_auth_data()

    def _create_default_auth_data(self) -> dict:
        """Crea estructura de datos de autenticación por defecto"""
        return {
            "password_hash": None,
            "salt": None,
            "failed_attempts": 0,
            "locked": False,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "auto_destroy_enabled": True,
            "max_attempts": self.max_attempts,
        }

    def _save_auth_data(self):
        """Guarda datos de autenticación"""
        with open(self.auth_file, "w", encoding="utf-8") as f:
            json.dump(self.auth_data, f, indent=2)

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Genera hash de contraseña con SHA-256 y salt"""
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()

    def has_password(self) -> bool:
        """Verifica si existe una contraseña configurada"""
        return self.auth_data.get("password_hash") is not None

    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validates password strength requirements

        Args:
            password: Password to validate

        Returns:
            Tuple[bool, str]: (valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)

        if not has_uppercase:
            return False, "Password must contain at least one uppercase letter"
        if not has_lowercase:
            return False, "Password must contain at least one lowercase letter"
        if not has_digit:
            return False, "Password must contain at least one number"
        if not has_symbol:
            return False, "Password must contain at least one special character"

        return True, "Password is strong"

    def set_password(
        self,
        password: str,
        auto_destroy_enabled: bool = True,
        max_attempts: int = 3,
    ) -> Tuple[bool, str]:
        """
        Establece la contraseña maestra

        Args:
            password: Nueva contraseña
            auto_destroy_enabled: Si la auto-destrucción está habilitada
            max_attempts: Número máximo de intentos permitidos

        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validate password strength
        valid, message = self.validate_password_strength(password)
        if not valid:
            return False, message

        # Generar salt
        salt = secrets.token_bytes(32)

        # Hash de contraseña
        password_hash = self._hash_password(password, salt)

        # Guardar
        self.auth_data["password_hash"] = password_hash
        self.auth_data["salt"] = salt.hex()
        self.auth_data["failed_attempts"] = 0
        self.auth_data["locked"] = False
        self.auth_data["auto_destroy_enabled"] = auto_destroy_enabled
        self.auth_data["max_attempts"] = max_attempts
        self.max_attempts = max_attempts

        self._save_auth_data()

        return True, "Contraseña establecida correctamente"

    def verify_password(self, password: str) -> Tuple[bool, str]:
        """
        Verifica la contraseña ingresada

        Args:
            password: Contraseña a verificar

        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Verificar si está bloqueado
        if self.auth_data.get("locked", False):
            return (
                False,
                "Sistema bloqueado por seguridad. Todos los datos han sido destruidos.",
            )

        # Verificar si existe contraseña
        if not self.has_password():
            return False, "No hay contraseña configurada"

        # Get current settings
        auto_destroy = self.auth_data.get("auto_destroy_enabled", True)
        max_attempts = self.auth_data.get("max_attempts", self.max_attempts)

        # Obtener salt y hash guardados
        salt = bytes.fromhex(self.auth_data["salt"])
        stored_hash = self.auth_data["password_hash"]

        # Calcular hash de la contraseña ingresada
        input_hash = self._hash_password(password, salt)

        # Verificar
        if input_hash == stored_hash:
            # Contraseña correcta
            self.auth_data["failed_attempts"] = 0
            self.auth_data["last_login"] = datetime.now().isoformat()
            self._save_auth_data()
            return True, "Acceso concedido"
        else:
            # Contraseña incorrecta
            if auto_destroy:
                self.auth_data["failed_attempts"] += 1
                attempts_left = max_attempts - self.auth_data["failed_attempts"]

                if attempts_left <= 0:
                    # Bloquear y marcar para destrucción
                    self.auth_data["locked"] = True
                    self._save_auth_data()
                    return False, "LÍMITE DE INTENTOS EXCEDIDO. Sistema bloqueado."

                self._save_auth_data()
                return (
                    False,
                    f"Contraseña incorrecta. Intentos restantes: {attempts_left}",
                )
            else:
                # No auto-destroy, just increment counter without limit
                self.auth_data["failed_attempts"] += 1
                self._save_auth_data()
                return False, "Contraseña incorrecta."

    def is_locked(self) -> bool:
        """Verifica si el sistema está bloqueado"""
        return self.auth_data.get("locked", False)

    def get_failed_attempts(self) -> int:
        """Retorna número de intentos fallidos"""
        return self.auth_data.get("failed_attempts", 0)

    def change_password(self, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña maestra

        Args:
            old_password: Contraseña actual
            new_password: Nueva contraseña

        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Verificar contraseña actual
        success, message = self.verify_password(old_password)

        if not success:
            return False, f"Contraseña actual incorrecta. {message}"

        # Establecer nueva contraseña
        return self.set_password(new_password)

    def reset_auth_data(self):
        """Resetea todos los datos de autenticación"""
        self.auth_data = self._create_default_auth_data()
        self._save_auth_data()

    def get_attempts_remaining(self) -> int:
        """Retorna intentos restantes antes del bloqueo"""
        max_attempts = self.auth_data.get("max_attempts", self.max_attempts)
        return max(0, max_attempts - self.auth_data.get("failed_attempts", 0))

    def is_auto_destroy_enabled(self) -> bool:
        """Verifica si la auto-destrucción está habilitada"""
        return self.auth_data.get("auto_destroy_enabled", True)

    def get_max_attempts(self) -> int:
        """Obtiene el número máximo de intentos configurado"""
        return self.auth_data.get("max_attempts", self.max_attempts)
