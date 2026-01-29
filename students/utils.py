from cryptography.fernet import Fernet
from django.conf import settings
import hashlib


if not settings.ENCRYPTION_KEY:
    raise RuntimeError("ENCRYPTION_KEY is not set")

cipher = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_value(value: str) -> str:
    return cipher.encrypt(value.encode()).decode()


def decrypt_value(value: str) -> str:
    return cipher.decrypt(value.encode()).decode()

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
