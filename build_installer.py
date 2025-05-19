import os
import subprocess
import shutil
import sys

def ensure_directories():
    """Create required directories if they don't exist"""
    directories = ['backend', 'sounds', 'ui']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create placeholder files to ensure directories are included
        with open(os.path.join(directory, '.placeholder'), 'w') as f:
            f.write('# Placeholder file for PyInstaller\n')

def cleanup_temp():
    """Clean up temporary PyInstaller files"""
    try:
        # Clean up temp directories
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('__pycache__', ignore_errors=True)
        if os.path.exists('OpenMail-Installer.spec'):
            os.remove('OpenMail-Installer.spec')
    except Exception as e:
        print(f"Warning: Cleanup failed - {e}")

def build_installer():
    print("🔹 Building OpenMail installer...")
    try:
        # Clean previous build
        cleanup_temp()
        
        # Build with console window enabled
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",  # Changed from --windowed to show console
            "--name", "OpenMail-Installer",
            "--add-data", "backend;backend",
            "--add-data", "ui;ui",
            "--add-data", "sounds;sounds",
            # Add icon if available
            # "--icon=resources/openmail.ico",
            "universal-installer.py"
        ], check=True)
        
        print("✅ Installer built successfully!")
        return True
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False

def sign_installer():
    print("🔹 Signing the installer...")
    try:
        subprocess.run([
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe",
            "sign",
            "/fd", "SHA256",
            "/a",
            "/t", "http://timestamp.digicert.com",
            r"dist\OpenMail-Installer.exe"
        ], check=True)
        print("✅ Installer signed successfully!")
        return True
    except Exception as e:
        print(f"❌ Signing failed: {e}")
        return False

if __name__ == "__main__":
    if build_installer():
        sign_installer()
    print("🚀 OpenMail installer is ready in the dist folder!")
