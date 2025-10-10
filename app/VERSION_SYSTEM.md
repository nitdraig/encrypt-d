# 🔄 Sistema de Versionado y Migraciones - Encrypt-D

Documentación completa del sistema de versionado automático y migraciones de datos.

---

## 📋 Descripción

Encrypt-D incluye un sistema completo de versionado que:

- ✅ Detecta actualizaciones automáticamente
- ✅ Crea respaldos antes de migrar
- ✅ Migra datos entre versiones sin pérdida
- ✅ Mantiene historial de respaldos
- ✅ Permite roll-back manual si es necesario

---

## 🏗️ Arquitectura

### Componentes

| Componente         | Archivo                            | Función                           |
| ------------------ | ---------------------------------- | --------------------------------- |
| **VersionManager** | `src/core/version_manager.py`      | Gestiona versiones y migraciones  |
| **version.json**   | `%APPDATA%/Encrypt-D/version.json` | Almacena versión instalada        |
| **Backups**        | `%APPDATA%/Encrypt-D/backups/`     | Respaldos automáticos             |
| **Migraciones**    | Métodos `_migrate_X_Y_to_X_Z()`    | Lógica específica de cada versión |

### Flujo de Inicio

```
1. App inicia
   ↓
2. VersionManager.needs_migration()
   ↓
3. ¿Necesita migración?
   │
   ├── SÍ → Mostrar diálogo de migración
   │         ↓
   │         Crear backup
   │         ↓
   │         Ejecutar migraciones
   │         ↓
   │         Actualizar version.json
   │         ↓
   │         Continuar con app
   │
   └── NO → Continuar normalmente
```

---

## 📁 Estructura de Archivos

### version.json

Ubicación: `%APPDATA%/Encrypt-D/version.json`

```json
{
  "version": "1.1.0",
  "updated_at": "2025-10-10T15:30:00",
  "platform": "windows"
}
```

### Directorio de Backups

```
%APPDATA%/Encrypt-D/backups/
├── backup_v1.0.0_20251010_143000/
│   ├── auth.dat
│   ├── config.json
│   ├── version.json
│   └── vault/
│       ├── folder1_encrypted/
│       └── folder2_encrypted/
├── backup_v1.0.0_20251009_120000/
└── backup_v1.1.0_20251011_180000/
```

---

## 🔄 Agregar una Nueva Migración

### Ejemplo: Migración v1.1 a v1.2

**Paso 1:** Actualizar `APP_VERSION` en `config.py`

```python
APP_VERSION = "1.2.0"
```

**Paso 2:** Crear método de migración en `version_manager.py`

```python
def _migrate_1_1_to_1_2(self) -> bool:
    """
    Migration from version 1.1.x to 1.2.0

    Changes in 1.2.0:
    - Added cloud backup settings
    - New field in auth.dat for 2FA
    """
    print("Migrating 1.1.x → 1.2.0")

    try:
        # Example: Add new field to config
        config_file = APP_DATA_DIR / "config.json"
        if config_file.exists():
            with open(config_file, "r") as f:
                config = json.load(f)

            # Add new field
            if "cloud_backup" not in config:
                config["cloud_backup"] = {
                    "enabled": False,
                    "provider": None
                }

            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

        print("✓ Config updated with cloud backup settings")
        return True

    except Exception as e:
        print(f"Migration failed: {e}")
        return False
```

**Paso 3:** Registrar migración en `_run_migrations()`

```python
def _run_migrations(self, from_version: str, to_version: str) -> bool:
    # ... código existente ...

    # Migration from 1.1.x to 1.2.0
    if from_major == 1 and from_minor == 1 and to_minor >= 2:
        migrations.append(self._migrate_1_1_to_1_2)

    # ... resto del código ...
```

---

## 🧪 Testing de Migraciones

### Test Manual

**Simular migración de v1.0 a v1.1:**

```bash
# 1. Instalar versión antigua (v1.0)
git checkout v1.0.0
python app/main.py

# 2. Crear algunos datos
# - Registrar usuario
# - Encriptar carpetas

# 3. Cerrar app

# 4. Cambiar a versión nueva (v1.1)
git checkout v1.1.0

# 5. Ejecutar app - debe mostrar diálogo de migración
python app/main.py

# 6. Verificar:
# - Backup creado en backups/
# - version.json actualizado a 1.1.0
# - Datos intactos y accesibles
```

### Test Automatizado (futuro)

```python
# tests/test_migrations.py
def test_migrate_1_0_to_1_1():
    # Setup: Create v1.0 data
    # Execute: Run migration
    # Assert: Data is correct in v1.1 format
    pass
```

---

## 🔍 Verificación de Versión

### Consultar Versión Instalada

```python
from core import VersionManager

vm = VersionManager()
print(f"Installed: {vm.get_installed_version()}")
print(f"Current: {vm.get_current_app_version()}")
```

### Información Completa

```python
info = vm.get_migration_info()
print(info)
# {
#     'installed_version': '1.0.0',
#     'current_version': '1.1.0',
#     'needs_migration': True,
#     'from_version': '1.0.0',
#     'to_version': '1.1.0',
#     'is_first_install': False
# }
```

---

## 💾 Gestión de Backups

### Listar Backups

