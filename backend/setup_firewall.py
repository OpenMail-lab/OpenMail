import os

def allow_flask_firewall():
    try:
        print("🔹 Configuring Windows Firewall to allow Flask on port 5001...")
        os.system('netsh advfirewall firewall add rule name="Allow Flask Public 5001" dir=in action=allow protocol=TCP localport=5001')
        print("✅ Firewall rule added successfully!")
    except Exception as e:
        print(f"❌ Failed to configure firewall: {e}")

# ✅ Run automatically when Flask starts
allow_flask_firewall()
