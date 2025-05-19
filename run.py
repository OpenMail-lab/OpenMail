import subprocess
import os
import sys

def start_openmail():
    print("🔹 Starting OpenMail services...")
    
    # Configure NAT and Firewall
    subprocess.run([sys.executable, "backend/setup_nat.py"])
    subprocess.run([sys.executable, "backend/setup_firewall.py"])
    
    # Start main service
    subprocess.Popen([sys.executable, "backend/home_service.py"])
    
    print("✅ OpenMail is running!")
    print("🌐 Access the application at: http://localhost:5001")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    start_openmail()
