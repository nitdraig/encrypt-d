# 🔒 Encrypt-D

> **Military-Grade Security. Human-Level Simplicity.**

**Encrypt-D** is a professional folder encryption manager for Windows, combining AES-256-GCM military-grade encryption with an intuitive interface. Part of **Excelso Vault** - the security division of the Excelso Tech Group.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

---

## 🌟 About Excelso

**Encrypt-D** is part of [Excelso](https://excelso.xyz), a technology group focused on driving innovation, digitalization, and sustainability.

### Excelso's Mission

> _"We fix it thinking of you. We are solutions. We are Excelso."_

This motto reflects a client-centered approach and commitment to delivering real digital solutions.

### Excelso Divisions

- **🔐 Vault**: Security and privacy solutions (Encrypt-D's home)
- **🌐 Open**: Open-source initiatives and collaborative projects
- **🚀 Tech Group**: Innovation-driven technological community

**Encrypt-D** embodies Excelso's values by:

- **"Thinking of you"** → Multi-language interface, intuitive design, automatic protection
- **"We are solutions"** → Solves data security comprehensively
- **"We are Excelso"** → Professional quality, open source, technological innovation

---

## 📊 Project Overview

### What is Encrypt-D?

A complete digital security solution offering military-grade protection for confidential information on Windows. It combines enterprise-class encryption with accessibility for all users, aligning with Excelso's mission to democratize technological solutions without compromising quality.

### Project Components

**1. Desktop Application (`app/`)**

- Military-grade encryption (AES-256-GCM)
- Professional modular architecture
- Intuitive graphical interface
- Multi-language support (EN/ES)
- Auto-destruction after failed attempts
- System-level hidden folders on Windows

**2. Web Landing Page (`web/`)**

- Modern site built with Astro
- Responsive and accessible design
- Integrated multi-language support
- SEO and performance optimized
- Deploy-ready for multiple platforms

---

## ✨ Key Features

### 🛡️ Security

- **Encryption**: AES-256-GCM (military standard)
- **Hashing**: PBKDF2-SHA256 (100,000 iterations)
- **Protection**: Auto-destruction after 3 failed attempts
- **Privacy**: Hidden folders at Windows system level

### 🌍 Global Reach

- Multi-language interface (EN/ES)
- Code in English (international standard)
- Easy expansion to new languages
- Complete bilingual documentation

### 🏗️ Professional Architecture

- Modular design (Screaming Architecture)
- Clear separation of concerns
- Maintainable and scalable code
- PEP 8 compliant

### 🎨 User Experience

- Modern graphical interface
- Professional dark theme
- Intuitive workflows
- Clear feedback

---

## 📁 Complete Project Structure

```
encrypt-d/
│
├── app/                        # Desktop Application
│   ├── main.py                # Application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── src/                   # Modular source code
│   │   ├── encryption/        # 🔐 Encryption module
│   │   ├── authentication/    # 🔑 Authentication module
│   │   ├── ui/               # 🎨 User interface module
│   │   ├── core/             # ⚙️ Core configuration
│   │   └── i18n/             # 🌍 Internationalization
│   ├── tests/                # 🧪 Test suite
│   ├── scripts/              # 🔨 Build scripts
│   └── docs/                 # 📖 Documentation (EN/ES)
│
├── web/                       # Landing Page
│   ├── src/
│   │   ├── components/       # Reusable Astro components
│   │   ├── layouts/          # Page layouts
│   │   ├── pages/            # Routes (EN/ES)
│   │   └── i18n/             # Translations
│   ├── public/               # Static assets
│   └── dist/                 # Build output
│
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Desktop Application

```bash
# Navigate to app directory
cd app

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Build executable
cd scripts
./build.bat  # Windows
```

### Web Landing Page

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Deploy
vercel  # or netlify deploy
```

---

## 💎 Project Tagline

> **"Your privacy, encrypted with certainty. Security without compromise."**

_Alternatives:_

- _"Intelligent Protection. Absolute Peace of Mind."_
- _"Where your secrets are truly safe."_
- _"Military-grade security, human-level simplicity."_

---

## 🎯 Use Cases

### For Enterprise Clients

- Protection of confidential documents
- Privacy regulation compliance
- Security on shared devices
- Sensitive information backup

### For Developers

- Clean architecture example
- Robust security implementation
- Open-source reference
- Educational project

### For Excelso Portfolio

- Technical capabilities demonstration
- Commitment to security
- Focus on real solutions
- Development quality showcase

---

## 📈 Strategic Value for Excelso

### 🔐 Vault Secure

_Encrypt-D is the first product in the Vault line_

**Strategic Benefits:**

1. **Positioning**: Establishes Excelso as a leader in digital security
2. **Portfolio**: First tangible product in the Vault area
3. **Open Source**: Builds trust and community
4. **Scalable**: Foundation for future products

**Future Opportunities:**

- **Encrypt-D Cloud**: Secure cloud synchronization
- **Encrypt-D Enterprise**: Organization version with centralized management
- **Encrypt-D Mobile**: iOS/Android apps
- **Encrypt-D Team**: Secure team sharing

---

## 🛡️ Security Specifications

| Feature                   | Implementation                      |
| ------------------------- | ----------------------------------- |
| **Encryption Algorithm**  | AES-256-GCM                         |
| **Key Derivation**        | PBKDF2-SHA256                       |
| **Iterations**            | 100,000                             |
| **Salt Size**             | 32 bytes (unique per folder)        |
| **Nonce Size**            | 12 bytes (unique per file)          |
| **Max Attempts**          | Configurable (1-10)                 |
| **Auto-Destruction**      | Optional                            |
| **Hidden Attributes**     | Windows HIDDEN + SYSTEM             |
| **Password Requirements** | Min 8 chars, A-Z, a-z, 0-9, symbols |

---

## 🔄 System Flow Diagrams

### 1. 🔐 Encryption Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FOLDER ENCRYPTION PROCESS                     │
└─────────────────────────────────────────────────────────────────┘

     [User Selects Folder]
              │
              ▼
     ┌─────────────────┐
     │ Validate Folder │ ◄─── Check existence & permissions
     └────────┬────────┘
              │ ✓ Valid
              ▼
     ┌─────────────────┐
     │ Generate Salt   │ ◄─── 32 bytes random (secrets.token_bytes)
     │   (32 bytes)    │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Derive Key from │ ◄─── PBKDF2-SHA256 + Salt + Password
     │  Master Password│      (100,000 iterations)
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Create Unique  │ ◄─── UUID for folder identification
     │   Folder ID     │
     └────────┬────────┘
              │
              ▼
    ┌──────────────────────┐
    │   FOR EACH FILE:     │
    │  ┌────────────────┐  │
    │  │ Generate Nonce │  │ ◄─── 12 bytes unique per file
    │  │  (12 bytes)    │  │
    │  └────────┬───────┘  │
    │           │           │
    │           ▼           │
    │  ┌────────────────┐  │
    │  │ Encrypt File   │  │ ◄─── AES-256-GCM
    │  │  AES-256-GCM   │  │      (Authenticated Encryption)
    │  └────────┬───────┘  │
    │           │           │
    │           ▼           │
    │  ┌────────────────┐  │
    │  │  Save to Vault │  │ ◄─── Store in hidden vault
    │  └────────────────┘  │
    └──────────────────────┘
              │
              ▼
     ┌─────────────────┐
     │ Create Metadata │ ◄─── JSON with file structure,
     │      File       │      original paths, salt, timestamps
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Hide Folder    │ ◄─── Set HIDDEN + SYSTEM attributes
     │  (Windows API)  │      (Not searchable in Explorer)
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Encryption Done │ ◄─── Return folder ID
     │   ✓ Success     │
     └─────────────────┘
              │
              ▼
     [Optional: Delete Original Folder]
```

---

### 2. 🔓 Decryption Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FOLDER DECRYPTION PROCESS                     │
└─────────────────────────────────────────────────────────────────┘

     [User Selects Encrypted Folder]
              │
              ▼
     ┌─────────────────┐
     │  Load Metadata  │ ◄─── Read JSON with folder info
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Verify Password │ ◄─── Check against stored hash
     └────────┬────────┘
              │ ✓ Correct
              ▼
     ┌─────────────────┐
     │ Extract Salt    │ ◄─── From metadata
     │  from Metadata  │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Derive Key from │ ◄─── PBKDF2-SHA256 + Salt + Password
     │  Master Password│      (Same process as encryption)
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Select Output   │ ◄─── User chooses destination
     │   Location      │
     └────────┬────────┘
              │
              ▼
    ┌──────────────────────┐
    │   FOR EACH FILE:     │
    │  ┌────────────────┐  │
    │  │ Extract Nonce  │  │ ◄─── Read from encrypted file header
    │  └────────┬───────┘  │
    │           │           │
    │           ▼           │
    │  ┌────────────────┐  │
    │  │ Decrypt File   │  │ ◄─── AES-256-GCM with key + nonce
    │  │  AES-256-GCM   │  │      (Verifies authentication tag)
    │  └────────┬───────┘  │
    │           │           │
    │           ▼           │
    │  ┌────────────────┐  │
    │  │ Restore Path   │  │ ◄─── Recreate original directory
    │  │   Structure    │  │      structure from metadata
    │  └────────┬───────┘  │
    │           │           │
    │           ▼           │
    │  ┌────────────────┐  │
    │  │  Write File    │  │ ◄─── Save decrypted file
    │  │  to Disk       │  │
    │  └────────────────┘  │
    └──────────────────────┘
              │
              ▼
     ┌─────────────────┐
     │  Verify All     │ ◄─── Check all files decrypted
     │  Files Restored │      successfully
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Decryption Done │ ◄─── Return output path
     │   ✓ Success     │
     └─────────────────┘
```

---

### 3. 🗑️ Deletion Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   SECURE DELETION PROCESS                        │
└─────────────────────────────────────────────────────────────────┘

     [User Selects Folder to Delete]
              │
              ▼
     ┌─────────────────┐
     │  Confirm User   │ ◄─── Show warning dialog
     │    Intention    │      (Permanent action)
     └────────┬────────┘
              │ ✓ Confirmed
              ▼
     ┌─────────────────┐
     │  Locate Folder  │ ◄─── Find in vault by ID
     │    in Vault     │
     └────────┬────────┘
              │
              ▼
    ┌──────────────────────┐
    │  DELETE ALL FILES:   │
    │  ┌────────────────┐  │
    │  │ Overwrite with │  │ ◄─── Security measure
    │  │  Random Data   │  │      (Optional: multiple passes)
    │  └────────┬───────┘  │
    │           │           │
    │           ▼           │
    │  ┌────────────────┐  │
    │  │  Delete File   │  │ ◄─── os.remove()
    │  └────────────────┘  │
    └──────────────────────┘
              │
              ▼
     ┌─────────────────┐
     │  Delete Metadata│ ◄─── Remove JSON configuration
     │      File       │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Delete Folder  │ ◄─── Remove vault directory
     │   from Vault    │      shutil.rmtree()
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Update Vault   │ ◄─── Remove from folder list
     │     Index       │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Deletion Done  │ ◄─── Permanent & irreversible
     │   ✓ Success     │
     └─────────────────┘
```

---

### 4. 🛡️ Security & Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              AUTHENTICATION & AUTO-DESTRUCTION FLOW              │
└─────────────────────────────────────────────────────────────────┘

           [Application Starts]
                    │
                    ▼
          ┌──────────────────┐
          │ Check Auth File  │
          │    Exists?       │
          └────────┬─────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    YES │                     │ NO
        ▼                     ▼
  ┌──────────┐        ┌──────────────┐
  │  Locked? │        │  SETUP MODE  │ ◄─── First time setup
  └────┬─────┘        └──────┬───────┘
       │                     │
   YES │ NO                  ▼
       │  │          ┌──────────────────┐
       │  │          │ Configure:       │
       │  │          │ • Password       │
       │  │          │ • Auto-destroy   │
       │  │          │ • Max attempts   │
       │  │          └──────┬───────────┘
       │  │                 │
       │  │                 ▼
       │  │          ┌──────────────────┐
       │  │          │ Validate Password│ ◄─── Check requirements:
       │  │          │   Strength       │      • Min 8 chars
       │  │          └──────┬───────────┘      • Uppercase (A-Z)
       │  │                 │                  • Lowercase (a-z)
       │  │            ✓ Strong               • Numbers (0-9)
       │  │                 │                  • Symbols
       │  │                 ▼
       │  │          ┌──────────────────┐
       │  │          │  Hash Password   │ ◄─── PBKDF2-SHA256
       │  │          │  & Save Config   │      100k iterations
       │  │          └──────┬───────────┘
       │  │                 │
       │  └─────────────────┴─────┐
       │                          │
       ▼                          ▼
┌─────────────┐          ┌──────────────┐
│LOCKED SCREEN│          │ LOGIN SCREEN │
└──────┬──────┘          └──────┬───────┘
       │                        │
       │                        ▼
       │                ┌──────────────────┐
       │                │ Enter Password   │
       │                └──────┬───────────┘
       │                       │
       │                       ▼
       │                ┌──────────────────┐
       │                │  Hash & Verify   │ ◄─── Compare hashes
       │                └──────┬───────────┘
       │                       │
       │            ┌──────────┴──────────┐
       │            │                     │
       │        CORRECT               INCORRECT
       │            │                     │
       │            ▼                     ▼
       │    ┌──────────────┐      ┌──────────────────┐
       │    │  MAIN SCREEN │      │ Auto-destroy     │
       │    │              │      │  enabled?        │
       │    │ • Add Folder │      └────┬──────┬──────┘
       │    │ • Decrypt    │           │      │
       │    │ • Delete     │       YES │      │ NO
       │    │ • Change PWD │           │      │
       │    └──────────────┘           ▼      ▼
       │                        ┌──────────────────┐
       │                        │ Increment Failed │
       │                        │ Attempts Counter │
       │                        └────┬──────┬──────┘
       │                             │      │
       │                             │      └──────► Unlimited attempts
       │                             │               Show error
       │                             ▼
       │                      ┌──────────────┐
       │                      │  Attempts    │
       │                      │   >= Max?    │
       │                      └──────┬───────┘
       │                             │
       │                   ┌─────────┴─────────┐
       │                   │                   │
       │                  YES                  NO
       │                   │                   │
       │                   ▼                   ▼
       │          ┌──────────────────┐  ┌──────────────┐
       │          │ DESTROY ALL DATA │  │ Show Error   │
       │          │                  │  │ & Remaining  │
       │          │ • Delete vault   │  │  Attempts    │
       │          │ • Lock system    │  └──────────────┘
       │          │ • Reset auth     │
       │          └────────┬─────────┘
       │                   │
       └───────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │  SYSTEM LOCKED   │ ◄─── Show locked screen
          │                  │      Option to reset
          │ All data         │
          │ destroyed        │
          └──────────────────┘
```

---

### 5. 🔄 Password Change Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PASSWORD CHANGE PROCESS                       │
└─────────────────────────────────────────────────────────────────┘

     [User Requests Password Change]
              │
              ▼
     ┌─────────────────┐
     │ Enter Current   │
     │   Password      │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Verify Current  │ ◄─── Hash & compare
     │   Password      │
     └────────┬────────┘
              │ ✓ Correct
              ▼
     ┌─────────────────┐
     │ Enter New       │
     │  Password (2x)  │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Validate New    │ ◄─── Check strength requirements
     │ Password        │      (8+ chars, A-Z, a-z, 0-9, symbols)
     └────────┬────────┘
              │ ✓ Valid
              ▼
     ┌─────────────────┐
     │  Verify Match   │ ◄─── Confirm passwords match
     └────────┬────────┘
              │ ✓ Match
              ▼
     ┌─────────────────┐
     │ Hash New        │ ◄─── PBKDF2-SHA256
     │  Password       │      New salt generated
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Update Auth    │ ◄─── Save new hash & salt
     │     File        │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │ Reset Failed    │ ◄─── Clear attempt counter
     │   Attempts      │
     └────────┬────────┘
              │
              ▼
     ┌─────────────────┐
     │  Change Done    │
     │   ✓ Success     │
     └─────────────────┘

     Note: Encrypted folders remain encrypted
           with the SAME encryption keys.
           Password change only affects authentication.
```

---

## 📊 Project Metrics

| Aspect                  | Value               |
| ----------------------- | ------------------- |
| **Lines of Code**       | ~2,800+             |
| **Python Modules**      | 5 (modular)         |
| **Web Components**      | 6 (Astro)           |
| **Languages Supported** | 2 (EN/ES)           |
| **Translated Strings**  | 53+ per language    |
| **Documentation Files** | 12+                 |
| **Functional Coverage** | 100%                |
| **Status**              | ✅ Production Ready |

---

## 🌈 Technology Stack

### Desktop Application

| Component  | Technology    | Purpose          |
| ---------- | ------------- | ---------------- |
| Language   | Python 3.8+   | Core development |
| GUI        | tkinter       | Native interface |
| Encryption | cryptography  | AES-256-GCM      |
| Hashing    | PBKDF2-SHA256 | Secure passwords |
| Build      | PyInstaller   | Generate .exe    |
| i18n       | Custom        | Multi-language   |

### Web Landing Page

| Component | Technology     | Purpose           |
| --------- | -------------- | ----------------- |
| Framework | Astro 4.16+    | Static generation |
| Language  | TypeScript     | Type safety       |
| Styling   | CSS3           | Modern design     |
| Build     | Vite           | Fast bundling     |
| Hosting   | Vercel/Netlify | Deployment        |

---

## 🎨 Visual Identity

### Color Palette (Implemented)

- **Primary**: Blue (#3b82f6) - Trust and technology
- **Secondary**: Purple (#8b5cf6) - Innovation and security
- **Accent**: Cyan (#06b6d4) - Modernity
- **Background**: Dark Blue (#0f172a) - Professionalism

### Conceptual Logo

```
🔒 ENCRYPT-D
   ─────────
   by EXCELSO OPEN
```

---

## 🗺️ Roadmap

### ✅ Completed (v1.1.0 - Current)

- [x] Functional desktop application
- [x] Professional landing page
- [x] Multi-language system (EN/ES)
- [x] Complete documentation
- [x] Build scripts
- [x] Configurable auto-destruction (1-10 attempts)
- [x] Strong password requirements
- [x] Responsive interface
- [x] Custom icon support

### 🔄 Short Term (v1.2 - Q1 2026)

- [ ] ☁️ Cloud backup & sync (Google Drive, OneDrive, Dropbox)
- [ ] 🔐 Two-factor authentication (2FA)
- [ ] 👤 Biometric authentication (Windows Hello)
- [ ] 📄 File-level encryption
- [ ] Additional languages (FR, DE, PT)
- [ ] Digital installer with signature

### 🎯 Medium Term (v1.3-1.4 - Q2-Q3 2026)

- [ ] 👥 Shared vaults (multi-user)
- [ ] 🗑️ Secure file shredding
- [ ] 🔗 Secure file links (temporary sharing)
- [ ] 📦 Compression before encryption
- [ ] 🖥️ Command-line interface (CLI)
- [ ] 📊 Audit logging
- [ ] Context menu integration

### 🚀 Long Term (v2.0 - 2027+)

- [ ] 💿 Virtual encrypted drive
- [ ] 📱 Mobile apps (iOS/Android)
- [ ] 🌐 Web vault (browser-based)
- [ ] 🤖 AI security assistant
- [ ] 💀 Dead man's switch
- [ ] ⛓️ Blockchain verification
- [ ] 🔌 Plugin system
- [ ] Cross-platform support (macOS, Linux)

---

### 📚 Detailed Roadmap

For comprehensive feature descriptions, technical details, and use cases, see:

- **📖 [ROADMAP.md](ROADMAP.md)** - Detailed English roadmap with technical specifications
- **🇪🇸 [FUTURAS_FUNCIONALIDADES.md](FUTURAS_FUNCIONALIDADES.md)** - Spanish version with examples and priorities

**Want to influence the roadmap?** Vote for features or suggest new ones:

- Email: feedback@excelso.tech
- Landing page contact form

---

## 🤝 Contributing

We welcome contributions from the community! Encrypt-D is open source and part of Excelso's commitment to collaborative development.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- **Code**: Must be in English
- **Comments**: Must be in English
- **UI Strings**: Use i18n system (translatable)
- **Style**: Follow PEP 8 (Python) or project standards
- **Tests**: Add tests for new features
- **Documentation**: Update relevant docs

See [CONTRIBUTING.md](app/docs/en/CONTRIBUTING.md) for detailed guidelines.

---

## 📚 Documentation

### English Documentation

- [Complete README](app/README.md) - Main project documentation
- [Architecture Guide](app/ARCHITECTURE.md) - Architecture details
- [Migration Guide](app/docs/en/MIGRATION_GUIDE.md) - Code migration examples
- [i18n Setup](app/docs/en/I18N_SETUP_SUMMARY.md) - Internationalization guide
- [Contributing](app/docs/en/CONTRIBUTING.md) - Contribution guidelines

### Spanish Documentation

- [README Español](app/docs/es/README-es.md) - Documentación principal
- [Configuración i18n](app/docs/es/CONFIGURACION_MULTILENGUAJE.md) - Sistema multi-idioma
- [Guía Rápida](app/docs/es/INSTRUCCIONES_RAPIDAS.md) - Quick start guide
- [Resumen del Proyecto](app/docs/es/RESUMEN_PROYECTO.md) - Project summary

### Web Documentation

- [Landing Page README](web/README.md) - Web project overview
- [Quick Start](web/QUICKSTART.md) - 3-minute setup guide
- [Deployment Guide](web/DEPLOYMENT.md) - Detailed deployment instructions
- [Features List](web/FEATURES.md) - Complete feature documentation

---

## 🔐 Security Considerations

### What Encrypt-D Protects

✅ Files at rest (stored on disk)  
✅ Against unauthorized physical access  
✅ Against brute force attacks (limited attempts)  
✅ Against casual snooping (hidden folders)

### What Encrypt-D Does NOT Protect

❌ Against keyloggers (hardware/software)  
❌ Against access while you're logged in  
❌ Against sophisticated state-level attacks  
❌ Files in transit (network transmission)

### Best Practices

- Use strong, unique passwords (12+ characters)
- Keep regular backups of important files
- Log out when not using the application
- Keep your system updated and secure
- Don't store password in plain text

---

## 💼 Commercial Message

### For Excelso Website

**Title**: _"Encrypt-D: Enterprise-Level Digital Protection"_

**Short Description**:

> The first security solution from the Vault family. Military-grade encryption for your most important files. Free, open source, and designed with you in mind.

**Call to Action**:

> "Protect your data today. Free download."

### For Marketing

**Headline**: _"What are your secrets worth?"_

**Body**:

> At Excelso, we believe your privacy is priceless. That's why we created Encrypt-D: a military-grade encryption solution, completely free and open source. Because digital security should be a right, not a privilege.

> _Part of Excelso Vault - Your digital vault_

---

## 📞 Support & Contact

### For Issues

- **Bug Reports**: [GitHub Issues](https://github.com/excelso/encrypt-d/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/excelso/encrypt-d/discussions)
- **Security Vulnerabilities**: security@excelso.xyz

### For General Inquiries

- **Website**: https://excelso.xyz
- **Email**: info@excelso.xyz
- **Twitter**: @ExcelsoTech
- **LinkedIn**: Excelso Tech Group

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Excelso Tech Group

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

---

## 🙏 Acknowledgments

### Built With

- **Python** - Core application language
- **Astro** - Web framework for landing page
- **cryptography** - Python cryptography library
- **tkinter** - GUI framework

### Special Thanks

- The open-source community
- Security researchers and auditors
- All contributors and testers
- Excelso team members

---

## 🎉 Project Status

**Current Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: October 10, 2025

### What's Included

✅ Fully functional desktop application  
✅ Professional landing page  
✅ Multi-language support (EN/ES)  
✅ Complete documentation  
✅ Build and deployment scripts  
✅ Automated tests  
✅ Security audited code

---

## 💡 Why Encrypt-D?

**Encrypt-D** represents a complete and professional solution that:

✅ **Solves a Real Problem**: Personal and enterprise data security  
✅ **Demonstrates Technical Excellence**: Modular architecture, clean code, international standards  
✅ **Aligns with Excelso**: "Thinking of you", real solutions, professional quality  
✅ **Launches Vault**: First piece of a security ecosystem  
✅ **Production Ready**: Code, documentation, and landing page complete

It's a perfect **flagship product** to launch Excelso's **Vault** area and demonstrate the tech group's commitment to **innovation, security, and accessibility**.

---

<div align="center">

**Built with ❤️ by Excelso Tech Group**

[Website](https://excelso.xyz) • [Documentation](app/docs/en/README.md) • [Download](https://encrypt-d.excelso.xyz) • [Contribute](CONTRIBUTING.md)

_Part of Excelso Vault - Secure. Private. Yours._

</div>
