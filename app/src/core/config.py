"""
Configuración global de la aplicación Encrypt-D
"""

import os
from pathlib import Path

# Configuración de la aplicación
APP_NAME = "Encrypt-D"
APP_VERSION = "1.0.0"

# Directorio de datos de la aplicación
APP_DATA_DIR = (
    Path(os.getenv("APPDATA")) / APP_NAME
    if os.name == "nt"
    else Path.home() / f".{APP_NAME.lower()}"
)
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Archivos de configuración
CONFIG_FILE = APP_DATA_DIR / "config.json"
AUTH_FILE = APP_DATA_DIR / "auth.dat"
VAULT_DIR = APP_DATA_DIR / "vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de seguridad
MAX_LOGIN_ATTEMPTS = 3
SALT_SIZE = 32
KEY_ITERATIONS = 100000

# Configuración de encriptación
CHUNK_SIZE = 64 * 1024  # 64KB chunks para archivos grandes

# Atributos de Windows para ocultar archivos
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
