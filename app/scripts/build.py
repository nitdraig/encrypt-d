"""
Build Script for Encrypt-D
Creates a standalone .exe file using PyInstaller
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess


def clean_build_dirs():
    """Cleans previous build directories"""
    dirs_to_clean = ["build", "dist", "__pycache__"]

    project_root = Path(__file__).parent.parent

    for dir_name in dirs_to_clean:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_path)

    # Clean .spec files
    for spec_file in project_root.glob("*.spec"):
        print(f"Removing {spec_file}...")
        spec_file.unlink()


def build_exe():
    """Builds the executable with PyInstaller"""
    print("=" * 60)
    print("Building Encrypt-D...")
    print("=" * 60)

    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # PyInstaller parameters
    params = [
        "pyinstaller",
        "--name=Encrypt-D",
        "--onefile",  # Single executable file
        "--windowed",  # No console (GUI mode)
        "--icon=NONE",  # You can add an .ico file here
        "--clean",
        "--noconfirm",
        # Add necessary paths
        f"--add-data=src{os.pathsep}src",
        # Hidden imports
        "--hidden-import=tkinter",
        "--hidden-import=cryptography",
        "--hidden-import=cryptography.hazmat.primitives",
        "--hidden-import=cryptography.hazmat.primitives.ciphers",
        "--hidden-import=cryptography.hazmat.primitives.ciphers.aead",
        "--hidden-import=cryptography.hazmat.primitives.kdf",
        "--hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2",
        # Main file
        "main.py",
    ]

    # Run PyInstaller
    try:
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        print(result.stdout)

        print("\n" + "=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        print(
            f"\nExecutable located at: {(project_root / 'dist' / 'Encrypt-D.exe').absolute()}"
        )
        print("\nYou can distribute this .exe file independently.")

        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("✗ Build failed")
        print("=" * 60)
        print(e.stderr)
        return False


def main():
    """Main function for build script"""
    print("\n🔒 Encrypt-D - Build Script\n")

    # Check we're in the correct directory
    if not Path("main.py").exists():
        print("Error: This script must be run from the project root")
        print("Current directory:", Path.cwd())
        sys.exit(1)

    # Check dependencies are installed
    try:
        import cryptography
        import PyInstaller
    except ImportError as e:
        print(f"Error: Missing dependencies")
        print(f"Run: pip install -r requirements.txt")
        sys.exit(1)

    # Clean previous builds
    clean_build_dirs()

    # Build executable
    success = build_exe()

    if success:
        # Clean temporary files
        print("\nCleaning temporary files...")
        if Path("build").exists():
            shutil.rmtree("build")
        for spec_file in Path(".").glob("*.spec"):
            spec_file.unlink()

        print("\n✓ Process completed!")
    else:
        print("\n✗ Build failed. Check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
