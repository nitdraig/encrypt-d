# 🎨 Icon Setup Guide - Encrypt-D

Complete guide to add a custom icon to your Encrypt-D executable.

---

## 🚀 Quick Setup

### Option 1: Generate Basic Icon (Automatic)

```bash
# 1. Install Pillow (if not installed)
pip install pillow

# 2. Generate icon
cd app
python scripts/create_icon.py

# 3. Rebuild with icon
python scripts/build.py
```

### Option 2: Use Custom Icon (Manual)

```bash
# 1. Get your .ico file (see sources below)

# 2. Save as app/icon.ico

# 3. Build
cd app
python scripts/build.py
```

---

## 📥 Where to Get Icons

### Free Icon Sources

1. **Icons8** - https://icons8.com/

   - Search: "lock", "security", "encryption"
   - Download as ICO (256x256 recommended)
   - ✅ Free with attribution

2. **Flaticon** - https://www.flaticon.com/

   - Large selection of security icons
   - Download as PNG, convert to ICO
   - ✅ Free with attribution

3. **IconFinder** - https://www.iconfinder.com/

   - Search: "lock icon"
   - Filter by "Free" and "ICO format"
   - ✅ Many free options

4. **Icon Archive** - https://iconarchive.com/
   - Security & privacy category
   - Download as ICO directly
   - ✅ Various licenses (check each)

---

## 🔄 Converting Images to ICO

### Online Converters

1. **ConvertICO** - https://convertico.com/

   - Upload PNG/JPG
   - Select all sizes (16x16 to 256x256)
   - Download ICO

2. **ICO Convert** - https://icoconvert.com/

   - Drag & drop image
   - Multiple size support
   - Free download

3. **Favicon.io** - https://favicon.io/
   - Text to icon
   - PNG to ICO
   - Simple and fast

### Desktop Tools

**Windows:**

- **IcoFX** - Professional icon editor
- **Greenfish Icon Editor** - Free and open source
- **Paint.NET** with ICO plugin

**Cross-platform:**

- **GIMP** - Free, supports ICO format
- **Inkscape** - Vector graphics, export to ICO

---

## 🎨 Icon Requirements

### Technical Specifications

| Aspect          | Requirement                  |
| --------------- | ---------------------------- |
| **Format**      | `.ico`                       |
| **Sizes**       | 16x16, 32x32, 48x48, 256x256 |
| **Recommended** | All sizes in one file        |
| **Minimum**     | 256x256                      |
| **Color Depth** | 32-bit (with transparency)   |

### Design Recommendations

**Do:**

