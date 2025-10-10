# 🔨 Instrucciones para Reconstruir el .exe

## ✅ Cambios Realizados

### 1. Error de Importación de Tkinter - SOLUCIONADO ✅

**Problema:**

```
cannot import name 'tk' from 'tkinter'
```

**Solución:**
Se agregaron imports adicionales de tkinter en el script de build:

- `--hidden-import=tkinter.ttk`
- `--hidden-import=tkinter.filedialog`
- `--hidden-import=tkinter.messagebox`
- `--hidden-import=_tkinter`

### 2. Branding de Excelso - AGREGADO ✅

**Agregado en `config.py`:**

```python
EXCELSO_COMPANY = "Excelso"
EXCELSO_DOMAIN = "excelso.xyz"
EXCELSO_SLOGAN = "We are solutions. We are EXCELSO"
EXCELSO_URL = "https://excelso.xyz"
```

**Footer en pantalla principal:**

- "Supported by Excelso • We are solutions. We are EXCELSO"
- Link clickeable a excelso.xyz

**Sección en diálogo "About":**

- Supported by Excelso
- Slogan
- Link a website

---

## 🚀 Cómo Reconstruir el .exe

### Opción 1: Usando el Script de Build (Recomendado)

```bash
cd E:\Programacion\Proyectos\personal-projects\encrypt-d\app
python scripts\build.py
```

### Opción 2: Build Manual

Si el script falla, usa este comando directamente:

```powershell
cd E:\Programacion\Proyectos\personal-projects\encrypt-d\app
python -m PyInstaller --name=Encrypt-D --onefile --windowed --icon=icon.ico --clean --noconfirm --add-data="src;src" --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --hidden-import=_tkinter --hidden-import=cryptography --hidden-import=cryptography.hazmat.primitives --hidden-import=cryptography.hazmat.primitives.ciphers --hidden-import=cryptography.hazmat.primitives.ciphers.aead --hidden-import=cryptography.hazmat.primitives.kdf --hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2 main.py
```

---

## 📋 Verificación Post-Build

Después de construir, verifica:

### ✅ 1. El .exe se crea correctamente

```bash
dir dist\Encrypt-D.exe
```

### ✅ 2. El .exe ejecuta sin errores

```bash
cd dist
.\Encrypt-D.exe
```

### ✅ 3. El footer de Excelso aparece

- Abre la aplicación
- En la pantalla principal, busca en la parte inferior:
  - **"Supported by Excelso • We are solutions. We are EXCELSO"**
- Click en "Supported by Excelso" → debe abrir https://excelso.xyz

### ✅ 4. El diálogo "About" incluye Excelso

- En la aplicación, click en el botón **"About"**
- Verifica que aparezca la sección:
  ```
  Supported by Excelso
  We are solutions. We are EXCELSO
  excelso.xyz (clickeable)
  ```

---

## 🐛 Troubleshooting

### Error: "PyInstaller no encontrado"

```bash
pip install pyinstaller==6.3.0
```

### Error: "cryptography no encontrado"

```bash
pip install -r requirements.txt
```

### Error: "Tkinter no funciona"

1. Verifica que Python tenga tkinter instalado:
   ```bash
   python -c "import tkinter; print('Tkinter OK')"
   ```
2. Si falla, reinstala Python con soporte de Tcl/Tk

### El .exe no muestra el footer de Excelso

1. Verifica que realmente usaste la versión actualizada:
   ```bash
   git status
   ```
2. Asegúrate de rebuild con `--clean`:
   ```bash
   python scripts\build.py
   ```
3. Elimina la carpeta `build` y `dist` manualmente:
   ```bash
   rmdir /s /q build dist
   python scripts\build.py
   ```

### El link de Excelso no abre

- Verifica que tienes un navegador predeterminado configurado en Windows
- El módulo `webbrowser` requiere un navegador instalado

---

## 📝 Checklist Completo

- [ ] Eliminé las carpetas `build` y `dist` antiguas
- [ ] Ejecuté `python scripts\build.py` sin errores
- [ ] El .exe se creó en `dist\Encrypt-D.exe`
- [ ] El .exe ejecuta sin error de tkinter
- [ ] El footer "Supported by Excelso" aparece en la pantalla principal
- [ ] El footer es clickeable y abre excelso.xyz
- [ ] El diálogo "About" muestra la sección de Excelso
- [ ] El slogan se muestra correctamente: "We are solutions. We are EXCELSO"

---

## 🎉 ¡Listo!

Si todos los checks están ✅, tu aplicación está lista con:

- ✅ Error de tkinter solucionado
- ✅ Branding de Excelso integrado
- ✅ Links funcionales a excelso.xyz
- ✅ Slogan visible en la aplicación

---

## 📸 Ejemplo Visual

**Footer en pantalla principal:**

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [Lista de carpetas encriptadas]                   │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Supported by Excelso • We are solutions. We are EXCELSO │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Diálogo About:**

```
┌─────────────────────────────────────────────────────┐
│                   About                             │
│                                                     │
│  [Información de la app]                           │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │ Supported by Excelso                          │ │
│  │ We are solutions. We are EXCELSO              │ │
│  │ excelso.xyz ←←← (clickeable)                  │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│              [Close]                                │
└─────────────────────────────────────────────────────┘
```

---

**¿Problemas?** Revisa el archivo `build.log` en la carpeta `app/` para más detalles.

**Última actualización:** Octubre 2025
