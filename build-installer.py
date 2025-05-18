import os
import subprocess

SIGNS_TOOL_PATH = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe"
INSTALLER_PATH = r"C:\Users\deepa\Downloads\OpenMail\dist\OpenMail-Installer.exe"

def sign_installer():
    if not os.path.exists(INSTALLER_PATH):
        print(f"❌ Error: {INSTALLER_PATH} not found. Build the installer first!")
        return

    print("🔹 Signing Windows installer...")
    subprocess.run([
        SIGNS_TOOL_PATH, "sign", "/fd", "SHA256", "/a", "/t",
        "http://timestamp.digicert.com", INSTALLER_PATH
    ], check=True)
    print("✅ Windows installer signed successfully!")

if __name__ == "__main__":
    sign_installer()
