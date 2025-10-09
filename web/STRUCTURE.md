# 🗂️ Estructura Visual del Proyecto

## 📊 Vista General

```
web/
│
├── 📄 Archivos de Configuración
│   ├── package.json          → Dependencias y scripts npm
│   ├── astro.config.mjs      → Configuración de Astro (i18n, site)
│   ├── tsconfig.json         → Configuración TypeScript
│   ├── netlify.toml          → Deploy config para Netlify
│   ├── vercel.json           → Deploy config para Vercel
│   └── .prettierrc           → Formateo de código
│
├── 📚 Documentación
│   ├── README.md             → Documentación principal
│   ├── QUICKSTART.md         → Guía inicio rápido (3 min)
│   ├── DEPLOYMENT.md         → Guías de despliegue
│   ├── FEATURES.md           → Lista completa de features
│   ├── PROJECT_SUMMARY.md    → Resumen ejecutivo
│   └── STRUCTURE.md          → Este archivo
│
├── 📁 src/                   → Código fuente
│   │
│   ├── 🧩 components/        → Componentes reutilizables
│   │   ├── Hero.astro        → Sección principal con CTA
│   │   ├── Features.astro    → 6 tarjetas de características
│   │   ├── Security.astro    → Especificaciones de seguridad
│   │   ├── Download.astro    → Opciones de descarga
│   │   ├── Navigation.astro  → Barra de navegación fija
│   │   └── Footer.astro      → Pie de página
│   │
│   ├── 📐 layouts/           → Layouts de página
│   │   └── Layout.astro      → Layout base (HTML, estilos globales)
│   │
│   ├── 📄 pages/             → Rutas del sitio
│   │   ├── index.astro       → / (Página principal - inglés)
│   │   └── es.astro          → /es (Página en español)
│   │
│   └── 🌍 i18n/              → Sistema de traducción
│       ├── en.json           → 53+ traducciones inglés
│       ├── es.json           → 53+ traducciones español
│       └── utils.ts          → Utilidades i18n (getLang, useTranslations)
│
├── 📦 public/                → Archivos estáticos
│   └── favicon.svg           → Ícono del sitio
│
├── 🏗️ dist/                  → Build output (generado por `npm run build`)
│   ├── index.html            → Página inglés compilada
│   ├── es/index.html         → Página español compilada
│   ├── _astro/*.css          → Estilos optimizados
│   └── favicon.svg           → Favicon copiado
│
└── 📦 node_modules/          → Dependencias instaladas (468 packages)
```

---

## 🎨 Flujo de Componentes

```
┌─────────────────────────────────────────────────┐
│                  Layout.astro                    │
│  (HTML base + estilos globales + meta tags)     │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │           Navigation.astro                 │ │
│  │  (Barra fija con links y cambio idioma)   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │              Hero.astro                    │ │
│  │  • Título con gradiente                    │ │
│  │  • Descripción                            │ │
│  │  • Botones CTA                            │ │
│  │  • Card flotante con métricas             │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │            Features.astro                  │ │
│  │  • Grid de 6 características              │ │
│  │  • Iconos y descripciones                 │ │
│  │  • Efectos hover                          │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │            Security.astro                  │ │
│  │  • 4 specs técnicos                       │ │
│  │  • Lista de 6 features                    │ │
│  │  • Diseño tipo dashboard                  │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │            Download.astro                  │ │
│  │  • 2 opciones de descarga                 │ │
│  │  • Requisitos del sistema                 │ │
│  │  • Botones de acción                      │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │             Footer.astro                   │ │
│  │  • Links organizados                       │ │
│  │  • Información de contacto                 │ │
│  │  • Copyright                              │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 🌐 Sistema de Rutas

```
Dominio: https://encrypt-d.com
│
├── / (Raíz)
│   └── Renderiza: src/pages/index.astro
│       └── Idioma: Inglés (en)
│           └── Usa: src/i18n/en.json
│
└── /es
    └── Renderiza: src/pages/es.astro
        └── Idioma: Español (es)
            └── Usa: src/i18n/es.json
