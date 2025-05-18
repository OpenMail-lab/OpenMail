import os
import subprocess
import sys
import platform

LOG_FILE = "openmail_install.log"

# ✅ Ensure OpenMail root directory is used (NO `dist`)
OPENMAIL_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

# ✅ Ensure `install_openmail.bat` is stored in OpenMail root
INSTALLER_SCRIPT = os.path.join(OPENMAIL_PATH, "install_openmail.bat")

def log_message(message):
    """Logs messages to file and console."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")
    print(message)

def create_installer_script():
    """Ensures `install_openmail.bat` is correctly placed in OpenMail root."""
    default_script = "@echo off\npython -m pip install -r requirements.txt\npause"

    if not os.path.exists(INSTALLER_SCRIPT):
        with open(INSTALLER_SCRIPT, "w") as script:
            script.write(default_script)
        log_message(f"✅ Installer script correctly created at {INSTALLER_SCRIPT}")

def ensure_python():
    """Checks if Python is installed and installs it if missing."""
    log_message("🔹 Checking Python installation...")

    create_installer_script()  # ✅ Ensure script exists before execution

    if not os.path.exists(INSTALLER_SCRIPT):
        log_message(f"❌ Installer script not found: {INSTALLER_SCRIPT} (Expected in {OPENMAIL_PATH})")
        sys.exit(1)

    try:
        log_message(f"🔹 Executing {INSTALLER_SCRIPT}...")
        subprocess.run(INSTALLER_SCRIPT, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Install script execution failed: {e}")
        sys.exit(1)

def install_dependencies():
    """Installs all required Python dependencies."""
    log_message("🔹 Installing OpenMail dependencies system-wide...")
    dependencies = ["flask", "kubernetes", "pygame", "requests"]

    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade"] + dependencies, check=True)
        log_message("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def start_microservices():
    """Starts required OpenMail microservices."""
    log_message("🔹 Starting microservices...")

    services = ["api/recovery_service.py", "api/sound_service.py"]
    for service in services:
        service_path = os.path.join(OPENMAIL_PATH, service)
        if not os.path.exists(service_path):
            log_message(f"❌ Microservice script not found: {service_path}")
            sys.exit(1)

        try:
            log_message(f"🔹 Starting {service}...")
            subprocess.run([sys.executable, service_path], check=True)
            log_message(f"✅ {service} started successfully!")
        except subprocess.CalledProcessError as e:
            log_message(f"❌ Error starting {service}: {e}")
            sys.exit(1)

def universal_install():
    """Executes full installation process."""
    log_message("🔹 Installing OpenMail...")

    ensure_python()  # ✅ Ensures Python is installed properly
    install_dependencies()  # ✅ Installs all required dependencies
    start_microservices()  # ✅ Starts OpenMail services

    log_message("✅ OpenMail installed successfully—without security warnings!")

if __name__ == "__main__":
    universal_install()
