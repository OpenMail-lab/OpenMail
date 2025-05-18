import stun

nat_type, external_ip, external_port = stun.get_ip_info()
print(f"NAT Type: {nat_type}, Public IP: {external_ip}, Port: {external_port}")
