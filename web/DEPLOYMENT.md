# 🚀 Deployment Guide - Encrypt-D Landing Page

This guide covers how to deploy the Encrypt-D landing page to various hosting platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- Node.js 18+ installed
- Git repository set up
- All dependencies installed (`npm install`)
- Successful build test (`npm run build`)

## 🌐 Deployment Options

### Option 1: Vercel (Recommended)

**Why Vercel?**
- Zero configuration needed
- Automatic HTTPS
- Global CDN
- Preview deployments for PRs
- Perfect for Astro sites

**Steps:**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **For production:**
   ```bash
   vercel --prod
   ```

**Or use Vercel Dashboard:**
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Vercel auto-detects Astro
5. Click "Deploy"

---

### Option 2: Netlify

**Why Netlify?**
- Easy setup
- Form handling (if needed)
- Split testing
- Good free tier

**Steps:**

1. **Using Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   netlify deploy
   ```

2. **For production:**
   ```bash
   netlify deploy --prod
   ```

**Or use Netlify Dashboard:**
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect your Git repository
4. Build settings are auto-detected via `netlify.toml`
5. Click "Deploy site"

---

### Option 3: Cloudflare Pages

**Why Cloudflare Pages?**
- Lightning fast with Cloudflare's global network
- Generous free tier
- Built-in analytics
- DDoS protection

**Steps:**

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Navigate to "Pages"
3. Click "Create a project"
4. Connect your Git repository
5. Configure build settings:
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Node version:** 20
6. Click "Save and Deploy"

---

### Option 4: GitHub Pages

**Why GitHub Pages?**
- Free for public repos
- Direct integration with GitHub
- Simple workflow

**Steps:**

1. **Install GitHub Pages adapter:**
   ```bash
   npm install @astrojs/adapter-static
   ```

2. **Update `astro.config.mjs`:**
   ```javascript
   import { defineConfig } from 'astro/config';
   
   export default defineConfig({
     site: 'https://yourusername.github.io',
     base: '/encrypt-d',
     // ... rest of config
   });
   ```

3. **Create GitHub Action** (`.github/workflows/deploy.yml`):
   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: [ main ]
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout
           uses: actions/checkout@v4
         - name: Setup Node
           uses: actions/setup-node@v4
           with:
             node-version: 20
         - name: Install dependencies
           run: npm ci
           working-directory: ./web
         - name: Build
           run: npm run build
           working-directory: ./web
         - name: Upload artifact
           uses: actions/upload-pages-artifact@v3
           with:
             path: ./web/dist

     deploy:
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       runs-on: ubuntu-latest
       needs: build
       steps:
         - name: Deploy to GitHub Pages
           id: deployment
           uses: actions/deploy-pages@v4
   ```

4. **Enable GitHub Pages** in repository settings

---

## 🔧 Environment Variables

If you need to set environment variables:

### Vercel
```bash
vercel env add PUBLIC_GITHUB_REPO
```

### Netlify
In dashboard: Site settings → Environment variables

### Cloudflare Pages
In dashboard: Settings → Environment variables

**Example variables:**
```
PUBLIC_GITHUB_REPO=https://github.com/yourusername/encrypt-d
PUBLIC_DOWNLOAD_URL=https://github.com/yourusername/encrypt-d/releases/latest
PUBLIC_DOCS_URL=https://github.com/yourusername/encrypt-d/tree/main/app/docs
```

---

## 🎯 Custom Domain

### Vercel
1. Go to project settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

### Netlify
1. Go to "Domain settings"
2. Click "Add custom domain"
3. Configure DNS records

### Cloudflare Pages
1. Go to "Custom domains"
2. Add your domain
3. Cloudflare automatically handles DNS

---

## ✅ Pre-Deployment Checklist

Before deploying to production:

- [ ] Update GitHub repository URL in all files
- [ ] Test build locally: `npm run build`
- [ ] Test preview: `npm run preview`
- [ ] Verify all links work
- [ ] Check both language versions (EN/ES)
- [ ] Test on mobile devices
- [ ] Check SEO meta tags
- [ ] Verify favicon displays correctly
- [ ] Test download links
- [ ] Review security headers

---

## 🔄 Continuous Deployment

All platforms support automatic deployments:

1. Push to your Git repository
2. Platform automatically detects changes
3. Builds and deploys new version
4. Old version remains live until new one succeeds

**Branch Strategy:**
- `main` → Production deployment
- `develop` → Preview deployment (most platforms)
- Pull requests → Preview deployments

---

## 📊 Performance Tips

### Optimize Images
```bash
npm install sharp
```
Astro will automatically optimize images.

### Enable Compression
Already configured in build output.

### CDN Caching
All platforms provide automatic CDN caching.

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

### TypeScript Errors
```bash
# Check types
npm run astro check
```

### Missing Dependencies
```bash
# Reinstall
npm ci
```

### Port Already in Use (Development)
```bash
# Use different port
npm run dev -- --port 3000
```

---

## 📞 Support

If you encounter issues:
1. Check the [Astro documentation](https://docs.astro.build/)
2. Review platform-specific docs
3. Check GitHub issues
4. Open a new issue with build logs

---

## 🎉 Post-Deployment

After successful deployment:

1. **Test the live site:**
   - Check all pages load
   - Verify both languages
   - Test all links
   - Verify download buttons

2. **Set up analytics** (optional):
   - Google Analytics
   - Plausible
   - Cloudflare Web Analytics

3. **Monitor performance:**
   - Use Lighthouse
   - Check Core Web Vitals
   - Monitor loading times

4. **Share:**
   - Update README with live URL
   - Share on social media
   - Add to project documentation

---

**Your Encrypt-D landing page is now live! 🚀**

Live URL Examples:
- Vercel: `https://encrypt-d.vercel.app`
- Netlify: `https://encrypt-d.netlify.app`
- Cloudflare: `https://encrypt-d.pages.dev`
- Custom: `https://encrypt-d.com`

