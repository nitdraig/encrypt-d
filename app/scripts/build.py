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
    # Use 'python -m PyInstaller' instead of 'pyinstaller' for better compatibility
    params = [
        sys.executable,  # Current Python interpreter
        "-m",
        "PyInstaller",
        "--name=Encrypt-D",
        "--onefile",  # Single executable file
        "--windowed",  # No console (GUI mode)
        "--icon=icon.ico",  # Custom icon file
        "--clean",
        "--noconfirm",
        # Add necessary paths
        f"--add-data=src{os.pathsep}src",
        f"--add-data=icon.ico{os.pathsep}.",  # Include icon in root of bundle
        # Hidden imports - Standard library
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=_tkinter",
        "--hidden-import=json",
        "--hidden-import=secrets",
        "--hidden-import=webbrowser",
        "--hidden-import=pathlib",
        "--hidden-import=shutil",
        "--hidden-import=os",
        "--hidden-import=sys",
        "--hidden-import=datetime",
        # Hidden imports - Cryptography
        "--hidden-import=cryptography",
        "--hidden-import=cryptography.hazmat.primitives",
        "--hidden-import=cryptography.hazmat.primitives.ciphers",
        "--hidden-import=cryptography.hazmat.primitives.ciphers.aead",
        "--hidden-import=cryptography.hazmat.primitives.kdf",
        "--hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2",
        "--hidden-import=cryptography.hazmat.primitives.hashes",
        "--hidden-import=cryptography.hazmat.backends",
        "--hidden-import=cryptography.hazmat.backends.openssl",
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
    except ImportError:
        print("Error: cryptography not installed")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    try:
        import PyInstaller
    except ImportError:
        print("Error: PyInstaller not installed")
        print("Run: pip install pyinstaller")
        print("\nAlternatively, if using Python from Microsoft Store,")
        print("consider installing Python from python.org for better compatibility.")
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
