#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil


def create_executable():
    """Create executable using PyInstaller"""
    try:
        # PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "StudentManagement",
            "--icon", "icon.ico",  # Optional: add an icon file
            "main.py"
        ]

        # Remove icon option if no icon file exists
        if not os.path.exists("icon.ico"):
            cmd.remove("--icon")
            cmd.remove("icon.ico")

        print("Creating executable...")
        subprocess.check_call(cmd)

        # Move executable to root directory
        if os.name == 'nt':  # Windows
            exe_name = "StudentManagement.exe"
        else:  # Linux/macOS
            exe_name = "StudentManagement"

        source_path = os.path.join("dist", exe_name)
        target_path = exe_name

        if os.path.exists(source_path):
            shutil.move(source_path, target_path)
            print(f"✓ Executable created: {target_path}")

            # Clean up build directories
            if os.path.exists("build"):
                shutil.rmtree("build")
            if os.path.exists("dist"):
                shutil.rmtree("dist")
            if os.path.exists("StudentManagement.spec"):
                os.remove("StudentManagement.spec")

            print("✓ Cleaned up temporary files")
            return True
        else:
            print("✗ Executable not found")
            return False

    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install PyInstaller")
        return False


def main():
    print("Student Management System Build Script")
    print("=" * 50)

    # Check if PyInstaller is available
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "--version"])
    except subprocess.CalledProcessError:
        print("PyInstaller not found. Installing...")
        if not install_pyinstaller():
            return

    if create_executable():
        print("\n✓ Build completed successfully!")
        print("\nYou can now run the program using:")
        if os.name == 'nt':
            print("  StudentManagement.exe")
        else:
            print("  ./StudentManagement")
    else:
        print("\n✗ Build failed. Please check the error messages above.")


if __name__ == "__main__":
    main()