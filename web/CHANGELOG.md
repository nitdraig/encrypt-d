# Changelog - Encrypt-D Landing Page

All notable changes to the Encrypt-D landing page will be documented in this file.

## [1.1.0] - 2025-10-10

### 🎉 Updated Content

#### Analytics Integration
- **Google Analytics 4**: Added support for GA4 tracking
  - Privacy-focused with IP anonymization
  - Tracks page views, engagement, and user behavior
  - Production-only (disabled in development)
  
- **Microsoft Clarity**: Added session recording and heatmap support
  - Session recordings to watch user interactions
  - Heatmaps showing click and scroll patterns
  - Automatic sensitive data masking
  
- **Easy Configuration**: Simple `.env` file setup
  - Copy `.env.example` to `.env`
  - Add your tracking IDs
  - Both tools are optional and work independently
  
- **Documentation**: Complete setup guide in `ANALYTICS_SETUP.md`

#### Version Bump
- Updated version display from 1.0.0 to 1.1.0 across all pages
- Added "NEW: Configurable Security" badge to hero section

#### Features Section Updates
- **Auto-Destruction Feature**: Updated from fixed "3 attempts" to "Configurable Auto-Destruction"
  - New description highlights choice between 1-10 attempts or unlimited
  - Marked as "NEW in v1.1!" to highlight recent improvement
  
- **Multi-Language Feature**: Replaced with "Responsive Interface"
  - Focus on adaptive UI that adjusts to screen size
  - Highlights strong password requirements
  - Marked as "NEW in v1.1!" for visibility

#### Security Section Updates
- **Brute Force Protection**: Changed from "Limited login attempts" to "Configurable (1-10) or unlimited"
- **Security Features List**: Updated to reflect new v1.1.0 capabilities:
  - Added: "Strong password requirements (8+ chars, A-Z, a-z, 0-9, symbols)"
  - Updated: "Configurable auto-destruction (1-10 attempts or disabled)"
  - Added: "Responsive interface adapts to any screen size"
  - Removed: "No password recovery - ultimate security" (less relevant)

#### How It Works Section
- **Step 1**: Updated from "Set Master Password" to "Configure Security"
  - Added detailed password requirements (8+ chars with complexity)
  - Mentions auto-destruction settings choice

### 🌍 Translations Updated

#### English (`en.json`)
- Updated 8 content blocks with new v1.1.0 information
- Added new badge text
- Enhanced descriptions for clarity

#### Spanish (`es.json`)
- Updated 8 content blocks with new v1.1.0 information
- Added new badge text ("NUEVO: Seguridad Configurable")
- Maintained translation quality and consistency

### 📦 Package Updates
- Updated `package.json` version from 1.0.0 to 1.1.0
- No dependency changes (remains stable)

### 📚 Documentation Updates
- Updated `PROJECT_SUMMARY.md` with v1.1.0 update date
- Updated status information

---

## [1.0.0] - 2025-10-09

### Initial Release

#### Core Features
- Professional landing page with modern design
- Full English and Spanish support
- 6 feature cards highlighting capabilities
- Security specifications section
- Download section with multiple options
- Responsive design for all devices

#### Components Created
- Hero component with CTA buttons
- Features grid component
- Security specifications component
- Download options component
- Navigation with language selector
- Footer with links and information

#### Technical Stack
- Astro 4.16+ for static site generation
- TypeScript for type safety
- Modern CSS with custom properties
- i18n system for translations
- SEO optimized
- Accessible (WCAG compliant)

#### Content
- Complete English translations (53+ strings)
- Complete Spanish translations (53+ strings)
- Detailed feature descriptions
- Security specifications
- System requirements
- Footer links and information

---

## What's Changed in v1.1.0?

### Key Updates

1. **Version Alignment**: Landing page now reflects desktop app v1.1.0
2. **Feature Accuracy**: Updated descriptions match new configurable security options
3. **User Clarity**: Better communication of flexible security settings
4. **Responsiveness Highlight**: New emphasis on adaptive interface

### Content Philosophy

The landing page now better reflects that Encrypt-D offers:
- **Flexibility**: Users choose their security level
- **Power**: Strong security requirements by default
- **Usability**: Responsive design adapts to any device

### Translation Quality

Both English and Spanish versions:
- ✅ Accurately reflect new features
- ✅ Maintain consistent tone
- ✅ Use clear, accessible language
- ✅ Highlight NEW features appropriately

---

## Upgrade Notes

### For Developers

- No breaking changes
- No new dependencies
- No structural changes
- Simply pull latest translations

### For Content Editors

- Review new descriptions in both languages
- Verify accuracy of technical specifications
- Update any custom content to match v1.1.0

### For Deployment

No changes needed to deployment pipeline:
- Same build process
- Same hosting requirements
- Same performance characteristics

---

## Future Plans

### v1.2.0 (Planned)
- [ ] Add "What's New" section for v1.1.0 features
- [ ] Include screenshot gallery
- [ ] Add user testimonials section
- [ ] Create comparison table (before/after security options)

### v2.0.0 (Future)
- [ ] Interactive demo section
- [ ] Video walkthrough
- [ ] Feature comparison table
- [ ] FAQ section
- [ ] Blog integration for security tips

---

## Links

- **Main Project**: [README.md](../README.md)
- **Desktop App**: [app/README.md](../app/README.md)
- **Desktop Changelog**: [app/CHANGELOG.md](../app/CHANGELOG.md)
- **Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**Maintained by**: Excelso Tech Group  
**License**: MIT  
**Status**: Production Ready

