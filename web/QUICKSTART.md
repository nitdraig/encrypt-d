# 🚀 Quickstart Guide - Encrypt-D Landing Page

Get the landing page running in 3 minutes!

## ⚡ Super Quick Start

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit: **http://localhost:4321**

That's it! 🎉

---

## 📋 Available Commands

| Command | Description | When to use |
|---------|-------------|-------------|
| `npm run dev` | Start dev server | Development |
| `npm run build` | Build for production | Before deployment |
| `npm run preview` | Preview production build | Test before deploy |
| `npm run astro check` | Check for errors | Before committing |

---

## 🌍 View Different Languages

### English (Default)
```
http://localhost:4321/
```

### Spanish
```
http://localhost:4321/es
```

---

## 🎨 Project Structure

```
web/
├── src/
│   ├── components/       # UI components
│   ├── layouts/          # Page layouts
│   ├── pages/            # Routes (index.astro, es.astro)
│   └── i18n/            # Translations (en.json, es.json)
├── public/              # Static files (favicon, etc.)
└── dist/                # Build output (after npm run build)
```

---

## ✏️ Making Changes

### Change Text Content

1. **Edit translations:**
   - English: `src/i18n/en.json`
   - Spanish: `src/i18n/es.json`

2. **Save file** → Changes auto-reload in browser

### Change Styles

1. **Edit component** (e.g., `src/components/Hero.astro`)
2. **Modify `<style>` section**
3. **Save** → See changes instantly

### Add New Section

1. **Create component** in `src/components/`
2. **Import in page** (`src/pages/index.astro`)
3. **Add to both** English and Spanish pages

---

## 🔧 Customization Guide

### Update GitHub Links

Search and replace in all files:
```
yourusername/encrypt-d → YOUR_USERNAME/YOUR_REPO
```

### Update Colors

Edit `src/layouts/Layout.astro` CSS variables:
```css
:root {
  --color-primary: #3b82f6;  /* Change this */
  --color-secondary: #8b5cf6; /* And this */
}
```

### Add New Language

1. **Create** `src/i18n/fr.json` (example: French)
2. **Copy structure** from `en.json`
3. **Translate all values**
4. **Create** `src/pages/fr.astro`
5. **Copy from** `es.astro` and change lang to 'fr'

---

## 🐛 Common Issues

### Port Already in Use
```bash
# Use different port
npm run dev -- --port 3000
```

### Dependencies Error
```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
# Check what's wrong
npm run astro check
```

### Build Fails
```bash
# Clear cache
rm -rf dist .astro
npm run build
```

---

## 📦 Building for Production

```bash
# Build the site
npm run build

# Preview production build locally
npm run preview
```

The built files are in `dist/` folder.

---

## 🚀 Deployment

### Quick Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Quick Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed guides.

---

## 📝 Next Steps

1. ✅ **Customize content** - Update translations with your info
2. ✅ **Update links** - Replace placeholder GitHub URLs
3. ✅ **Add download link** - Update when you have releases
4. ✅ **Set up analytics** - Configure Google Analytics & Clarity (optional)
5. ✅ **Test both languages** - Make sure everything works
6. ✅ **Build and deploy** - Get it online!

---

## 📚 Learn More

- [ANALYTICS_SETUP.md](./ANALYTICS_SETUP.md) - Set up Google Analytics & Clarity
- [FEATURES.md](./FEATURES.md) - Complete features list
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guides
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - Project overview
- [Astro Docs](https://docs.astro.build/) - Learn Astro

---

## 💡 Pro Tips

### Hot Reload Not Working?
- Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)

### Want to See Build Size?
```bash
npm run build -- --verbose
```

### Test on Mobile?
```bash
# Start dev server
npm run dev

# Access from phone using your computer's IP
http://YOUR_IP:4321
```

### Optimize Images?
Place images in `src/assets/` instead of `public/` for automatic optimization.

---

## 🎉 You're Ready!

The landing page is:
- ✅ Modern and professional
- ✅ Fully responsive
- ✅ Multi-language ready
- ✅ Fast and optimized
- ✅ Easy to customize
- ✅ Ready to deploy

**Start the dev server and see your beautiful landing page!**

```bash
npm run dev
```

Happy coding! 🚀

