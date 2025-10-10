# 📊 Analytics Setup Guide - Encrypt-D Landing Page

This guide will help you set up **Google Analytics** and **Microsoft Clarity** for your Encrypt-D landing page.

## 🎯 Overview

The landing page comes with built-in support for:
- **Google Analytics 4 (GA4)** - Track page views, user behavior, and conversions
- **Microsoft Clarity** - Session recordings and heatmaps

Both analytics platforms are:
- ✅ **Privacy-focused** (anonymized IP for GA4)
- ✅ **Production-only** (disabled in development)
- ✅ **Optional** (work independently)
- ✅ **Free** to use

---

## 🚀 Quick Setup

### Step 1: Create Environment File

```bash
# Navigate to web directory
cd web

# Copy the example file
cp .env.example .env
```

### Step 2: Add Your IDs

Edit `.env` and add your tracking IDs:

```bash
# Google Analytics
PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# Microsoft Clarity
PUBLIC_CLARITY_PROJECT_ID=abc123def456
```

### Step 3: Build and Deploy

```bash
npm run build
```

That's it! Analytics will be active in production.

---

## 📈 Google Analytics Setup

### 1. Create Google Analytics Account

1. Go to [Google Analytics](https://analytics.google.com/)
2. Click **"Start measuring"**
3. Create an account (or use existing)
4. Set up a property for your website

### 2. Get Your Measurement ID

1. In GA4, go to **Admin** (bottom left)
2. Under **Property**, click **Data Streams**
3. Select your web stream (or create one)
4. Copy your **Measurement ID** (format: `G-XXXXXXXXXX`)

### 3. Add to Environment File

```bash
PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

### 4. What Gets Tracked?

Automatically tracked:
- ✅ Page views
- ✅ Scroll depth
- ✅ Outbound link clicks
- ✅ File downloads
- ✅ Site search (if applicable)
- ✅ User engagement time

Privacy features:
- ✅ **IP anonymization** enabled
- ✅ **SameSite cookies** for security
- ✅ GDPR compliant

---

## 🔍 Microsoft Clarity Setup

### 1. Create Clarity Account

1. Go to [Microsoft Clarity](https://clarity.microsoft.com/)
2. Sign in with Microsoft account (free)
3. Click **"Add new project"**

### 2. Set Up Project

1. Enter your website details:
   - **Name**: Encrypt-D Landing Page
   - **Website URL**: https://yourdomain.com
2. Click **"Add new project"**

### 3. Get Your Project ID

1. After creation, you'll see your **Project ID**
2. It's an alphanumeric string (e.g., `abc123def456`)
3. Copy this ID

### 4. Add to Environment File

```bash
PUBLIC_CLARITY_PROJECT_ID=abc123def456
```

### 5. What Gets Tracked?

Clarity provides:
- ✅ **Session recordings** - Watch how users interact
- ✅ **Heatmaps** - See where users click and scroll
- ✅ **Rage clicks** - Identify frustrated users
- ✅ **Dead clicks** - Find broken interactions
- ✅ **Excessive scrolling** - Detect usability issues

Privacy features:
- ✅ **Masks sensitive data** automatically
- ✅ No personal information collected
- ✅ GDPR compliant

---

## 🛠️ Configuration Details

### Environment Variables

| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `PUBLIC_GA_MEASUREMENT_ID` | No | G-XXXXXXXXXX | G-ABC123DEF4 |
| `PUBLIC_CLARITY_PROJECT_ID` | No | Alphanumeric | abc123def456 |

### Important Notes

1. **Prefix is Important**: All variables MUST start with `PUBLIC_` to be accessible in Astro components
2. **Production Only**: Analytics run only in production builds (`npm run build`)
3. **Independent**: You can use one, both, or none - they work independently
4. **No Rebuild Needed**: After deployment, you can change IDs without rebuilding

### Development vs Production

```bash
# Development - Analytics DISABLED
npm run dev
# ❌ No tracking
# ✓ Fast reload
# ✓ No analytics overhead

# Production - Analytics ENABLED
npm run build
# ✓ GA4 tracking active
# ✓ Clarity recording active
# ✓ Real user data
```

---

## 📊 Verifying Setup

### Check Google Analytics

1. Deploy your site
2. Visit your live URL
3. Go to GA4 → **Reports** → **Realtime**
4. You should see your visit in real-time

### Check Microsoft Clarity

1. Deploy your site
2. Visit your live URL
3. Go to Clarity → **Dashboard**
4. Recordings appear within a few minutes

### Debug Issues

If analytics aren't working:

1. **Check .env file exists** in `web/` directory
2. **Verify IDs are correct** (no typos)
3. **Confirm production build**: `npm run build`
4. **Wait a few minutes** for data to appear
5. **Check browser console** for errors
6. **Disable ad blockers** for testing

---

## 🔐 Privacy & Compliance

### GDPR Compliance

Both analytics platforms are configured for privacy:

**Google Analytics:**
- IP anonymization enabled
- No PII (Personally Identifiable Information) collected
- Cookie consent recommended (add your own banner)

**Microsoft Clarity:**
- Automatic masking of sensitive data
- No personal information stored
- Sessions are anonymized

### Cookie Banner (Optional)

If you want a cookie consent banner, consider:
- [Cookie Consent](https://www.osano.com/cookieconsent)
- [CookieYes](https://www.cookieyes.com/)
- [OneTrust](https://www.onetrust.com/)

Example implementation:
```html
<!-- Add before </body> in Layout.astro -->
<script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js"></script>
```

---

## 🎯 Best Practices

### 1. Monitor Key Metrics

**Google Analytics - Track:**
- Page views per language (/ vs /es)
- Download button clicks
- GitHub link clicks
- Average session duration
- Bounce rate

**Microsoft Clarity - Watch for:**
- Rage clicks on download button
- Scroll depth on features section
- Mobile vs desktop behavior
- Navigation patterns

### 2. Set Up Goals (GA4)

Create custom events for:
```javascript
// Download button click
gtag('event', 'download_click', {
  'event_category': 'engagement',
  'event_label': 'exe_download'
});

// GitHub link click
gtag('event', 'github_click', {
  'event_category': 'engagement',
  'event_label': 'repository_visit'
});
```

### 3. Regular Reviews

- **Weekly**: Check Clarity for usability issues
- **Monthly**: Review GA4 for traffic trends
- **Quarterly**: Optimize based on insights

---

## 🚫 Disabling Analytics

### Temporarily Disable

Comment out in `.env`:
```bash
# PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
# PUBLIC_CLARITY_PROJECT_ID=abc123def456
```

### Permanently Remove

1. Delete `.env` file
2. Remove `<Analytics />` from `Layout.astro`
3. Delete `src/components/Analytics.astro`

---

## 📚 Resources

### Google Analytics
- [GA4 Documentation](https://support.google.com/analytics/answer/9304153)
- [GA4 Setup Guide](https://support.google.com/analytics/answer/9304153)
- [Privacy & Terms](https://policies.google.com/privacy)

### Microsoft Clarity
- [Clarity Documentation](https://docs.microsoft.com/en-us/clarity/)
- [Getting Started](https://clarity.microsoft.com/getting-started)
- [Privacy Policy](https://privacy.microsoft.com/en-us/privacystatement)

### Astro
- [Environment Variables](https://docs.astro.build/en/guides/environment-variables/)
- [Client-side Scripts](https://docs.astro.build/en/guides/client-side-scripts/)

---

## 🐛 Troubleshooting

### Analytics not showing in GA4

**Problem**: No data appearing in Google Analytics

**Solutions:**
1. ✅ Wait 24-48 hours (GA4 can be slow initially)
2. ✅ Check Measurement ID format: `G-XXXXXXXXXX`
3. ✅ Verify it's a production build
4. ✅ Disable browser extensions (ad blockers)
5. ✅ Check browser console for errors

### Clarity not recording

**Problem**: No sessions in Microsoft Clarity

**Solutions:**
1. ✅ Wait 5-10 minutes (processing delay)
2. ✅ Check Project ID is correct
3. ✅ Verify domain matches in Clarity settings
4. ✅ Clear browser cache
5. ✅ Try incognito mode

### Environment variables not working

**Problem**: IDs not being read from .env

**Solutions:**
1. ✅ Ensure file is named exactly `.env` (not `.env.txt`)
2. ✅ Check it's in `web/` directory (not root)
3. ✅ Verify `PUBLIC_` prefix on variable names
4. ✅ Restart dev server after creating `.env`
5. ✅ Rebuild for production: `npm run build`

---

## 🎉 Success Checklist

- [ ] Created `.env` file in `web/` directory
- [ ] Added Google Analytics Measurement ID
- [ ] Added Microsoft Clarity Project ID
- [ ] Built production version (`npm run build`)
- [ ] Deployed to hosting platform
- [ ] Verified GA4 shows real-time data
- [ ] Verified Clarity shows recordings
- [ ] Tested on both English and Spanish pages
- [ ] Documented setup for team

---

## 📞 Support

If you need help:

1. **Check this guide first** - Most issues are covered
2. **GA4 Support**: [Google Analytics Help](https://support.google.com/analytics/)
3. **Clarity Support**: [Microsoft Clarity Help](https://docs.microsoft.com/en-us/clarity/)
4. **Astro Support**: [Astro Discord](https://astro.build/chat)

---

**Happy Analyzing! 📊**

Track with confidence, improve with data.

