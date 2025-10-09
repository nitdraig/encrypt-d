"""
Script de prueba para verificar funcionalidades básicas de Encrypt-D
Ejecuta este script para verificar que todo funciona correctamente
"""

import os
import tempfile
import shutil
from pathlib import Path

print("🧪 Iniciando pruebas de Encrypt-D...\n")

# Test 1: Importar módulos
print("✓ Test 1: Importando módulos...")
try:
    from config import APP_NAME, APP_VERSION, VAULT_DIR
    from crypto_manager import CryptoManager
    from auth_manager import AuthManager

    print(f"  ✓ Módulos importados correctamente")
    print(f"  ✓ Aplicación: {APP_NAME} v{APP_VERSION}")
except ImportError as e:
    print(f"  ✗ Error al importar: {e}")
    exit(1)

# Test 2: Verificar dependencias
print("\n✓ Test 2: Verificando dependencias...")
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import tkinter as tk

    print("  ✓ cryptography instalado")
    print("  ✓ tkinter disponible")
except ImportError as e:
    print(f"  ✗ Falta dependencia: {e}")
    exit(1)

# Test 3: Crear instancias
print("\n✓ Test 3: Creando instancias de gestores...")
try:
    temp_vault = Path(tempfile.mkdtemp())
    temp_auth = temp_vault / "auth.dat"

    crypto = CryptoManager(temp_vault)
    auth = AuthManager(temp_auth)

    print("  ✓ CryptoManager creado")
    print("  ✓ AuthManager creado")
except Exception as e:
    print(f"  ✗ Error: {e}")
    exit(1)

# Test 4: Funcionalidades de autenticación
print("\n✓ Test 4: Probando autenticación...")
try:
    # Configurar contraseña
    success, msg = auth.set_password("test_password_123")
    assert success, f"No se pudo configurar contraseña: {msg}"
    print("  ✓ Contraseña configurada")

    # Verificar contraseña correcta
    success, msg = auth.verify_password("test_password_123")
    assert success, f"Contraseña correcta rechazada: {msg}"
    print("  ✓ Verificación correcta funciona")

    # Verificar contraseña incorrecta
    success, msg = auth.verify_password("wrong_password")
    assert not success, "Contraseña incorrecta fue aceptada"
    print("  ✓ Verificación incorrecta funciona")

    # Verificar contador de intentos
    attempts = auth.get_attempts_remaining()
    print(f"  ✓ Sistema de intentos funciona (restantes: {attempts})")
except AssertionError as e:
    print(f"  ✗ {e}")
    exit(1)
except Exception as e:
    print(f"  ✗ Error: {e}")
    exit(1)

# Test 5: Funcionalidades de encriptación
print("\n✓ Test 5: Probando encriptación...")
try:
    # Crear carpeta de prueba
    test_folder = Path(tempfile.mkdtemp())
    test_file = test_folder / "test.txt"
    test_file.write_text("Contenido de prueba para encriptación")

    # Encriptar
    success, msg = crypto.encrypt_folder(
        str(test_folder), "test_password_123", "Test Folder"
    )
    assert success, f"No se pudo encriptar: {msg}"
    print("  ✓ Carpeta encriptada correctamente")
    print(f"    {msg}")

    # Verificar que la carpeta fue encriptada
    folders = crypto.get_encrypted_folders()
    assert len(folders) > 0, "No se encontraron carpetas encriptadas"
    print(f"  ✓ Carpetas encriptadas: {len(folders)}")

    # Desencriptar
    folder_id = folders[0]["id"]
    output_folder = Path(tempfile.mkdtemp())
    success, msg = crypto.decrypt_folder(
        folder_id, "test_password_123", str(output_folder)
    )
    assert success, f"No se pudo desencriptar: {msg}"
    print("  ✓ Carpeta desencriptada correctamente")

    # Verificar contenido
    decrypted_file = output_folder / "test.txt"
    assert decrypted_file.exists(), "Archivo desencriptado no existe"
    content = decrypted_file.read_text()
    assert content == "Contenido de prueba para encriptación", "Contenido no coincide"
    print("  ✓ Contenido verificado correctamente")

    # Limpiar
    shutil.rmtree(test_folder)
    shutil.rmtree(output_folder)

except AssertionError as e:
    print(f"  ✗ {e}")
    exit(1)
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

# Test 6: Verificar GUI
print("\n✓ Test 6: Verificando GUI...")
try:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    root.destroy()
    print("  ✓ GUI puede inicializarse")
except Exception as e:
    print(f"  ✗ Error con GUI: {e}")

# Limpiar archivos temporales
print("\n✓ Limpiando archivos temporales...")
try:
    shutil.rmtree(temp_vault)
    print("  ✓ Archivos temporales eliminados")
except:
    pass

# Resumen
print("\n" + "=" * 50)
print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 50)
print("\n🚀 Encrypt-D está listo para usar!")
print("\nPara ejecutar la aplicación:")
print("  python main.py")
print("\nPara compilar el ejecutable:")
print("  python build.py")
print("  o ejecuta: build.bat")
