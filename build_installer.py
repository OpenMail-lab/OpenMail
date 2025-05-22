import os
import sys
import subprocess
import PyInstaller.__main__

SIGNS_TOOL_PATH = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe"

def sign_installer():
    installer_path = os.path.join('dist', 'OpenMail-Installer.exe')
    if not os.path.exists(installer_path):
        print("❌ Installer not found!")
        return False

    print("🔹 Signing the installer...")
    try:
        subprocess.run([
            SIGNS_TOOL_PATH, "sign",
            "/fd", "SHA256",
            "/a",
            "/t", "http://timestamp.digicert.com",
            installer_path
        ], check=True)
        print("✅ Installer signed successfully!")
        return True
    except Exception as e:
        print(f"❌ Signing failed: {e}")
        return False

def build_installer():
    print("🔹 Building OpenMail installer...")
    
    build_args = [
        'universal-installer.py',  # Changed from home_service.py to universal-installer.py
        '--name=OpenMail-Installer',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--add-data=frontend;frontend',
        '--add-data=backend;backend',
        '--add-data=install_openmail.bat;.',
        '--hidden-import=PIL',
        '--hidden-import=tkinter',
        '--collect-submodules=customtkinter',
        '--exclude-module=webview'
    ]

    PyInstaller.__main__.run(build_args)
    sign_installer()  # Add signing step back

if __name__ == "__main__":
    build_installer()
