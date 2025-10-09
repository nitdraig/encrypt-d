# 🔒 Encrypt-D

**Secure Folder Encryption Manager for Windows**

> **Multi-language Application** | English Code | Modular Architecture

## 📁 Project Structure (Screaming Architecture)

```
encrypt-d/
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .cursorrules                 # Project rules and standards
├── .gitignore                   # Git exclusions
│
├── src/                         # Source code (modular)
│   ├── encryption/              # 🔐 Encryption module
│   │   ├── __init__.py
│   │   └── crypto_manager.py   # AES-256-GCM encryption logic
│   │
│   ├── authentication/          # 🔑 Authentication module
│   │   ├── __init__.py
│   │   └── auth_manager.py     # Password & security logic
│   │
│   ├── ui/                      # 🎨 User interface module
│   │   ├── __init__.py
│   │   └── application.py      # GUI with tkinter
│   │
│   ├── core/                    # ⚙️ Core configuration
│   │   ├── __init__.py
│   │   └── config.py            # App constants & settings
│   │
│   └── i18n/                    # 🌍 Internationalization
│       ├── __init__.py
│       ├── translator.py        # Translation system
│       ├── en.json              # English translations
│       └── es.json              # Spanish translations
│
├── tests/                       # 🧪 Test suite
│   ├── __init__.py
│   └── test_functionality.py   # Functionality tests
│
├── scripts/                     # 🔨 Build scripts
│   ├── build.py                # Python build script
│   └── build.bat               # Windows batch script
│
└── docs/                        # 📖 Documentation
    ├── en/                      # English documentation
    │   ├── README.md
    │   ├── CONTRIBUTING.md
    │   ├── MIGRATION_GUIDE.md
    │   └── I18N_SETUP_SUMMARY.md
    │
    └── es/                      # Spanish documentation
        ├── README-es.md
        ├── CONFIGURACION_MULTILENGUAJE.md
        ├── INSTRUCCIONES_RAPIDAS.md
        └── RESUMEN_PROYECTO.md
```

## ✨ Key Features

### 🔒 Security

- **AES-256-GCM encryption** (military standard)
- **PBKDF2-SHA256 hashing** (100,000 iterations)
- **Auto-destruction** after 3 failed attempts
- **Hidden folders** from Windows Explorer

### 🌍 Multi-language

- **Code in English** (international standard)
- **UI in multiple languages** (EN/ES)
- **Easy to add new languages**
- **Auto-detect system language**

### 📦 Modular Architecture

- **Screaming Architecture** design
- **Clear separation of concerns**
- **Easy to maintain and extend**
- **Independent modules**

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd encrypt-d

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

### Build Executable

```bash
# Windows
cd scripts
build.bat

# Or with Python
python build.py
```

The `.exe` file will be in the `dist/` folder.

## 🏗️ Architecture

### Screaming Architecture Principles

The project structure "screams" about what the application does:

- **`src/encryption/`** → "I encrypt files!"
- **`src/authentication/`** → "I handle passwords!"
- **`src/ui/`** → "I show the interface!"
- **`src/i18n/`** → "I support multiple languages!"

Each module is independent and has a single responsibility.

### Module Dependencies

```
main.py
  └── ui/
      ├── encryption/
      │   └── core/
      ├── authentication/
      │   └── core/
      └── i18n/
          └── core/
```

## 📖 Documentation

### English

- [Contributing Guide](docs/en/CONTRIBUTING.md)
- [Migration Guide](docs/en/MIGRATION_GUIDE.md)
- [i18n Setup](docs/en/I18N_SETUP_SUMMARY.md)

### Spanish

- [Guía de Configuración](docs/es/CONFIGURACION_MULTILENGUAJE.md)
- [Instrucciones Rápidas](docs/es/INSTRUCCIONES_RAPIDAS.md)
- [Resumen del Proyecto](docs/es/RESUMEN_PROYECTO.md)

## 🧪 Testing

```bash
# Run tests
cd tests
python test_functionality.py
```

## 🔧 Development

### Adding a New Module

1. Create directory in `src/`
2. Add `__init__.py`
3. Implement functionality
4. Update imports in `main.py`

### Code Standards

- **Language**: English only
- **Style**: PEP 8
- **Docstrings**: Google style
- **UI Strings**: Use i18n system

See [.cursorrules](.cursorrules) for complete standards.

## 🌟 Benefits of This Architecture

### Modularity

✅ Each module is independent  
✅ Easy to test in isolation  
✅ Clear boundaries

### Scalability

✅ Add new features without touching existing code  
✅ Easy to refactor  
✅ Plugin-ready architecture

### Maintainability

✅ Easy to find code  
✅ Clear responsibilities  
✅ Self-documenting structure

## 📊 Technology Stack

| Component  | Technology   | Purpose          |
| ---------- | ------------ | ---------------- |
| Language   | Python 3.8+  | Core development |
| GUI        | tkinter      | Native interface |
| Encryption | cryptography | AES-256-GCM      |
| Build      | PyInstaller  | Create .exe      |
| i18n       | Custom       | Multi-language   |

## 🤝 Contributing

See [CONTRIBUTING.md](docs/en/CONTRIBUTING.md) for guidelines.

**Remember:** Code in English, comments in English, but the UI speaks the user's language!

## 📝 License

MIT License - See LICENSE file for details.

## 🎯 Roadmap

- [ ] Additional languages (FR, DE, etc.)
- [ ] Cloud synchronization
- [ ] Mobile app
- [ ] Browser extension

---

**Encrypt-D** - Secure. Modular. International. 🔒🌍
