# Encrypt-D Landing Page

Official landing page for Encrypt-D - Secure Folder Encryption for Windows.

## 🚀 Tech Stack

- **Astro** - Modern web framework
- **TypeScript** - Type safety
- **Multi-language** - English & Spanish

## 📁 Project Structure

```
web/
├── src/
│   ├── components/       # Reusable Astro components
│   │   ├── Hero.astro
│   │   ├── Features.astro
│   │   ├── Security.astro
│   │   ├── Download.astro
│   │   ├── Navigation.astro
│   │   └── Footer.astro
│   ├── layouts/
│   │   └── Layout.astro  # Base layout
│   ├── pages/
│   │   ├── index.astro   # English homepage
│   │   └── es.astro      # Spanish homepage
│   └── i18n/
│       ├── en.json       # English translations
│       ├── es.json       # Spanish translations
│       └── utils.ts      # i18n utilities
├── public/               # Static assets
└── astro.config.mjs      # Astro configuration
```

## 🛠️ Commands

All commands are run from the web directory:

| Command           | Action                                       |
|-------------------|----------------------------------------------|
| `npm install`     | Installs dependencies                        |
| `npm run dev`     | Starts local dev server at `localhost:4321`  |
| `npm run build`   | Build your production site to `./dist/`      |
| `npm run preview` | Preview your build locally, before deploying |

## 🌍 Multi-language Support

The site supports both English and Spanish:

- **English**: `/` (default)
- **Spanish**: `/es`

Translations are managed in JSON files under `src/i18n/`.

## 🎨 Features

- **Modern Design**: Clean, professional UI with gradient accents
- **Responsive**: Mobile-first design that works on all devices
- **Fast**: Built with Astro for optimal performance
- **SEO-Ready**: Proper meta tags and semantic HTML
- **Accessible**: WCAG compliant with keyboard navigation

## 📝 Adding New Languages

1. Create a new JSON file in `src/i18n/` (e.g., `fr.json`)
2. Add the language to `src/i18n/utils.ts`
3. Create a new page in `src/pages/` (e.g., `fr.astro`)
4. Update `astro.config.mjs` to include the new locale

## 🚀 Deployment

The site can be deployed to any static hosting platform:

- **Vercel**: `vercel deploy`
- **Netlify**: Connect your Git repository
- **GitHub Pages**: Build and push `dist/` folder
- **Cloudflare Pages**: Connect your repository

## 📄 License

MIT License - Same as the main Encrypt-D project.

