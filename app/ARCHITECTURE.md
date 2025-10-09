# 🏗️ Encrypt-D Architecture

## Screaming Architecture Overview

This project follows **Screaming Architecture** principles, where the folder structure clearly communicates what the application does, not which frameworks it uses.

## 📁 Directory Structure

```
encrypt-d/
│
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── .cursorrules                     # Project coding standards
├── .gitignore                       # Git exclusions
├── ARCHITECTURE.md                  # This file
│
├── src/                             # Source code (modular)
│   │
│   ├── encryption/                  # 🔐 ENCRYPTION MODULE
│   │   ├── __init__.py             # Module exports
│   │   └── crypto_manager.py       # Encryption/decryption logic
│   │                                # - AES-256-GCM implementation
│   │                                # - File encryption/decryption
│   │                                # - Folder management
│   │
│   ├── authentication/              # 🔑 AUTHENTICATION MODULE
│   │   ├── __init__.py             # Module exports
│   │   └── auth_manager.py         # Authentication logic
│   │                                # - Password hashing (PBKDF2)
│   │                                # - Failed attempts tracking
│   │                                # - Auto-destruction mechanism
│   │
│   ├── ui/                          # 🎨 USER INTERFACE MODULE
│   │   ├── __init__.py             # Module exports
│   │   └── application.py          # GUI implementation
│   │                                # - tkinter interface
│   │                                # - All screens and dialogs
│   │                                # - User interactions
│   │
│   ├── core/                        # ⚙️ CORE MODULE
│   │   ├── __init__.py             # Module exports
│   │   └── config.py               # Configuration
│   │                                # - Application constants
│   │                                # - Paths and settings
│   │                                # - Security parameters
│   │
│   └── i18n/                        # 🌍 INTERNATIONALIZATION MODULE
│       ├── __init__.py             # Module exports
│       ├── translator.py           # Translation system
│       │                            # - Language management
│       │                            # - Translation loading
│       │                            # - Format string support
│       ├── en.json                 # English translations
│       └── es.json                 # Spanish translations
│
├── tests/                           # 🧪 TEST SUITE
│   ├── __init__.py                 # Tests package
│   └── test_functionality.py       # Functionality tests
│
├── scripts/                         # 🔨 BUILD SCRIPTS
│   ├── build.py                    # Python build script
│   └── build.bat                   # Windows batch script
│
└── docs/                            # 📖 DOCUMENTATION
    ├── en/                          # English docs
    │   ├── README.md
    │   ├── CONTRIBUTING.md
    │   ├── MIGRATION_GUIDE.md
    │   └── I18N_SETUP_SUMMARY.md
    │
    └── es/                          # Spanish docs
        ├── README-es.md
        ├── CONFIGURACION_MULTILENGUAJE.md
        ├── INSTRUCCIONES_RAPIDAS.md
        └── RESUMEN_PROYECTO.md
```

## 🎯 Module Responsibilities

### 1. Encryption Module (`src/encryption/`)

**Responsibility:** Handle all encryption and decryption operations

**Key Components:**

- `CryptoManager`: Main class for encryption operations
- AES-256-GCM encryption algorithm
- PBKDF2 key derivation
- File and folder encryption/decryption
- Metadata management

**Dependencies:**

- `cryptography` library
- `core.config` for paths and constants

**Public API:**

```python
from encryption import CryptoManager

manager = CryptoManager(vault_dir)
success, message = manager.encrypt_folder(path, password, name)
success, message = manager.decrypt_folder(folder_id, password, output_path)
```

### 2. Authentication Module (`src/authentication/`)

**Responsibility:** Handle user authentication and security

**Key Components:**

- `AuthManager`: Main class for authentication
- Password hashing with PBKDF2-SHA256
- Failed attempts tracking
- Auto-destruction mechanism
- Session management

**Dependencies:**

- Python standard library (hashlib, secrets)
- `core.config` for security parameters

**Public API:**

```python
from authentication import AuthManager

auth = AuthManager(auth_file, max_attempts=3)
success, message = auth.set_password(password)
success, message = auth.verify_password(password)
is_locked = auth.is_locked()
```

### 3. UI Module (`src/ui/`)

**Responsibility:** Provide graphical user interface

**Key Components:**

- `EncryptDGUI`: Main GUI application class
- Setup screen
- Login screen
- Main application screen
- Dialog management

**Dependencies:**

- `tkinter` for GUI
- `encryption.CryptoManager`
- `authentication.AuthManager`
- `i18n` for translations

**Public API:**

```python
from ui import EncryptDGUI

app = EncryptDGUI()
app.run()
```

### 4. Core Module (`src/core/`)

**Responsibility:** Provide shared configuration and constants

**Key Components:**

- Application configuration
- Path definitions
- Security parameters
- Constants

**Dependencies:** None (lowest level)

**Public API:**

```python
from core.config import APP_NAME, VAULT_DIR, MAX_LOGIN_ATTEMPTS
```

### 5. i18n Module (`src/i18n/`)

