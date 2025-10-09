# 🚀 Instrucciones Rápidas - Encrypt-D

## ⚡ Inicio Rápido

### Opción 1: Ejecutar directamente (Sin compilar)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
python main.py
```

### Opción 2: Crear ejecutable .exe

```bash
# Ejecutar el script de construcción
build.bat

# O manualmente:
python build.py
```

El archivo `Encrypt-D.exe` estará en la carpeta `dist/`

## 📝 Uso Básico

1. **Primera vez**: Configura una contraseña maestra
2. **Agregar carpeta**: Click en "➕ Agregar Carpeta"
3. **Desencriptar**: Selecciona carpeta → "🔓 Desencriptar"
4. **Eliminar**: Selecciona carpeta → "🗑️ Eliminar"

## ⚠️ IMPORTANTE

- **Máximo 3 intentos fallidos** → Destrucción automática de datos
- **No hay recuperación** de contraseña
- **Guarda tu contraseña** en un lugar seguro
- **Haz respaldos** de archivos importantes

## 🔒 Características Principales

✅ Encriptación AES-256  
✅ Carpetas ocultas del sistema  
✅ Auto-destrucción por seguridad  
✅ Interfaz gráfica moderna  
✅ Sin instalación (modo .exe)

## 📂 ¿Dónde están mis datos?

Los datos encriptados se guardan en:

```
%APPDATA%\Encrypt-D\vault\
```

Esta carpeta está oculta del sistema de archivos de Windows.

## 🆘 Solución Rápida de Problemas

**No inicia:**

```bash
pip install --upgrade -r requirements.txt
```

**Error al compilar:**

```bash
pip install --upgrade pyinstaller
```

**Sistema bloqueado:**

- Los datos han sido destruidos por seguridad
- Reinicia la aplicación para configurar nuevamente

## 📞 Más Información

Ver `README.md` para documentación completa.

---

**¡Protege tus archivos con Encrypt-D!** 🔒
