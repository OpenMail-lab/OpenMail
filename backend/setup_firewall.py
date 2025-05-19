import os
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def allow_flask_firewall():
    if not is_admin():
        print("⚠️ Admin privileges required. Please run as administrator.")
        return False
        
    try:
        # Allow both inbound and outbound traffic
        os.system('netsh advfirewall firewall add rule name="Allow Flask Public 5001 IN" dir=in action=allow protocol=TCP localport=5001')
        os.system('netsh advfirewall firewall add rule name="Allow Flask Public 5001 OUT" dir=out action=allow protocol=TCP localport=5001')
        print("✅ Firewall rules added successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to configure firewall: {e}")
        return False

if __name__ == "__main__":
    os.chdir(r"c:\Users\deepa\Downloads\OpenMail")
    allow_flask_firewall()
    os.system('pip install flask requests')
