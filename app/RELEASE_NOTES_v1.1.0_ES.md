# 🎉 Encrypt-D v1.1.0 - Notas de la Versión

## Resumen Ejecutivo

**Encrypt-D v1.1.0** introduce mejoras significativas en seguridad, flexibilidad y experiencia de usuario. Esta versión mantiene la misma arquitectura robusta de la v1.0.0 mientras agrega opciones de configuración avanzadas y una interfaz más adaptable.

---

## 🌟 Nuevas Características Principales

### 1. ⚙️ Configuración de Seguridad Personalizable

#### Auto-Destrucción Opcional

- **Antes (v1.0)**: La auto-destrucción estaba siempre activada con 3 intentos fijos
- **Ahora (v1.1)**: Los usuarios pueden:
  - ✅ **Activar** auto-destrucción con intentos configurables (1-10)
  - ✅ **Desactivar** auto-destrucción para intentos ilimitados

#### Interfaz de Configuración

Durante el primer setup, aparece una nueva sección **"🛡️ Opciones de Seguridad"** con:

- Checkbox para habilitar/deshabilitar auto-destrucción
- Selector numérico (spinbox) para elegir intentos máximos (1-10)
- Información contextual que cambia según la configuración elegida

#### Casos de Uso

- **Máxima Seguridad**: Auto-destrucción activada con 3 intentos (valor por defecto)
- **Dispositivo Personal**: Auto-destrucción activada con 5-10 intentos para mayor comodidad
- **Entorno Confiable**: Auto-destrucción desactivada para acceso sin límites

---

### 2. 🔐 Requisitos de Contraseña Más Fuertes

#### Nuevas Reglas de Validación

Las contraseñas ahora **DEBEN** cumplir:

