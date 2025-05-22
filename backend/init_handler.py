import subprocess
import sys
import importlib.util
import os

class InitializationHandler:
    def __init__(self):
        self.requirements_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'requirements.txt'
        )
        self.required_packages = [
            'customtkinter',
            'webview',
            'requests',
            'tkinter',
            'PIL',
            'pygame'
        ]

    def check_and_install_dependencies(self):
        try:
            import pip
        except ImportError:
            print("Installing pip...")
            self.install_pip()

        with open(self.requirements_file, 'r') as f:
            required = [line.strip() for line in f if line.strip() 
                       and not line.startswith('#')]
            
        for package in required:
            if ';' in package:  # Platform specific packages
                package_name = package.split(';')[0].strip()
                platform = package.split(';')[1].strip()
                if not self.check_platform(platform):
                    continue
            else:
                package_name = package

            if '==' in package_name:
                package_name = package_name.split('==')[0]

            if not self.is_package_installed(package_name):
                print(f"Installing {package_name}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        print("Checking dependencies...")
        for package in self.required_packages:
            if not self.is_package_installed(package):
                print(f"Installing {package}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"✓ {package} installed successfully")
                except:
                    print(f"✗ Failed to install {package}")
                    sys.exit(1)

    def is_package_installed(self, package_name):
        return importlib.util.find_spec(package_name) is not None

    def check_platform(self, platform_req):
        import platform
        return eval(platform_req)

    def install_pip(self):
        import ensurepip
        ensurepip.bootstrap()
