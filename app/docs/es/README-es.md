# 🔒 Encrypt-D

**Gestor de Carpetas Encriptadas para Windows**

Encrypt-D es una aplicación de escritorio segura que permite encriptar y proteger carpetas completas con contraseña, manteniéndolas ocultas y protegidas contra accesos no autorizados.

## ✨ Características

### 🔐 Seguridad Robusta
- **Encriptación AES-256-GCM**: Estándar militar para máxima seguridad
- **Hash de contraseñas con PBKDF2**: 100,000 iteraciones con SHA-256
- **Salt único por carpeta**: Cada carpeta tiene su propia clave derivada
- **Protección contra fuerza bruta**: Sistema de intentos limitados

### 🛡️ Auto-destrucción
- Después de 3 intentos fallidos de contraseña, todos los datos son destruidos automáticamente
- No hay forma de recuperar datos sin la contraseña correcta
- Protección total contra accesos no autorizados

### 📁 Gestión de Carpetas
- Encripta carpetas completas con todos sus archivos y subcarpetas
- Mantiene la estructura original al desencriptar
- Las carpetas encriptadas están ocultas del sistema
- No se pueden encontrar con el buscador de Windows

### 🎨 Interfaz Moderna
- Interfaz gráfica intuitiva y fácil de usar
- Diseño moderno con tema oscuro
- Lista visual de carpetas encriptadas
- Operaciones simples: agregar, desencriptar, eliminar

## 📋 Requisitos

- **Sistema Operativo**: Windows 10/11
- **Python**: 3.8 o superior (para desarrollo/compilación)
- **Dependencias**: Ver `requirements.txt`

## 🚀 Instalación

### Opción 1: Usar el Ejecutable (Recomendado)

1. Descarga el archivo `Encrypt-D.exe`
2. Ejecuta el archivo
3. ¡Listo! No requiere instalación

### Opción 2: Desde el Código Fuente

