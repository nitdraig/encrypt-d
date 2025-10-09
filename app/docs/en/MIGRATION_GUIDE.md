# Migration Guide: Spanish Code to English with i18n

This guide shows how to migrate the existing Spanish code to English code with internationalization support.

## Overview

**Goal:** Convert all Spanish code to English while maintaining Spanish language support through the i18n system.

## Step-by-Step Migration

### Step 1: Import the Translation System

Add to the top of each file:

```python
from i18n import translate as t, get_translator
```

### Step 2: Rename Variables (Spanish → English)

**Before (Spanish):**

```python
def encriptar_carpeta(self, ruta_carpeta: str, contraseña: str) -> Tuple[bool, str]:
    """Encripta una carpeta completa"""
    ruta_origen = Path(ruta_carpeta)

    if not ruta_origen.exists():
        return False, "La carpeta no existe"
```

**After (English):**

```python
def encrypt_folder(self, folder_path: str, password: str) -> Tuple[bool, str]:
    """Encrypts a complete folder"""
    source_path = Path(folder_path)

    if not source_path.exists():
        return False, t("error.folder_not_exist")
```

### Step 3: Convert Comments to English

**Before (Spanish):**

```python
# Generar salt único
salt = secrets.token_bytes(32)

# Derivar clave
key = self._derive_key(password, salt)

# Encriptar todos los archivos
file_mapping = {}
```

**After (English):**

```python
# Generate unique salt
salt = secrets.token_bytes(32)

# Derive encryption key
key = self._derive_key(password, salt)

# Encrypt all files
file_mapping = {}
```

### Step 4: Convert Docstrings to English

**Before (Spanish):**

```python
def _derivar_clave(self, contraseña: str, sal: bytes) -> bytes:
    """Deriva una clave de 256 bits desde la contraseña"""
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sal,
        iterations=100000,
    )
    return kdf.derive(contraseña.encode())
```

**After (English):**

```python
def _derive_key(self, password: str, salt: bytes) -> bytes:
    """Derives a 256-bit key from the password

    Uses PBKDF2 with SHA-256 and 100,000 iterations.

    Args:
        password: User password
        salt: Unique salt bytes

    Returns:
        Derived encryption key (32 bytes)
    """
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())
```

### Step 5: Convert User Messages to i18n

**Before (Spanish hardcoded):**

```python
messagebox.showerror("Error", "La carpeta no existe")
messagebox.showinfo("Éxito", f"Carpeta encriptada exitosamente. ID: {folder_id}")
messagebox.askyesno("Confirmar", "¿Desea eliminar la carpeta original?")
```

**After (English with i18n):**

```python
messagebox.showerror(
    t("error.title"),
    t("error.folder_not_exist")
)

messagebox.showinfo(
    t("success.title"),
    t("success.folder_encrypted", id=folder_id)
)

messagebox.askyesno(
    t("folder.delete_original_title"),
    t("folder.delete_original_message")
)
```

### Step 6: Convert GUI Labels

**Before (Spanish):**

```python
ttk.Label(frame, text="Contraseña (mínimo 6 caracteres):").pack()
password_entry = ttk.Entry(frame, show="*")

ttk.Button(frame, text="Configurar y Continuar", command=setup).pack()
```

**After (English with i18n):**

```python
ttk.Label(frame, text=t("setup.password_label")).pack()
password_entry = ttk.Entry(frame, show="*")

ttk.Button(frame, text=t("setup.button_continue"), command=setup).pack()
```

## Complete Example: Login Screen

### Before (Spanish)

```python
def _show_login_screen(self):
    """Muestra pantalla de inicio de sesión"""
    self._clear_window()

    frame = ttk.Frame(self.root, padding=50)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Título
    ttk.Label(
        frame,
        text="🔒 Encrypt-D",
        style='Title.TLabel'
    ).pack(pady=20)

    ttk.Label(
        frame,
        text="Ingrese su contraseña para acceder",
        style='Subtitle.TLabel'
    ).pack(pady=10)

    # Campo de contraseña
    ttk.Label(frame, text="Contraseña:").pack(pady=(30, 5))
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        password = password_entry.get()

        if not password:
            messagebox.showerror("Error", "Ingrese la contraseña")
            return

        success, message = self.auth_manager.verify_password(password)

        if success:
            self.authenticated = True
            self._show_main_screen()
        else:
            messagebox.showerror("Acceso Denegado", message)

    ttk.Button(frame, text="Iniciar Sesión", command=attempt_login).pack()
```

