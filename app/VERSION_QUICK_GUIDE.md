# 🚀 Guía Rápida - Sistema de Versionado

## ¿Qué es esto?

Encrypt-D ahora **detecta automáticamente** cuando instalas una versión nueva y **migra tus datos sin pérdida**.

---

## ✅ Lo Que Hace Automáticamente

1. **Detecta** cuando actualizas la app
2. **Crea backup** de todos tus datos
3. **Migra** los datos al nuevo formato
4. **Mantiene** tus carpetas encriptadas intactas

---

## 🎬 ¿Cómo Funciona?

### Primera Instalación (v1.1.0)

```
1. Instalas Encrypt-D v1.1.0
2. Creas tu contraseña
3. Encriptas carpetas
4. Se guarda: version.json → "1.1.0"
```

### Actualización (v1.1.0 → v1.2.0)

```
1. Instalas Encrypt-D v1.2.0
2. Abres la app
3. ¡AUTOMÁTICO! →
   ┌─────────────────────────────────┐
   │  🔄 Update Detected             │
   │                                 │
   │  v1.1.0 → v1.2.0                │
   │                                 │
   │  Your data will be migrated     │
   │  A backup will be created       │
   │                                 │
   │  [Update Now]   [Exit]          │
   └─────────────────────────────────┘
4. Haces click en "Update Now"
5. Se crea backup automático
6. Se migran tus datos
7. ✅ Listo! App funciona con v1.2.0
```

---

## 📁 ¿Dónde Están Mis Datos?

### Ubicación Principal

```
%APPDATA%\Encrypt-D\
├── auth.dat          ← Tu contraseña
├── version.json      ← Versión instalada
├── vault\            ← Tus carpetas encriptadas
└── backups\          ← Respaldos automáticos
    ├── backup_v1.1.0_20251010_120000\
    ├── backup_v1.1.0_20251011_150000\
    └── backup_v1.2.0_20251012_180000\
```

### Acceso Rápido

```bash
# Abrir carpeta de datos
Win+R → %APPDATA%\Encrypt-D
```

---

## 🛡️ ¿Mis Datos Están Seguros?

### SÍ - Triple Protección:

1. **Backup Automático** antes de cualquier cambio
2. **Migración Probada** para cada versión
3. **Recuperación Manual** siempre disponible

---

## 🔄 Restaurar Backup Manual

Si algo sale mal (muy raro):

```bash
# 1. Cerrar Encrypt-D

# 2. Abrir carpeta de backups
Win+R → %APPDATA%\Encrypt-D\backups

# 3. Elegir el backup (ej: backup_v1.1.0_20251010_120000)

# 4. Copiar TODO el contenido a la carpeta padre
# Seleccionar: auth.dat, version.json, vault\
# Copiar a: %APPDATA%\Encrypt-D\

# 5. Abrir Encrypt-D
```

---

## ❓ Preguntas Frecuentes

### ¿Puedo usar una versión antigua después de actualizar?

**NO.** Una vez migrado a v1.2, no puedes volver a v1.1 sin restaurar el backup.

### ¿Pierdo mis carpetas encriptadas?

**NO.** Tus carpetas encriptadas se mantienen intactas. Solo se actualiza el formato de configuración si es necesario.

### ¿Qué pasa si falla la migración?

1. Tu backup está seguro en `backups/`
2. La app te mostrará un error
3. Puedes restaurar el backup manualmente
4. Reporta el error para que lo arreglemos

### ¿Cuántos backups se guardan?

Por defecto, se mantienen los **últimos 5 backups**. Los más antiguos se eliminan automáticamente.

### ¿Ocupan mucho espacio los backups?

Depende de cuántos datos tengas. Ejemplo:

- 10 carpetas pequeñas: ~50 MB por backup
- 100 archivos grandes: ~500 MB por backup

---

## 🎯 Recomendaciones

### ✅ DO

- Deja que la app haga backups automáticos
- Guarda un backup externo importante antes de actualizar
- Actualiza cuando haya una versión nueva

### ❌ DON'T

- No borres la carpeta `backups/` manualmente
- No uses versiones antiguas después de migrar
- No modifiques `version.json` manualmente

---

## 📋 Checklist de Actualización

Cuando veas el diálogo de migración:

- [ ] Lee el mensaje
- [ ] Asegúrate de tener espacio en disco (para el backup)
- [ ] Click en "Update Now"
- [ ] Espera a que termine (unos segundos)
- [ ] ✅ Listo!

---

## 🆘 Si Algo Sale Mal

1. **No entres en pánico** - tus datos están respaldados
2. **Cierra la app**
3. **Ve a** `%APPDATA%\Encrypt-D\backups`
4. **Restaura** el backup más reciente
5. **Reporta el problema** con detalles

---

## 🚀 Próximas Versiones

### Planeado

- **v1.2.0** (Q1 2026): Cloud backup, 2FA
- **v1.3.0** (Q2 2026): File-level encryption
- **v2.0.0** (2027): Mobile app, cross-platform

### Mejoras Futuras del Sistema de Versionado

- Auto-update desde internet
- UI para gestionar backups
- Roll-back automático si falla
- Progress bar para migraciones largas

---

## 📞 Soporte

¿Problemas con la migración?

- **Email:** support@excelso.xyz
- **Documentación:** `VERSION_SYSTEM.md`
- **GitHub:** [Issues](https://github.com/excelso/encrypt-d/issues)

---

**Versión del documento:** 1.0  
**Última actualización:** Octubre 2025