- ✅ Mínimo **8 caracteres** (antes: 6)
- ✅ Al menos **1 letra mayúscula** (A-Z)
- ✅ Al menos **1 letra minúscula** (a-z)
- ✅ Al menos **1 número** (0-9)
- ✅ Al menos **1 carácter especial** (!@#$%^&\*...)

#### Validación en Tiempo Real

- Feedback inmediato si la contraseña no cumple requisitos
- Mensajes de error específicos indicando qué falta
- Ejemplo de error: "La contraseña debe contener al menos una letra mayúscula"

#### Ejemplos de Contraseñas

```
❌ "password"     -> No cumple (falta mayúscula, número, símbolo)
❌ "Password1"    -> No cumple (falta símbolo)
✅ "Password1!"   -> Cumple todos los requisitos
✅ "MyV@ult2025"  -> Cumple todos los requisitos
✅ "Secur3#Pass"  -> Cumple todos los requisitos
```

#### Aplicación

- Se aplica durante el setup inicial
- Se aplica al cambiar la contraseña
- **Compatibilidad**: Las contraseñas existentes de v1.0 siguen funcionando

---

### 3. 📐 Interfaz Adaptable y Responsive

#### Tamaño Dinámico de Ventana

**Antes (v1.0)**:

- Ventana fija de 1000x700 píxeles
- No redimensionable
- Problemas en pantallas pequeñas o muy grandes

**Ahora (v1.1)**:

- ✅ Tamaño calculado según resolución de pantalla (80% del tamaño)
- ✅ Máximo de 1400x900 para pantallas grandes
- ✅ Mínimo de 800x600 para pantallas pequeñas
- ✅ Ventana centrada automáticamente
- ✅ **Completamente redimensionable**

#### Mejoras de Usabilidad

- Pantalla de setup con scroll para pantallas pequeñas
- Elementos de UI que se adaptan al tamaño de ventana
- Mejor visualización en laptops, monitores grandes, y tablets

#### Ejemplos de Adaptación

```
📱 Laptop 1366x768  → Ventana: 1093x614 (mínimo ajustado a 800x600)
🖥️ Monitor 1920x1080 → Ventana: 1400x864 (limitado al máximo)
🖥️ 4K 3840x2160    → Ventana: 1400x900 (limitado al máximo)
```

---

### 4. 📊 Diagramas de Flujo Completos

Se agregaron **5 diagramas de flujo detallados** al README principal:

#### 1. 🔐 Flujo de Encriptación

Muestra paso a paso:

- Selección de carpeta
- Generación de salt y derivación de clave
- Encriptación archivo por archivo con AES-256-GCM
- Creación de metadata
- Ocultación de carpeta

#### 2. 🔓 Flujo de Desencriptación

Detalla:

- Carga de metadata
- Verificación de contraseña
- Derivación de clave con salt original
- Desencriptación y restauración de estructura

#### 3. 🗑️ Flujo de Eliminación

Explica:

- Confirmación de usuario
- Sobrescritura segura de datos
- Eliminación permanente de archivos y metadata

#### 4. 🛡️ Flujo de Seguridad y Autenticación

Diagrama completo que incluye:

- Proceso de setup inicial
- Validación de contraseña
- Sistema de intentos fallidos
- Lógica de auto-destrucción
- Flujo con y sin auto-destrucción

#### 5. 🔄 Flujo de Cambio de Contraseña

Muestra:

- Verificación de contraseña actual
- Validación de nueva contraseña
- Actualización de hash y salt
- Nota importante: Las carpetas encriptadas NO se re-encriptan

---

## 🔧 Mejoras Técnicas

### Módulo de Autenticación (`auth_manager.py`)

#### Nuevos Métodos

```python
# Validar fortaleza de contraseña
def validate_password_strength(password: str) -> Tuple[bool, str]

# Verificar si auto-destrucción está habilitada
def is_auto_destroy_enabled() -> bool

# Obtener intentos máximos configurados
def get_max_attempts() -> int
```

#### Métodos Actualizados

```python
# Ahora acepta parámetros de configuración
def set_password(
    password: str,
    auto_destroy_enabled: bool = True,
    max_attempts: int = 3
) -> Tuple[bool, str]

# Respeta configuración de auto-destrucción
def verify_password(password: str) -> Tuple[bool, str]
```

### Interfaz de Usuario (`application.py`)

#### Pantalla de Setup Mejorada

- Canvas con scroll para contenido largo
- Sección de requisitos de contraseña visible
- Sección de opciones de seguridad con:
  - Checkbox para auto-destrucción
  - Spinbox para número de intentos
  - Labels informativos que cambian dinámicamente

#### Pantalla de Login Actualizada

- Muestra contador de intentos solo si auto-destrucción está activada
- Feedback apropiado según configuración de seguridad

#### Ventana Principal Responsive

- Cálculo dinámico de tamaño basado en resolución
- Límites mínimos y máximos apropiados
- Centrado automático en pantalla

### Configuración (`config.py`)

```python
# Nuevas constantes
MIN_LOGIN_ATTEMPTS = 1               # Mínimo configurable
MAX_LOGIN_ATTEMPTS_LIMIT = 10        # Máximo configurable
MAX_LOGIN_ATTEMPTS = 3               # Valor por defecto

# Actualizado
APP_VERSION = "1.1.0"
```

### Traducciones (i18n)

#### Nuevas Strings Agregadas

**Inglés (`en.json`)**: 10+ nuevas traducciones
**Español (`es.json`)**: 10+ nuevas traducciones

Incluyen:

- Opciones de seguridad
- Requisitos de contraseña
- Mensajes informativos sobre intentos
- Labels para configuración

---

## 📈 Estadísticas de Cambios

| Categoría                        | Cambios             |
| -------------------------------- | ------------------- |
| **Archivos Modificados**         | 5                   |
| **Nuevos Métodos**               | 3                   |
| **Líneas de Código Agregadas**   | ~400                |
| **Nuevas Strings de Traducción** | 20+ (10 por idioma) |
| **Nuevas Constantes**            | 2                   |
| **Diagramas Agregados**          | 5                   |
| **Documentación Nueva**          | 450+ líneas         |

---

## 🎯 Casos de Uso Actualizados

### Caso 1: Usuario Paranoico con Máxima Seguridad

```
✅ Auto-destrucción: Activada
✅ Intentos máximos: 1
✅ Contraseña: MyUltr@S3cur3P@ssw0rd!2025
```

→ Un solo intento fallido destruye todos los datos

### Caso 2: Usuario Casual en Entorno Seguro

```
✅ Auto-destrucción: Desactivada
✅ Intentos máximos: N/A
✅ Contraseña: MyP@ssw0rd123
```

→ Intentos ilimitados, ideal para uso personal

### Caso 3: Balance entre Seguridad y Conveniencia

```
✅ Auto-destrucción: Activada
✅ Intentos máximos: 5
✅ Contraseña: Secure#V@ult2025
```

→ Protección contra ataques pero con margen de error

---

## 🔄 Proceso de Actualización

### Para Usuarios de v1.0.0

#### ✅ Compatibilidad Total

- Todas las carpetas encriptadas en v1.0 funcionan en v1.1
- No se requiere re-encriptación
- Configuración de seguridad existente se mantiene (3 intentos, auto-destrucción activada)

#### Nuevas Características Disponibles

- **Contraseñas fuertes**: Solo se aplica al cambiar la contraseña
- **Opciones de seguridad**: Solo configurables en nuevas instalaciones
- **Interfaz responsive**: Disponible inmediatamente

#### Nota Importante

🚨 **Configuración de seguridad no es modificable después del setup inicial**

- Para cambiar opciones de seguridad, se debe resetear la aplicación
- Próxima versión incluirá pantalla de configuración

---

## 🐛 Correcciones de Bugs

- ✅ Ventana demasiado grande en pantallas pequeñas
- ✅ Ventana muy pequeña en pantallas 4K
- ✅ Contador de intentos se mostraba incorrectamente
- ✅ Setup screen no tenía scroll en pantallas pequeñas

---

## 🚧 Limitaciones Conocidas

### Auto-Destrucción No Configurable Post-Setup

- **Limitación**: No se puede cambiar la configuración de auto-destrucción después del setup inicial
- **Workaround**: Resetear aplicación (perdiendo datos encriptados)
- **Planeado para**: v1.2.0 - Pantalla de configuración

### Ventana con Límites Fijos

- **Limitación**: Mínimo 800x600, máximo 1400x900
- **Impacto**: Usuarios con pantallas muy pequeñas o múltiples monitores
- **Planeado para**: v1.2.0 - Perfiles de UI guardados

---

## 🔮 Próximas Características (Roadmap)

### Versión 1.2.0 (Planificada Q1 2026)

- [ ] Pantalla de configuración post-setup
- [ ] Modificar opciones de seguridad sin resetear
- [ ] Más idiomas (Francés, Alemán, Portugués)
- [ ] Temas de color personalizables
- [ ] Exportar/Importar configuración

### Versión 2.0.0 (Planificada Q2-Q3 2026)

- [ ] Encrypt-D Cloud (sincronización)
- [ ] Compresión antes de encriptar
- [ ] Logs de auditoría
- [ ] Integración con menú contextual de Windows
- [ ] Encrypt-D Mobile (iOS/Android)

---

## 📚 Documentación Actualizada

### README Principal

- ✅ Sección de diagramas de flujo
- ✅ Especificaciones de seguridad actualizadas
- ✅ Información sobre Excelso agregada
- ✅ Roadmap completo

### README de App

- ✅ Características v1.1.0 destacadas
- ✅ Sección de experiencia de usuario
- ✅ Ejemplos actualizados

### Nuevo CHANGELOG.md

- ✅ Historial completo de versiones
- ✅ Formato Keep a Changelog
- ✅ Notas de actualización detalladas

---

## 🧪 Testing Recomendado

### Pruebas Funcionales

1. ✅ Setup con auto-destrucción activada (varios valores de intentos)
2. ✅ Setup con auto-destrucción desactivada
3. ✅ Validación de contraseñas débiles/fuertes
4. ✅ Funcionamiento en diferentes resoluciones de pantalla
5. ✅ Encriptar/Desencriptar carpetas (compatibilidad v1.0)
6. ✅ Cambio de contraseña con nuevas reglas

### Pruebas de Seguridad

1. ✅ Verificar que auto-destrucción funciona según configuración
2. ✅ Verificar que intentos ilimitados funcionan correctamente
3. ✅ Verificar rechazo de contraseñas débiles
4. ✅ Verificar persistencia de configuración de seguridad

---

## 👥 Contribuciones

Esta versión fue desarrollada pensando en:

- **Flexibilidad**: Diferentes usuarios, diferentes necesidades de seguridad
- **Seguridad**: Contraseñas más fuertes por defecto
- **Accesibilidad**: Interfaz que se adapta a cualquier pantalla
- **Transparencia**: Documentación clara sobre cómo funciona el sistema

---

## 💬 Feedback y Soporte

¿Encontraste un bug? ¿Tienes una sugerencia?

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: info@excelso.com

---

## 🎉 Agradecimientos

Gracias por usar **Encrypt-D v1.1.0**

> _"Tu privacidad, encriptada con certeza. Seguridad sin compromisos."_

**Parte de Excelso Vault** - Tu bóveda digital segura

---

**Encrypt-D** es código abierto y parte del compromiso de **Excelso** con la innovación, seguridad y accesibilidad tecnológica.

🔗 [GitHub](https://github.com/excelso/encrypt-d) | 🌐 [Excelso](https://excelso.com) | 📖 [Documentación](./docs/)
