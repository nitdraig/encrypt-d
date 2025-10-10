# 📊 Analytics Quick Start

Set up analytics in 3 steps!

## Step 1: Create `.env` file

```bash
cd web
cp .env.example .env
```

## Step 2: Add your IDs

Edit `.env`:

```bash
# Google Analytics (from analytics.google.com)
PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# Microsoft Clarity (from clarity.microsoft.com)
PUBLIC_CLARITY_PROJECT_ID=abc123def456
```

## Step 3: Build & Deploy

```bash
npm run build
vercel  # or your deployment method
```

Done! ✅

---

## 🔗 Get Your IDs

### Google Analytics
1. Go to [analytics.google.com](https://analytics.google.com/)
2. Create property → Web stream
3. Copy your **G-XXXXXXXXXX** ID

### Microsoft Clarity
1. Go to [clarity.microsoft.com](https://clarity.microsoft.com/)
2. Add new project
3. Copy your **Project ID**

---

## ✨ Features

- ✅ **Production only** - No tracking in development
- ✅ **Privacy-focused** - IP anonymization enabled
- ✅ **Optional** - Use one, both, or neither
- ✅ **Free** - Both platforms are 100% free

---

## 📚 Full Guide

See [ANALYTICS_SETUP.md](./ANALYTICS_SETUP.md) for detailed documentation.

---

**Quick tip**: Analytics will only work after `npm run build` and deployment. They're automatically disabled during development (`npm run dev`).