- ✅ Use simple, recognizable shapes (lock, shield, key)
- ✅ Use brand colors (#00adb5, #3b82f6, #8b5cf6)
- ✅ Keep it clear at small sizes
- ✅ Use transparency for modern look
- ✅ Test at 16x16 size

**Don't:**

- ❌ Too much detail (won't show at small sizes)
- ❌ Text (unreadable at small sizes)
- ❌ Light colors on light background
- ❌ Too many colors (keep it simple)

---

## 🖼️ Design Ideas

### Concept 1: Lock Icon

```
🔒 Simple padlock
- Classic security symbol
- Recognizable at any size
- Professional look
```

### Concept 2: Shield Icon

```
🛡️ Shield with lock
- Protection + security
- Modern and professional
- Clear symbolism
```

### Concept 3: Key Icon

```
🔑 Key or keyhole
- Encryption metaphor
- Clean design
- Distinctive
```

### Concept 4: Folder with Lock

```
📁🔒 Folder + lock overlay
- Shows app purpose clearly
- Intuitive for users
- Unique identifier
```

---

## 🔧 Implementation Steps

### Step 1: Prepare Your Icon

```bash
# Ensure icon is in app directory
app/
  ├── icon.ico        # Your icon file
  ├── main.py
  └── scripts/
      └── build.py
```

### Step 2: Verify Icon

```bash
# Check icon exists
dir icon.ico

# Check icon properties (right-click → Properties)
# Should show multiple sizes available
```

### Step 3: Update Build Script

The script is already configured! It will automatically use `icon.ico` if present.

```python
# In scripts/build.py (already updated)
"--icon=icon.ico",  # ✅ Uses your icon
```

### Step 4: Build with Icon

```bash
cd app
python scripts/build.py
```

### Step 5: Verify

```bash
# Check the .exe file
dir dist\Encrypt-D.exe

# Right-click → Properties → Should show your icon
```

---

## 🎨 Creating Icon with Pillow

If you want to create a simple icon programmatically:

```python
# Already provided in scripts/create_icon.py
python scripts/create_icon.py
```

This creates:

- `icon.ico` - Multi-size icon for .exe
- `icon.png` - Preview of the icon

Colors match Encrypt-D brand:

- Background: `#1a1a2e` (dark blue)
- Lock: `#00adb5` (cyan accent)

---

## 🐛 Troubleshooting

### Icon Not Showing in .exe

**Problem**: Built .exe still has default Python icon

**Solutions:**

1. **Verify icon exists**

   ```bash
   cd app
   dir icon.ico
   ```

2. **Check icon format**

   - Must be `.ico` format (not `.png` renamed)
   - Use online converter if needed

3. **Rebuild completely**

   ```bash
   python scripts/build.py
   ```

4. **Clear Windows icon cache**
   ```bash
   # In cmd as Administrator
   ie4uinit.exe -show
   ie4uinit.exe -ClearIconCache
   ```

### Icon Looks Blurry

**Problem**: Icon pixelated or low quality

**Solutions:**

1. **Use high-resolution source**

   - Start with at least 512x512 PNG
   - Ensure sharp, vector-based design

2. **Include all sizes**

   - 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
   - Each size optimized separately

3. **Use professional tool**
   - GIMP or IcoFX for better quality
   - Manual size optimization

### PyInstaller Icon Error

**Problem**: Build fails with icon-related error

**Solutions:**

1. **Check path**

   ```python
   # Use absolute path if needed
   "--icon=E:\\path\\to\\icon.ico"
   ```

2. **Test icon validity**

   - Open in icon editor
   - Verify format and sizes

3. **Use NONE temporarily**
   ```python
   "--icon=NONE"  # Build without icon first
   ```

---

## 📊 Icon Size Reference

| Size        | Usage                        |
| ----------- | ---------------------------- |
| **16x16**   | Task Manager, small toolbars |
| **32x32**   | Desktop shortcuts, explorer  |
| **48x48**   | Large icon view              |
| **64x64**   | Extra large icons            |
| **128x128** | Jumbo icons                  |
| **256x256** | High DPI displays            |

**Recommendation**: Include all sizes for best appearance.

---

## 🎯 Best Practices

1. **Test Your Icon**

   - View at all sizes
   - Check on different backgrounds
   - Verify clarity at 16x16

2. **Brand Consistency**

   - Use Encrypt-D colors
   - Match landing page style
   - Professional appearance

3. **File Management**

   - Keep source files (PNG/SVG)
   - Version control icons
   - Document design choices

4. **Legal Compliance**
   - Check icon license
   - Attribute if required
   - Respect copyright

---

## 📚 Resources

### Icon Design

- [Icon Design Guidelines](https://developer.microsoft.com/en-us/windows/apps/design/style/iconography/)
- [Material Design Icons](https://material.io/design/iconography/)
- [Windows Icon Guidelines](https://docs.microsoft.com/en-us/windows/apps/design/style/icons)

### Tools

- [GIMP](https://www.gimp.org/) - Free image editor
- [Inkscape](https://inkscape.org/) - Vector graphics
- [IcoFX](https://icofx.ro/) - Icon editor

### Inspiration

- [Dribbble - Security Icons](https://dribbble.com/search/security-icon)
- [Behance - Lock Icons](https://www.behance.net/search/projects?search=lock%20icon)

---

## ✅ Quick Checklist

- [ ] Icon file created/downloaded
- [ ] Saved as `app/icon.ico`
- [ ] Format verified (.ico with multiple sizes)
- [ ] Build script updated (already done!)
- [ ] Rebuilt executable
- [ ] Icon appears correctly in .exe
- [ ] Tested on desktop shortcut
- [ ] Looks good at small sizes

---

## 🎉 Success!

Your `.exe` now has a professional icon!

**Next steps:**

1. Create desktop shortcut
2. Test the icon appearance
3. Distribute your application

**Tip**: The icon file should be ~50-150KB. If larger, optimize or reduce sizes.

---

**Need help?** Check the troubleshooting section or refer to PyInstaller documentation.
