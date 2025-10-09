# Contributing to Encrypt-D

Thank you for considering contributing to Encrypt-D! This document provides guidelines for contributing to the project.

## Language Standards

### Code Language: English Only

**All code MUST be written in English:**

- ✅ Variable names: English
- ✅ Function names: English
- ✅ Class names: English
- ✅ Comments: English
- ✅ Docstrings: English
- ✅ Documentation: English

```python
# ✅ GOOD - English code and comments
def encrypt_folder(folder_path: str, password: str) -> bool:
    """Encrypts a folder with the given password.

    Args:
        folder_path: Path to the folder to encrypt
        password: Password for encryption

    Returns:
        True if successful, False otherwise
    """
    # Generate unique salt for this folder
    salt = secrets.token_bytes(32)
    return True

# ❌ BAD - Spanish code
def encriptar_carpeta(ruta_carpeta: str, contraseña: str) -> bool:
    """Encripta una carpeta con la contraseña dada."""
    # Generar sal única para esta carpeta
    sal = secrets.token_bytes(32)
    return True
```

### User Interface: Multi-language

**All user-facing strings must be translatable:**

```python
# ✅ GOOD - Translatable strings
from i18n import translate as t

def show_error():
    messagebox.showerror(
        t("error.title"),
        t("error.folder_not_exist")
    )

# ❌ BAD - Hardcoded strings
def show_error():
    messagebox.showerror(
        "Error",
        "The folder does not exist"
    )
```

## Adding New Features

### 1. Write Code in English

All new code must follow English naming conventions:

```python
# Class names: PascalCase
class CryptoManager:
    pass

# Function names: snake_case
def encrypt_file(file_path: str) -> bytes:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_LOGIN_ATTEMPTS = 3

# Variables: snake_case
file_path = "/path/to/file"
encryption_key = generate_key()
```

### 2. Add Translations

When adding new user-facing strings:

1. **Add to `i18n/en.json` (English):**

```json
{
  "feature": {
    "new_button": "New Feature",
    "success_message": "Feature executed successfully"
  }
}
```

2. **Add to `i18n/es.json` (Spanish):**

```json
{
  "feature": {
    "new_button": "Nueva Función",
    "success_message": "Función ejecutada exitosamente"
  }
}
```

3. **Use in code:**

```python
from i18n import translate as t

button_text = t("feature.new_button")
success_msg = t("feature.success_message")
```

### 3. Write English Comments

```python
# ✅ GOOD - English comments
def _derive_key(self, password: str, salt: bytes) -> bytes:
    """Derives a 256-bit key from the password.

    Uses PBKDF2 with SHA-256 and 100,000 iterations for
    maximum security against brute-force attacks.
    """
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

# ❌ BAD - Spanish comments
def _derivar_clave(self, contraseña: str, sal: bytes) -> bytes:
    """Deriva una clave de 256 bits desde la contraseña.

    Usa PBKDF2 con SHA-256 y 100,000 iteraciones para
    máxima seguridad contra ataques de fuerza bruta.
    """
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sal,
        iterations=100000,
    )
    return kdf.derive(contraseña.encode())
```

## Code Style

### Python Style Guide

- Follow **PEP 8** conventions
- Use **type hints** where appropriate
- Maximum line length: **88 characters**
- Use **double quotes** for strings
- Use **descriptive names** (in English)

### Docstring Format

Use Google-style docstrings:

```python
def encrypt_folder(
    self,
    folder_path: str,
    password: str,
    folder_name: str = None
) -> Tuple[bool, str]:
    """Encrypts a complete folder.

    This function recursively encrypts all files in the folder,
    maintaining the original directory structure in metadata.

    Args:
        folder_path: Path to the folder to encrypt
        password: Password for encryption
        folder_name: Custom name for the folder (optional)

    Returns:
        A tuple containing:
            - bool: True if successful, False otherwise
            - str: Success message or error description

    Raises:
        ValueError: If folder_path does not exist
        PermissionError: If lacking necessary permissions

    Example:
        >>> manager = CryptoManager(vault_dir)
        >>> success, msg = manager.encrypt_folder(
        ...     "/path/to/folder",
        ...     "my_password",
        ...     "Important Files"
        ... )
        >>> if success:
        ...     print(f"Success: {msg}")
    """
    # Implementation here
    pass
```

## Testing

### Write Tests in English

```python
# ✅ GOOD - English test names and comments
def test_encrypt_folder_success():
    """Test that folder encryption succeeds with valid input."""
    manager = CryptoManager(temp_vault)
    success, message = manager.encrypt_folder(
        test_folder_path,
        "test_password",
        "Test Folder"
    )
    assert success is True
    assert "encrypted successfully" in message.lower()

# ❌ BAD - Spanish test names
def test_encriptar_carpeta_exitoso():
    """Prueba que la encriptación de carpeta tenga éxito."""
    pass
```

## Commit Messages

Write commit messages in English:

```bash
# ✅ GOOD
git commit -m "Add multi-language support for UI"
git commit -m "Fix encryption bug with special characters"
git commit -m "Improve error handling in auth manager"

# ❌ BAD
git commit -m "Agregar soporte multi-idioma"
git commit -m "Arreglar bug de encriptación"
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**

```
feat: Add language selector to settings menu

- Add dropdown for language selection
- Save language preference to config
- Update all UI elements on language change

Closes #123
```

## Translation Guidelines

### Adding a New Language

1. Create a new JSON file: `i18n/[language_code].json`
2. Copy the structure from `i18n/en.json`
3. Translate all strings to the new language
4. Update the language selector in the UI

### Translation Best Practices

- **Be consistent**: Use the same terminology throughout
- **Keep it concise**: UI space is limited
- **Test in UI**: Ensure text fits in buttons and labels
- **Context matters**: Consider the context of each string
- **Ask native speakers**: When possible, verify with native speakers

### Translation Keys

Use descriptive, hierarchical keys:

```json
{
  "module": {
    "feature": {
      "action": "Text here"
    }
  }
}
```

Examples:

- `login.button_submit` - Clear and specific
- `error.invalid_password` - Easy to find
- `settings.language.select` - Well organized

## Pull Request Process

1. **Create a branch**: `feature/your-feature-name` or `fix/bug-description`
2. **Write in English**: All code, comments, and commit messages
3. **Add translations**: For any new user-facing strings
4. **Test thoroughly**: Ensure all tests pass
5. **Update documentation**: If needed
6. **Submit PR**: With a clear English description

### PR Description Template

```markdown
## Description

Brief description of changes in English

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made

- List of changes
- In English
- Be specific

## Testing

How was this tested?

## Translations

- [ ] English strings added to en.json
- [ ] Spanish strings added to es.json
- [ ] Tested in both languages

## Checklist

- [ ] Code follows English naming conventions
- [ ] Comments are in English
- [ ] Docstrings are in English
- [ ] User strings are translatable
- [ ] Tests pass
- [ ] Documentation updated
```

## Questions?

If you have questions about:

- **Code standards**: Check `.cursorrules` file
- **Translations**: See `i18n.py` documentation
- **Architecture**: See `RESUMEN_PROYECTO.md`

## Thank You!

Your contributions help make Encrypt-D better for everyone. Thank you for taking the time to contribute and for following our English code standards!

---

**Remember**: We code in English, but we speak to users in their language. 🌍