1. **Clonar o descargar el repositorio**

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
python main.py
```

## 🔨 Compilar el Ejecutable

Si deseas compilar tu propio ejecutable:

### Método 1: Script de Construcción (Windows)
```bash
build.bat
```

### Método 2: Python
```bash
python build.py
```

### Método 3: Manual con PyInstaller
```bash
pyinstaller --name=Encrypt-D --onefile --windowed --clean main.py
```

El ejecutable se generará en la carpeta `dist/`

## 📖 Uso

### Primera Vez

1. **Configurar Contraseña Maestra**
   - Al iniciar por primera vez, se te pedirá crear una contraseña maestra
   - Esta contraseña protegerá todas tus carpetas encriptadas
   - ⚠️ **IMPORTANTE**: Guarda esta contraseña en un lugar seguro
   - No hay forma de recuperarla si la olvidas

2. **Configuración de Seguridad**
   - El sistema permite máximo 3 intentos fallidos
   - Después del tercer intento, todos los datos serán destruidos
   - Esta es una medida de seguridad contra accesos no autorizados

### Encriptar una Carpeta

1. Click en **"➕ Agregar Carpeta"**
2. Selecciona la carpeta que deseas proteger
3. Ingresa un nombre personalizado (opcional)
4. Confirma la encriptación
5. Opcionalmente, elimina la carpeta original

La carpeta será encriptada y guardada de forma segura en la bóveda oculta.

### Desencriptar una Carpeta

1. Selecciona la carpeta de la lista
2. Click en **"🔓 Desencriptar"**
3. Elige dónde restaurar la carpeta
4. La carpeta será desencriptada con su contenido original

### Eliminar una Carpeta

1. Selecciona la carpeta de la lista
2. Click en **"🗑️ Eliminar"**
3. Confirma la eliminación

⚠️ **Esta acción es permanente y no se puede deshacer**

### Cambiar Contraseña

1. Click en **"Cambiar Contraseña"** en el menú superior
2. Ingresa tu contraseña actual
3. Ingresa y confirma la nueva contraseña

## 🏗️ Arquitectura del Proyecto

```
encrypt-d/
│
├── main.py              # Punto de entrada principal
├── gui.py               # Interfaz gráfica (tkinter)
├── crypto_manager.py    # Gestión de encriptación/desencriptación
├── auth_manager.py      # Gestión de autenticación
├── config.py            # Configuración global
│
├── requirements.txt     # Dependencias Python
├── build.py            # Script de compilación
├── build.bat           # Script de compilación (Windows)
│
└── README.md           # Este archivo
```

## 🔧 Componentes Técnicos

### Encriptación
- **Algoritmo**: AES-256 en modo GCM (Galois/Counter Mode)
- **Derivación de clave**: PBKDF2 con SHA-256
- **Iteraciones**: 100,000 para máxima seguridad
- **Salt**: 32 bytes aleatorios por carpeta
- **Nonce**: 12 bytes únicos por archivo

### Almacenamiento
- Los datos encriptados se guardan en:
  - Windows: `%APPDATA%\Encrypt-D\vault\`
- La carpeta está oculta con atributos HIDDEN + SYSTEM
- Metadata en formato JSON cifrado

### Autenticación
- Hash de contraseña con PBKDF2-SHA256
- Salt único de 32 bytes
- Contador de intentos fallidos persistente
- Bloqueo automático tras intentos máximos

## 🔒 Consideraciones de Seguridad

### ✅ Lo que Encrypt-D HACE:
- Encripta todos los archivos con AES-256
- Oculta las carpetas encriptadas del sistema
- Protege contra intentos de fuerza bruta
- Destruye datos tras intentos fallidos
- Usa estándares criptográficos modernos

### ⚠️ Lo que Encrypt-D NO HACE:
- No protege contra keyloggers o malware
- No protege si alguien tiene acceso físico con tu sesión iniciada
- No protege contra ataques a nivel de sistema operativo
- No es un reemplazo de copias de seguridad

### 🛡️ Mejores Prácticas

1. **Contraseña Fuerte**
   - Usa al menos 12 caracteres
   - Combina letras, números y símbolos
   - No uses información personal

2. **Respaldo**
   - Mantén copias de seguridad de archivos importantes
   - La auto-destrucción es permanente

3. **Seguridad del Sistema**
   - Usa antivirus actualizado
   - Mantén Windows actualizado
   - No compartas tu sesión de usuario

4. **Privacidad**
   - Cierra sesión cuando no uses la aplicación
   - No dejes la carpeta desencriptada sin supervisión

## 🚨 Recuperación de Emergencia

### Si olvidaste tu contraseña:
**No hay forma de recuperarla.** Los datos estarán permanentemente inaccesibles. Por eso es crucial guardar la contraseña en un lugar seguro.

### Si el sistema se bloqueó:
Si se excedieron los intentos, todos los datos han sido destruidos por seguridad. Puedes reiniciar la aplicación desde cero, pero los datos anteriores no se pueden recuperar.

### Si necesitas mover tus datos:
Los datos encriptados están en `%APPDATA%\Encrypt-D\`. Puedes copiar esta carpeta a otra computadora, pero necesitarás la contraseña para acceder.

## 🔄 Escalabilidad

El proyecto está diseñado para ser escalable:

### Características Futuras Posibles:
- [ ] Múltiples perfiles de usuario
- [ ] Encriptación de archivos individuales
- [ ] Soporte para unidades USB
- [ ] Sincronización en la nube (encriptada)
- [ ] Autenticación de dos factores (2FA)
- [ ] Compresión antes de encriptar
- [ ] Logs de acceso
- [ ] Modo portable (sin instalación)

### Extensiones:
- El código está modularizado para fácil extensión
- Cada componente (crypto, auth, gui) es independiente
- Se pueden agregar nuevos métodos de encriptación
- Se pueden implementar diferentes backends de almacenamiento

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que tienes Python 3.8+ instalado
- Asegúrate de que las dependencias están instaladas
- Ejecuta: `pip install -r requirements.txt`

### Error al encriptar
- Verifica que tienes permisos de escritura
- Asegúrate de que la carpeta no esté en uso
- Verifica que hay espacio suficiente en disco

### El ejecutable no funciona
- Recompila con `build.py`
- Verifica que PyInstaller está instalado
- Prueba ejecutar primero con Python

### Los datos no aparecen
- Verifica que estás usando la contraseña correcta
- Asegúrate de no haber excedido los intentos
- Revisa que la carpeta `%APPDATA%\Encrypt-D\` existe

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

## ⚖️ Disclaimer

Este software se proporciona "tal cual", sin garantías de ningún tipo. El autor no se hace responsable por pérdida de datos, mal uso o cualquier daño derivado del uso de esta aplicación. Usa bajo tu propio riesgo.

**Importante:** Este software incluye funcionalidades de destrucción de datos. Asegúrate de entender completamente cómo funciona antes de usarlo con datos importantes.

## 👨‍💻 Desarrollo

### Estructura del Código

- **`main.py`**: Entry point, inicializa la GUI
- **`gui.py`**: Toda la lógica de interfaz con tkinter
- **`crypto_manager.py`**: Lógica de encriptación/desencriptación
- **`auth_manager.py`**: Gestión de contraseñas y autenticación
- **`config.py`**: Configuraciones globales

### Contribuir

Si deseas mejorar Encrypt-D:

1. Haz un fork del proyecto
2. Crea una rama para tu feature
3. Implementa tus cambios
4. Prueba exhaustivamente
5. Envía un pull request

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

---

**Encrypt-D v1.0.0** - Protege lo que importa 🔒

Desarrollado con ❤️ para la seguridad y privacidad de tus datos.

