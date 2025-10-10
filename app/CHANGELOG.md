# Changelog

All notable changes to Encrypt-D will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-10

### 🎉 New Features

#### Configurable Security Settings

- **Optional Auto-Destruction**: Users can now choose whether to enable or disable the auto-destruction feature during setup
- **Customizable Max Attempts**: When auto-destruction is enabled, users can configure the maximum number of failed login attempts (1-10)
- **Unlimited Attempts Mode**: When auto-destruction is disabled, users can have unlimited login attempts
- Security settings are configured during initial setup and stored persistently

#### Enhanced Password Security

- **Stronger Password Requirements**: Passwords now require minimum 8 characters instead of 6
- **Password Complexity Validation**:
  - At least one uppercase letter (A-Z)
  - At least one lowercase letter (a-z)
  - At least one number (0-9)
  - At least one special character (!@#$%^&\*...)
- **Real-time Validation**: Immediate feedback when password doesn't meet requirements
- **Password Strength Indicator**: Visual feedback during password creation
- Applies to both initial setup and password changes

#### Responsive User Interface

- **Adaptive Window Size**: Window automatically adapts to screen resolution (80% of screen, max 1400x900)
- **Centered Window**: Application window opens centered on screen
- **Resizable Interface**: Users can now resize the window (minimum 800x600)
- **Scrollable Setup Screen**: Setup screen with scrolling support for smaller displays
- **Optimized Layout**: Interface elements scale properly with window size
- Improves usability on different screen sizes and resolutions

### 📚 Documentation

#### Comprehensive Flow Diagrams

Added detailed ASCII flow diagrams to main README:

- **Encryption Flow**: Complete step-by-step encryption process
- **Decryption Flow**: Detailed decryption and restoration process
- **Deletion Flow**: Secure deletion workflow
- **Security & Authentication Flow**: Full authentication system including auto-destruction logic
- **Password Change Flow**: Password update process

#### Updated Documentation

- Updated all README files with new v1.1.0 features
- Added security specifications table with new configurable options
- Enhanced feature descriptions
- Added visual markers for new features (⭐ NEW in v1.1)

### 🔧 Technical Improvements

#### Authentication System

- New `validate_password_strength()` method in AuthManager
- Enhanced `set_password()` to accept security configuration parameters
- Modified `verify_password()` to respect auto-destruction settings
- Added `is_auto_destroy_enabled()` and `get_max_attempts()` methods
- Auto-destruction settings stored in auth data file

#### User Interface

- Redesigned setup screen with security options section
- Added checkbox for auto-destruction toggle
- Added spinbox for attempts configuration (1-10 range)
- Dynamic UI that shows/hides options based on auto-destruction setting
- Conditional display of attempt counter on login screen
- Password requirements display in setup screen

#### Configuration

- Added `MIN_LOGIN_ATTEMPTS` constant (1)
- Added `MAX_LOGIN_ATTEMPTS_LIMIT` constant (10)
- Updated `MAX_LOGIN_ATTEMPTS` to be configurable default (3)
- Version bumped to 1.1.0

#### Translations

- Added 10+ new translation strings in English
- Added 10+ new translation strings in Spanish
- Updated password labels to reflect new requirements
- Added security options translations
- Added password requirements detailed explanations

### 🐛 Bug Fixes

- Fixed window sizing on high-resolution displays
- Improved scroll handling on setup screen
- Fixed attempt counter display when auto-destruction is disabled

### 💡 User Experience Improvements

- Better visual feedback during setup
- Clear explanation of security options
- Informative tooltips and help text
- More intuitive security configuration
- Improved accessibility with resizable windows

### 🔒 Security Enhancements

- Stronger password policy enforcement
- More flexible security configuration
- Better protection against weak passwords
- Maintained backward compatibility with existing vaults

---

## [1.0.0] - 2025-10-09

### Initial Release

#### Core Features

- AES-256-GCM encryption for folders
- PBKDF2-SHA256 password hashing (100,000 iterations)
- Auto-destruction after 3 failed attempts
- Hidden folders (Windows HIDDEN + SYSTEM attributes)
- Multi-language support (English/Spanish)
- Modular architecture (Screaming Architecture)

#### User Interface

- Modern dark theme GUI
- Folder management (add, decrypt, delete)
- Password management (setup, change)
- Language selector
- About dialog

#### Security

- Military-grade encryption
- Secure password storage
- Protected vault directory
- Metadata encryption
- Unique salt per folder
- Unique nonce per file

#### Documentation

- Comprehensive README
- Multi-language documentation (EN/ES)
- Architecture documentation
- Contributing guidelines
- Migration guides
- Quick start guides

---

## Release Notes

### Version 1.1.0 Highlights

This release focuses on **flexibility and security**:

1. **Flexible Security**: Users can now choose their preferred security level, from maximum protection with auto-destruction to convenience with unlimited attempts.

2. **Stronger Passwords**: Enhanced password requirements ensure better protection against unauthorized access.

3. **Better Usability**: Responsive interface adapts to different screen sizes, making the application more accessible.

4. **Clear Documentation**: Comprehensive flow diagrams help users understand exactly how their data is protected.

### Upgrade Notes

- **Existing Users**: Your current vaults remain fully compatible. The new features only affect new setups.
- **Password Changes**: If you change your password after upgrading, the new strength requirements will apply.
- **Security Settings**: Existing installations maintain their current security settings (3 attempts, auto-destruction enabled).

### Breaking Changes

**None** - This release is fully backward compatible with v1.0.0 vaults and configurations.

### Known Issues

- Auto-destruction settings can only be configured during initial setup (not changeable after setup)
- Window resize has minimum bounds (800x600) but no maximum on some displays

### Future Plans

See the main README for the complete roadmap. Coming in future versions:

- Settings screen to modify security options after setup
- Biometric authentication options
- Cloud synchronization (Encrypt-D Cloud)
- Mobile applications (iOS/Android)
- Enterprise version with team management

---

**For more information, visit the [GitHub repository](https://github.com/excelso/encrypt-d)**

**Part of Excelso Vault** - Your Digital Security Solution