```python
vm = VersionManager()
backups = vm.list_backups()

for backup in backups:
    print(f"{backup['name']} - {backup['created']}")
```

### Limpiar Backups Antiguos

```python
# Mantener solo los últimos 5 backups
deleted = vm.cleanup_old_backups(keep_last=5)
print(f"Deleted {deleted} old backups")
```

### Restaurar Backup Manual

```bash
# 1. Cerrar Encrypt-D

# 2. Navegar a backups
cd %APPDATA%\Encrypt-D\backups\

# 3. Listar backups disponibles
dir

# 4. Copiar archivos del backup a directorio principal
# Ejemplo: Restaurar backup_v1.0.0_20251010_143000
copy backup_v1.0.0_20251010_143000\* ..\ /Y

# 5. Abrir Encrypt-D
```

---

## ⚠️ Consideraciones Importantes

### Migraciones Son Destructivas

- Las migraciones **modifican** los datos originales
- **SIEMPRE** crea un backup antes de migrar
- El backup automático se ejecuta antes de cualquier cambio

### Compatibilidad Hacia Adelante

- v1.1 **puede** leer datos de v1.0
- v1.0 **NO puede** leer datos de v1.1
- Una vez migrado, no se puede usar versión anterior sin restaurar backup

### Migraciones Acumulativas

Si saltas versiones (ej: v1.0 → v1.3), se ejecutan TODAS las migraciones intermedias:

```
v1.0 → v1.1 (migración 1)
v1.1 → v1.2 (migración 2)
v1.2 → v1.3 (migración 3)
```

---

## 📊 Historial de Migraciones

### v1.0.0 → v1.1.0

**Fecha:** Octubre 2025

**Cambios:**

- Agregada configuración de auto-destrucción opcional
- Agregada configuración de máximo intentos (1-10)
- Requisitos de contraseña más fuertes

**Migración:**

- Compatible hacia atrás con auth.dat de v1.0
- No requiere cambios manuales
- AuthManager agrega nuevos campos automáticamente

**Backup Recomendado:** ✅ Sí (automático)

---

### v1.1.0 → v1.2.0 (Planeado)

**Fecha:** Q1 2026

**Cambios Esperados:**

- Cloud backup settings
- 2FA configuration
- Biometric auth settings

**Migración Planeada:**

- Agregar campos a config.json
- Agregar campos a auth.dat para 2FA
- Migrar estructura de vault si es necesario

---

## 🛠️ Troubleshooting

### Error: "Migration failed"

**Causa:** Error durante la migración

**Solución:**

1. Tu backup está seguro en `backups/`
2. Restaura el backup manualmente (ver sección anterior)
3. Reporta el error con logs

### Error: "No module named 'version_manager'"

**Causa:** Archivo no incluido en .exe

**Solución:**
Asegúrate de que `version_manager.py` está en `src/core/` y rebuildeá:

```bash
python scripts/build.py
```

### Versión No Se Actualiza

**Causa:** version.json corrupto o no writable

**Solución:**

```bash
# Elimina version.json manualmente
del %APPDATA%\Encrypt-D\version.json

# Abre app - detectará primera instalación
```

---

## 📚 API Reference

### VersionManager

#### `get_current_app_version() -> str`

Retorna la versión de la aplicación (desde config.py)

#### `get_installed_version() -> Optional[str]`

Retorna la versión instalada (desde version.json) o None si es primera instalación

#### `needs_migration() -> Tuple[bool, Optional[str], str]`

Verifica si se necesita migración

**Returns:** `(needs_migration, from_version, to_version)`

#### `create_backup() -> Tuple[bool, str]`

Crea backup de todos los datos del usuario

**Returns:** `(success, backup_path_or_error)`

#### `migrate(from_version: str, to_version: str) -> Tuple[bool, str]`

Ejecuta migración entre versiones

**Returns:** `(success, message)`

#### `list_backups() -> list`

Lista todos los backups disponibles

#### `cleanup_old_backups(keep_last: int = 5) -> int`

Elimina backups antiguos, manteniendo solo los más recientes

**Returns:** Número de backups eliminados

---

## 🎯 Best Practices

### Para Desarrolladores

1. **Siempre incrementa la versión:** Cambios en formato de datos = nueva versión
2. **Escribe migraciones explícitas:** No confíes en compatibilidad automática
3. **Testea migraciones:** Simula upgrades de versiones anteriores
4. **Documenta cambios:** Actualiza este documento con cada migración

### Para Usuarios

1. **No elimines backups manualmente:** Usa `cleanup_old_backups()`
2. **Guarda backups importantes externamente:** Copia `backups/` a USB/nube
3. **No downgrades:** Una vez migrado, usa la nueva versión
4. **Reporta problemas:** Si la migración falla, reporta con logs

---

## 🚀 Future Enhancements

### Planeado para v2.0

- [ ] Auto-update desde internet
- [ ] Verificación de integridad de backups (checksums)
- [ ] Compresión de backups antiguos
- [ ] UI para gestionar backups (listar, restaurar, eliminar)
- [ ] Migración en segundo plano (progress bar)
- [ ] Roll-back automático si migración falla
- [ ] Tests automáticos de migraciones

---

**Última actualización:** Octubre 2025  
**Versión del documento:** 1.0
