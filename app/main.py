"""
Encrypt-D - Secure Folder Encryption Application
Entry point for the application

Author: Encrypt-D Team
Version: 1.0.0
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui import EncryptDGUI


def main():
    """Main function to start the application"""
    try:
        app = EncryptDGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