**Responsibility:** Handle internationalization and translations

**Key Components:**

- `Translator`: Translation management class
- Language detection
- Translation file loading
- Format string support
- Fallback mechanisms

**Dependencies:**

- `core.config` for i18n directory path

**Public API:**

```python
from i18n import translate as t, set_language

set_language("es")
text = t("login.title")
formatted = t("success.folder_encrypted", id=folder_id)
```

## 🔄 Module Dependencies

```
┌─────────────────────────────────────────┐
│              main.py                    │
│         (Entry Point)                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│           ui/                           │
│      (User Interface)                   │
└──┬────────────┬────────────┬────────────┘
   │            │            │
   ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│encryption│ │   auth   │ │   i18n   │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┴────────────┘
                  │
                  ▼
            ┌──────────┐
            │   core   │
            │ (config) │
            └──────────┘
```

**Dependency Rules:**

1. `core` has NO dependencies (foundation)
2. `encryption`, `authentication`, `i18n` depend ONLY on `core`
3. `ui` depends on all other modules
4. `main.py` depends ONLY on `ui`

## 🎨 Design Patterns Used

### 1. Singleton Pattern

**Used in:** `i18n` module for the global translator instance

```python
_translator: Optional[Translator] = None

def get_translator() -> Translator:
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator
```

### 2. Facade Pattern

**Used in:** Each module's `__init__.py` provides a clean interface

```python
# encryption/__init__.py
from .crypto_manager import CryptoManager
__all__ = ["CryptoManager"]
```

### 3. Strategy Pattern

**Used in:** Encryption algorithm selection (ready for extension)

### 4. Observer Pattern (potential)

**Ready for:** UI updates when encryption status changes

## 🔐 Security Architecture

### Data Flow for Encryption

```
User selects folder
       ↓
UI collects input
       ↓
CryptoManager.encrypt_folder()
       ↓
Generate unique salt
       ↓
Derive key from password + salt (PBKDF2)
       ↓
For each file:
    Generate nonce
    Encrypt with AES-256-GCM
    Save to vault
       ↓
Save metadata
       ↓
Hide vault folder (Windows attributes)
```

### Data Flow for Authentication

```
User enters password
       ↓
AuthManager.verify_password()
       ↓
Load salt from auth file
       ↓
Hash input password with salt
       ↓
Compare hashes
       ↓
Match? → Grant access, reset attempts
No match? → Increment attempts, check limit
       ↓
Limit exceeded? → Lock system, trigger destruction
```

## 📊 Module Statistics

| Module         | Files | Lines      | Dependencies | Complexity |
| -------------- | ----- | ---------- | ------------ | ---------- |
| core           | 1     | ~35        | 0            | Low        |
| i18n           | 1     | ~200       | 1 (core)     | Medium     |
| encryption     | 1     | ~270       | 1 (core)     | High       |
| authentication | 1     | ~160       | 1 (core)     | Medium     |
| ui             | 1     | ~650       | 4 (all)      | High       |
| **Total**      | **5** | **~1,315** | -            | -          |

## 🚀 Scalability Features

### Easy to Add:

1. **New Encryption Algorithm**

   - Add to `encryption/` module
   - Implement interface
   - UI automatically uses it

2. **New Authentication Method**

   - Add to `authentication/` module
   - Implement interface
   - UI switches methods

3. **New Language**

   - Add `src/i18n/xx.json`
   - Translator auto-loads it
   - UI shows new option

4. **New UI Screen**
   - Add method to `ui/application.py`
   - Use existing modules
   - Follows same patterns

## 🧪 Testing Strategy

### Unit Tests (per module)

- `tests/test_encryption.py` → Encryption module
- `tests/test_authentication.py` → Authentication module
- `tests/test_i18n.py` → i18n module

### Integration Tests

- `tests/test_functionality.py` → Full workflow tests

### UI Tests (future)

- `tests/test_ui.py` → GUI interaction tests

## 📈 Future Architecture Enhancements

### Phase 1: Plugin System

```
src/
└── plugins/
    ├── __init__.py
    ├── base.py (plugin interface)
    └── encryption_plugins/
        ├── aes256.py
        └── chacha20.py
```

### Phase 2: Database Layer

```
src/
└── storage/
    ├── __init__.py
    ├── database.py
    └── models/
```

### Phase 3: API Layer

```
src/
└── api/
    ├── __init__.py
    ├── rest_api.py
    └── websocket.py
```

## 💡 Benefits of This Architecture

### ✅ Maintainability

- Clear module boundaries
- Easy to find code
- Single responsibility principle

### ✅ Testability

- Independent modules
- Easy to mock dependencies
- Clear interfaces

### ✅ Scalability

- Add features without touching existing code
- Plugin-ready structure
- Microservices-ready

### ✅ Understandability

- Self-documenting structure
- Clear purpose per module
- Minimal coupling

## 📚 References

- [Screaming Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)

---

**Remember:** The architecture should scream "I encrypt folders!" not "I'm built with Python and tkinter!"
