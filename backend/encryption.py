from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
CIPHER = Fernet(KEY)

def encrypt_message(message):
    return CIPHER.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    return CIPHER.decrypt(encrypted_message.encode()).decode()
