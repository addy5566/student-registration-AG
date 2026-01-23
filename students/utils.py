# utility function for encription and decreyption

from cryptography.fernet import Fernet
from django.conf import settings

# Generate key ONCE and keep it constant
cipher = Fernet(settings.ENCRYPTION_KEY)

def encrypt_value(value: str) -> str:
    return cipher.encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str:
    return cipher.decrypt(value.encode()).decode()
