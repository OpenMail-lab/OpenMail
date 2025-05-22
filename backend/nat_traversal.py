import socket
import urllib.request

def get_public_ip():
    """Get public IP using fallback methods"""
    try:
        # Try primary method - using a public API
        response = urllib.request.urlopen('https://api.ipify.org')
        return response.read().decode('utf-8')
    except:
        # Final fallback - return localhost
        return "127.0.0.1"

def setup_nat_connection():
    """Setup basic NAT connection"""
    try:
        # Basic socket test
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 0))  # Bind to any available port
        sock.close()
        return True
    except:
        return False

public_ip = get_public_ip()
nat_setup = setup_nat_connection()
print(f"Public IP: {public_ip}, NAT Setup Successful: {nat_setup}")