```

---

## 📋 Scripts Disponibles

```bash
┌─────────────────────────────────────────────────┐
│ npm run dev                                     │
│ → Inicia servidor desarrollo (puerto 4321)     │
│ → Hot reload habilitado                        │
│ → Usa: astro dev                               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ npm run build                                   │
│ → Compila sitio para producción               │
│ → Genera archivos en /dist                    │
│ → Usa: astro check && astro build             │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ npm run preview                                 │
│ → Preview del build de producción             │
│ → Requiere: npm run build primero             │
│ → Usa: astro preview                           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ npm run astro check                            │
│ → Verifica errores TypeScript                  │
│ → No compila, solo revisa                     │
│ → Usa: @astrojs/check                          │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Sistema de Estilos

### Arquitectura CSS

```
Layout.astro (estilos globales)
│
├── :root variables
│   ├── Colores (primary, secondary, accent, etc.)
│   ├── Gradientes
│   └── Espaciados
│
├── Reset global
│   ├── Box-sizing
│   ├── Margin/Padding
│   └── Font-smoothing
│
├── Base styles
│   ├── Body (fondo, texto)
│   ├── Tipografía (h1-h6)
│   ├── Links
│   └── Utilidades (.container, .section)
│
└── Media queries
    └── Responsive breakpoints

Cada Componente.astro
│
└── <style> scoped
    ├── Estilos específicos del componente
    ├── Usa variables CSS del global
    ├── Hover effects
    └── Animaciones locales
```

---

## 🌍 Sistema i18n

### Flujo de Traducción

```
1. Usuario visita página
   │
   ├── URL: / → Idioma: 'en'
   └── URL: /es → Idioma: 'es'
   
2. Página carga i18n/utils.ts
   │
   └── useTranslations(lang)
       └── Retorna función t(key)

3. Componente usa t(key)
   │
   ├── Ejemplo: t('hero.title')
   │
   └── Busca en i18n/{lang}.json
       │
       ├── en.json: "hero.title" → "Encrypt-D"
       └── es.json: "hero.title" → "Encrypt-D"

4. Renderiza texto traducido
   └── HTML: <h1>Encrypt-D</h1>
```

### Estructura JSON

```json
{
  "nav": {
    "features": "Features",
    "security": "Security",
    ...
  },
  "hero": {
    "title": "Encrypt-D",
    "subtitle": "...",
    "cta": {
      "download": "...",
      "learnMore": "..."
    }
  },
  "features": { ... },
  "security": { ... },
  "download": { ... },
  "footer": { ... }
}
```

---

## 🏗️ Build Process

```
┌─────────────────┐
│  npm run build  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  1. TypeScript Check            │
│     astro check                 │
│     └→ Verifica tipos          │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  2. Astro Build                 │
│     Procesa archivos .astro     │
└────────┬────────────────────────┘
         │
         ├─→ src/pages/index.astro
         │   └→ dist/index.html
         │
         └─→ src/pages/es.astro
             └→ dist/es/index.html
         │
         ├─→ Optimiza CSS
         │   └→ dist/_astro/*.css
         │
         └─→ Copia public/
             └→ dist/favicon.svg
         │
         ▼
┌─────────────────────────────────┐
│  3. Output Final                │
│     dist/ (listo para deploy)   │
│     • index.html (2 KB)        │
│     • es/index.html (2 KB)     │
│     • _astro/*.css (8 KB)      │
│     • favicon.svg (1 KB)       │
│                                │
│     Total: ~70 KB (gzipped)    │
└─────────────────────────────────┘
```

---

## 🚀 Deployment Flow

```
┌────────────────────┐
│  Código Local      │
│  (web/)           │
└─────────┬──────────┘
          │
          │ git push
          ▼
┌────────────────────┐
│  GitHub Repo       │
│  (main branch)    │
└─────────┬──────────┘
          │
          │ webhook
          ▼
┌────────────────────────────────┐
│  Plataforma (Vercel/Netlify)   │
│                                │
│  1. Detecta cambios           │
│  2. npm install               │
│  3. npm run build             │
│  4. Despliega dist/           │
└─────────┬──────────────────────┘
          │
          ▼
┌────────────────────┐
│  Sitio en Vivo     │
│  https://...      │
│  • CDN global     │
│  • HTTPS auto     │
│  • Cache optimiz. │
└────────────────────┘
```

---

## 📊 Mapa de Archivos por Función

