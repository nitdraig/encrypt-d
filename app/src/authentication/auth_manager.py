"""
Authentication and Access Control Manager
Includes protection against failed attempts and auto-destruction
"""

import json
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime, timedelta
from core.security_logger import get_logger
from core.permissions import set_restricted_permissions


class AuthManager:
    """Gestiona autenticación y seguridad de acceso"""

    # Rate limiting constants
    RATE_LIMIT_WINDOW = 60  # seconds
    RATE_LIMIT_MAX_ATTEMPTS = 5  # max attempts within window
    RATE_LIMIT_LOCKOUT_TIME = 300  # 5 minutes lockout

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
            except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
                print(f"Warning: Auth file load failed: {e}")
                return self._create_default_auth_data()
            except Exception as e:
                print(f"Critical: Unexpected error loading auth: {e}")
                raise
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
            # Rate limiting fields
            "rate_limit_attempts": [],  # List of timestamp strings
            "rate_limit_locked_until": None,  # ISO timestamp or None
        }

    def _save_auth_data(self):
        """Guarda datos de autenticación"""
        with open(self.auth_file, "w", encoding="utf-8") as f:
            json.dump(self.auth_data, f, indent=2)

        # Set restrictive permissions on auth file
        set_restricted_permissions(self.auth_file)

    def _check_rate_limit(self) -> Tuple[bool, str]:
        """
        Checks if rate limiting is in effect

        Returns:
            Tuple[bool, str]: (allowed, message)
        """
        now = datetime.now()

        # Check if currently locked out
        locked_until = self.auth_data.get("rate_limit_locked_until")
        if locked_until:
            locked_time = datetime.fromisoformat(locked_until)
            if now < locked_time:
                remaining = int((locked_time - now).total_seconds())
                return False, f"Too many attempts. Locked for {remaining} more seconds."
            else:
                # Lockout expired, clear it
                self.auth_data["rate_limit_locked_until"] = None
                self.auth_data["rate_limit_attempts"] = []
                self._save_auth_data()

        # Clean old attempts outside the window
        cutoff = now - timedelta(seconds=self.RATE_LIMIT_WINDOW)
        attempts = self.auth_data.get("rate_limit_attempts", [])
        recent_attempts = [ts for ts in attempts if datetime.fromisoformat(ts) > cutoff]

        # Check if exceeded max attempts
        if len(recent_attempts) >= self.RATE_LIMIT_MAX_ATTEMPTS:
            # Trigger lockout
            lockout_until = now + timedelta(seconds=self.RATE_LIMIT_LOCKOUT_TIME)
            self.auth_data["rate_limit_locked_until"] = lockout_until.isoformat()
            self.auth_data["rate_limit_attempts"] = []
            self._save_auth_data()

            logger = get_logger()
            if logger:
                logger.log_exception(
                    "rate_limit",
                    f"Rate limit exceeded, locked for {self.RATE_LIMIT_LOCKOUT_TIME}s",
                )

            return (
                False,
                f"Too many attempts. Locked for {self.RATE_LIMIT_LOCKOUT_TIME} seconds.",
            )

        return True, "OK"

    def _record_login_attempt(self):
        """Records a login attempt for rate limiting"""
        now = datetime.now()

        # Clean old attempts
        cutoff = now - timedelta(seconds=self.RATE_LIMIT_WINDOW)
        attempts = self.auth_data.get("rate_limit_attempts", [])
        recent_attempts = [ts for ts in attempts if datetime.fromisoformat(ts) > cutoff]

        # Add new attempt
        recent_attempts.append(now.isoformat())
        self.auth_data["rate_limit_attempts"] = recent_attempts
        self._save_auth_data()

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
        if len(password) < 12:
            return False, "Password must be at least 12 characters long"

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
        # Check rate limiting first
        allowed, message = self._check_rate_limit()
        if not allowed:
            return False, message

        # Record this login attempt
        self._record_login_attempt()

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

        # Verificar (usando compare_digest para evitar timing attacks)
        if secrets.compare_digest(input_hash, stored_hash):
            # Contraseña correcta
            self.auth_data["failed_attempts"] = 0
            self.auth_data["last_login"] = datetime.now().isoformat()
            self._save_auth_data()

            # Log successful login
            logger = get_logger()
            if logger:
                logger.log_login_success()

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

                    # Log account lock
                    logger = get_logger()
                    if logger:
                        logger.log_account_locked()

                    return False, "LÍMITE DE INTENTOS EXCEDIDO. Sistema bloqueado."

                self._save_auth_data()

                # Log failed login
                logger = get_logger()
                if logger:
                    logger.log_login_failed(attempts_left)

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
        result = self.set_password(new_password)

        # Log password change if successful
        if result[0]:
            logger = get_logger()
            if logger:
                logger.log_password_changed()

        return result

    def reset_auth_data(self):
        """Resetea todos los datos de autenticación"""
        self.auth_data = self._create_default_auth_data()
        self._save_auth_data()

        # Log account reset
        logger = get_logger()
        if logger:
            logger.log_account_reset()

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
