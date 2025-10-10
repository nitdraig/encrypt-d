"""
Simple script to create a basic icon for Encrypt-D
Creates a PNG that you can convert to ICO
"""

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def create_basic_icon():
    """Creates a simple lock icon"""
    if not PIL_AVAILABLE:
        print("Error: Pillow is not installed")
        print("Run: pip install pillow")
        print("\nAlternatively, download an icon from:")
        print("- https://icons8.com/")
        print("- https://www.flaticon.com/")
        print("- https://www.iconfinder.com/")
        return False

    # Create image
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (26, 26, 46, 255)  # Dark blue
    lock_color = (0, 173, 181, 255)  # Cyan accent

    # Draw circle background
    margin = 20
    draw.ellipse([margin, margin, size - margin, size - margin], fill=bg_color)

    # Draw lock body (rectangle)
    lock_width = 80
    lock_height = 90
    lock_x = (size - lock_width) // 2
    lock_y = size // 2

    draw.rounded_rectangle(
        [lock_x, lock_y, lock_x + lock_width, lock_y + lock_height],
        radius=10,
        fill=lock_color,
    )

    # Draw lock shackle (arc)
    shackle_width = 50
    shackle_height = 40
    shackle_x = (size - shackle_width) // 2
    shackle_y = lock_y - shackle_height

    # Outer arc
    draw.arc(
        [
            shackle_x - 10,
            shackle_y,
            shackle_x + shackle_width + 10,
            shackle_y + shackle_height * 2,
        ],
        start=180,
        end=0,
        fill=lock_color,
        width=15,
    )

    # Draw keyhole
    keyhole_size = 15
    keyhole_x = size // 2 - keyhole_size // 2
    keyhole_y = lock_y + 30

    # Circle part of keyhole
    draw.ellipse(
        [keyhole_x, keyhole_y, keyhole_x + keyhole_size, keyhole_y + keyhole_size],
        fill=bg_color,
    )

    # Slot part of keyhole
    slot_width = 6
    slot_height = 20
    slot_x = size // 2 - slot_width // 2
    slot_y = keyhole_y + keyhole_size - 5

    draw.rectangle(
        [slot_x, slot_y, slot_x + slot_width, slot_y + slot_height], fill=bg_color
    )

    # Save in multiple sizes
    sizes = [256, 128, 64, 48, 32, 16]
    icons = []

    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        icons.append(resized)

    # Save as ICO
    icons[0].save("icon.ico", format="ICO", sizes=[(s, s) for s in sizes])

    # Also save as PNG for reference
    img.save("icon.png", "PNG")

    print("✓ Icon created successfully!")
    print("  - icon.ico (for .exe)")
    print("  - icon.png (preview)")
    print("\nYou can now run: python scripts/build.py")

    return True


if __name__ == "__main__":
    print("🎨 Encrypt-D Icon Generator\n")

    if not PIL_AVAILABLE:
        print("⚠️  Pillow not installed")
        print("\nOption 1: Install Pillow and generate icon")
        print("  pip install pillow")
        print("  python scripts/create_icon.py")
        print("\nOption 2: Download icon manually")
        print("  - Visit: https://icons8.com/icons/set/lock")
        print("  - Download as .ico")
        print("  - Save as: app/icon.ico")
        print("  - Run: python scripts/build.py")
    else:
        create_basic_icon()