### 🎨 UI/Visual
```
src/components/Hero.astro      → Hero section
src/components/Features.astro  → Features cards
src/components/Security.astro  → Security specs
src/components/Download.astro  → Download options
src/layouts/Layout.astro       → Global styles
```

### 🌍 Internacionalización
```
src/i18n/en.json     → Traducciones inglés
src/i18n/es.json     → Traducciones español
src/i18n/utils.ts    → Utilidades i18n
```

### 📄 Páginas/Rutas
```
src/pages/index.astro  → / (inglés)
src/pages/es.astro     → /es (español)
```

### 🔧 Configuración
```
package.json       → Dependencies
astro.config.mjs   → Astro config
tsconfig.json      → TypeScript config
```

### 📚 Documentación
```
README.md          → Docs principal
QUICKSTART.md      → Inicio rápido
DEPLOYMENT.md      → Deploy guides
FEATURES.md        → Features list
PROJECT_SUMMARY.md → Resumen
STRUCTURE.md       → Este archivo
```

---

## 🔍 Dónde Encontrar Qué

| Quiero...                  | Ir a...                       |
|---------------------------|-------------------------------|
| Cambiar texto inglés      | `src/i18n/en.json`           |
| Cambiar texto español     | `src/i18n/es.json`           |
| Modificar hero section    | `src/components/Hero.astro`   |
| Cambiar colores           | `src/layouts/Layout.astro`    |
| Agregar nueva página      | `src/pages/`                  |
| Modificar navegación      | `src/components/Navigation.astro` |
| Cambiar footer            | `src/components/Footer.astro` |
| Ver cómo empezar          | `QUICKSTART.md`               |
| Guías de deployment       | `DEPLOYMENT.md`               |
| Lista de features         | `FEATURES.md`                 |
| Resumen del proyecto      | `PROJECT_SUMMARY.md`          |

---

## 🎯 Archivos Clave por Tarea

### Para Desarrollo
```
src/pages/index.astro      → Página principal
src/layouts/Layout.astro   → Estilos globales
src/i18n/utils.ts          → Sistema de traducción
```

### Para Contenido
```
src/i18n/en.json     → Editar textos inglés
src/i18n/es.json     → Editar textos español
public/              → Imágenes/assets estáticos
```

### Para Deployment
```
astro.config.mjs     → Config general
netlify.toml         → Para Netlify
vercel.json          → Para Vercel
DEPLOYMENT.md        → Guías detalladas
```

### Para Documentación
```
README.md            → Info general
QUICKSTART.md        → Empezar rápido
FEATURES.md          → Qué incluye
PROJECT_SUMMARY.md   → Resumen ejecutivo
```

---

## 📈 Flujo de Trabajo Típico

### Desarrollo
```
1. cd web
2. npm run dev
3. Editar archivos en src/
4. Ver cambios en http://localhost:4321
5. Guardar → Auto-reload
```

### Agregar Contenido
```
1. Identificar qué cambiar
2. Si es texto: editar src/i18n/*.json
3. Si es estilo: editar componente .astro
4. Si es estructura: modificar src/pages/
5. Verificar en ambos idiomas (/ y /es)
```

### Deployment
```
1. npm run build (verificar errores)
2. npm run preview (ver resultado)
3. git commit & push
4. Plataforma auto-despliega
5. Verificar sitio en vivo
```

---

## 💡 Tips de Navegación

### Encontrar Código Rápido
```bash
# Buscar texto en todos los archivos
grep -r "hero.title" src/

# Buscar en traducciones
grep "features" src/i18n/*.json
```

### Ver Estructura Completa
```bash
# Windows
tree /F web

# Ver solo src/
tree /F web\src
```

### Abrir en VSCode
```bash
# Abrir proyecto web
code web/

# Abrir archivo específico
code web/src/pages/index.astro
```

---

## 🎉 Resumen

**Archivos Totales:** ~30 archivos (sin node_modules)  
**Componentes:** 6 componentes Astro  
**Páginas:** 2 páginas (EN/ES)  
**Líneas de Código:** ~1,500 líneas  
**Documentación:** 6 archivos MD  

**Todo está organizado de forma lógica y fácil de navegar.**

---

**Última Actualización:** Octubre 9, 2025  
**Estado:** ✅ Completo y Documentado