### After (English with i18n)

```python
def _show_login_screen(self):
    """Shows the login screen"""
    self._clear_window()

    frame = ttk.Frame(self.root, padding=50)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Title
    ttk.Label(
        frame,
        text=t("login.title"),
        style='Title.TLabel'
    ).pack(pady=20)

    ttk.Label(
        frame,
        text=t("login.subtitle"),
        style='Subtitle.TLabel'
    ).pack(pady=10)

    # Password field
    ttk.Label(frame, text=t("login.password_label")).pack(pady=(30, 5))
    password_entry = ttk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        password = password_entry.get()

        if not password:
            messagebox.showerror(
                t("error.title"),
                t("login.error_empty")
            )
            return

        success, message = self.auth_manager.verify_password(password)

        if success:
            self.authenticated = True
            self._show_main_screen()
        else:
            messagebox.showerror(
                t("login.access_denied"),
                message
            )

    ttk.Button(
        frame,
        text=t("login.button_login"),
        command=attempt_login
    ).pack()
```

## Common Patterns

### Pattern 1: Error Messages

```python
# Before
return False, "Error al encriptar: " + str(e)

# After
return False, t("error.encrypt_failed", error=str(e))
```

### Pattern 2: Success Messages with Variables

```python
# Before
return True, f"Carpeta encriptada exitosamente. ID: {folder_id}"

# After
return True, t("success.folder_encrypted", id=folder_id)
```

### Pattern 3: Confirmation Dialogs

```python
# Before
response = messagebox.askyesno(
    "Confirmar",
    f"¿Desea encriptar la carpeta '{folder_name}'?"
)

# After
response = messagebox.askyesno(
    t("folder.confirm_encrypt_title"),
    t("folder.confirm_encrypt_message", name=folder_name)
)
```

### Pattern 4: TreeView Columns

```python
# Before
self.folder_tree.heading('name', text='Nombre')
self.folder_tree.heading('status', text='Estado')

# After
self.folder_tree.heading('name', text=t("main.column_name"))
self.folder_tree.heading('status', text=t("main.column_status"))
```

## Translation File Structure

Keep translations organized by feature:

```json
{
  "app": {
    "name": "...",
    "version": "..."
  },
  "login": {
    "title": "...",
    "subtitle": "...",
    "button_login": "..."
  },
  "error": {
    "title": "...",
    "folder_not_exist": "...",
    "encrypt_failed": "..."
  }
}
```

## Testing After Migration

1. **Test English UI:**

```python
from i18n import set_language
set_language("en")
# Run application
```

2. **Test Spanish UI:**

```python
from i18n import set_language
set_language("es")
# Run application
```

3. **Test Missing Translations:**
   - If a key is missing, it returns the key itself
   - Check console for missing translation warnings

## Checklist for Each File

- [ ] All variable names converted to English
- [ ] All function names converted to English
- [ ] All class names converted to English (if any)
- [ ] All comments converted to English
- [ ] All docstrings converted to English
- [ ] All user-facing strings use `t()` function
- [ ] No hardcoded Spanish strings remain
- [ ] Translation keys added to both `en.json` and `es.json`
- [ ] File tested in both languages

## Benefits After Migration

✅ **Code readability**: English is the standard for programming  
✅ **International collaboration**: Easier for global developers  
✅ **Maintainability**: Consistent codebase  
✅ **User satisfaction**: Each user sees their language  
✅ **Scalability**: Easy to add more languages

## Need Help?

- Check `.cursorrules` for project standards
- See `CONTRIBUTING.md` for contribution guidelines
- Review `i18n.py` for translation system documentation

---

**Remember**: Code in English, translate for users! 🌍
