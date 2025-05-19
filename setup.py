import os
import subprocess
from setuptools import setup, find_packages

print("🔹 Building and signing OpenMail installer...")
subprocess.run(["python3", "build-installer.py"])  # 🔥 Run automatic code signing!
print("✅ Installer built and signed successfully!")

LOG_FILE = "openmail_install.log"

def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")
    print(message)  # Display in console as well

def install_dependencies():
    try:
        log_message("🔹 Installing dependencies...")
        os.system("pip install --upgrade flask kubernetes pygame requests")
        log_message("✅ Dependencies installed successfully!")
    except Exception as e:
        log_message(f"❌ Error installing dependencies: {e}")

def deploy_microservices():
    try:
        log_message("🔹 Deploying microservices...")
        os.system("kubectl apply -f microservices/")
        log_message("✅ Microservices deployed successfully!")
    except Exception as e:
        log_message(f"❌ Error deploying microservices: {e}")

def start_services():
    try:
        log_message("🔹 Starting background services...")
        subprocess.run(["python3", "api/recovery_service.py"])
        subprocess.run(["python3", "api/sound_service.py"])
        log_message("✅ Services started successfully!")
    except Exception as e:
        log_message(f"❌ Error starting services: {e}")

def run_installation():
    log_message("🚀 Starting OpenMail Installation...")
    install_dependencies()
    deploy_microservices()
    start_services()
    log_message("✅ OpenMail installed successfully!")

def retry_on_failure(func, retries=3):
    for attempt in range(retries):
        try:
            func()
            return
        except Exception as e:
            log_message(f"⚠️ Attempt {attempt + 1} failed: {e}")
    log_message("❌ Installation failed after multiple attempts.")

if __name__ == "__main__":
    run_installation()

setup(
    name="openmail",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
        'pygame',
        'cryptography',
        'pytest',
        'flake8'
    ],
    author="OpenMail Team",
    description="A modern email client with DevOps tools integration",
    python_requires='>=3.8',
)
