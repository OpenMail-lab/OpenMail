import os

def configure_nat():
    print("🔹 Automatically configuring NAT for Flask on port 5001...")
    os.system(f'netsh interface portproxy add v4tov4 listenport=5001 connectport=5001 connectaddress=192.168.29.71')
    print("✅ NAT mapping applied successfully!")

configure_nat()
