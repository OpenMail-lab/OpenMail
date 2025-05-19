import os
import socket
import requests
import json

CONFIG_FILE = "setup_config.json"

def is_already_configured():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('nat_configured', False)
    except FileNotFoundError:
        return False

def get_public_ipv4():
    """Force IPv4 connection with better error handling"""
    try:
        ip_services = [
            "https://api4.ipify.org",
            "https://ipv4.icanhazip.com",
            "https://v4.ident.me"
        ]
        
        for service in ip_services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    ip = response.text.strip()
                    print(f"✅ Got public IP: {ip}")
                    return ip
            except:
                continue
                
        # Fallback: Get local IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        print(f"⚠️ Using local IP: {local_ip}")
        return local_ip
        
    except Exception as e:
        print(f"❌ IP detection failed: {e}")
        return "127.0.0.1"

def configure_nat():
    """Configure NAT only if not already configured"""
    if is_already_configured():
        print("✅ NAT already configured!")
        return True
        
    try:
        public_ip = get_public_ipv4()
        print(f"🔹 Setting up NAT with public IP: {public_ip}")
        
        if os.name == 'nt':  # Windows
            os.system(f'netsh interface portproxy delete all')
            os.system(f'netsh interface portproxy add v4tov4 listenport=5001 connectport=5001 connectaddress={public_ip}')
        else:  # Linux/MacOS
            os.system('sudo iptables -t nat -F')  # Clear existing rules
            os.system(f'sudo iptables -t nat -A PREROUTING -p tcp --dport 5001 -j DNAT --to-destination {public_ip}:5001')
        
        # Save configuration state
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'nat_configured': True, 'public_ip': public_ip}, f)
            
        print("✅ NAT configured successfully!")
        return True
    except Exception as e:
        print(f"❌ NAT configuration failed: {e}")
        return False

if __name__ == "__main__":
    configure_nat()
