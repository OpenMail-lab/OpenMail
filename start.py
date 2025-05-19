import subprocess
import os

def start_openmail():
    print("Starting OpenMail...")
    try:
        subprocess.run(["python", "backend/domain_service.py"])
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    start_openmail()
