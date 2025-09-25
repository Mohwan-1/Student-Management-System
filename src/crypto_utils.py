import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from typing import Any, Dict


class CryptoManager:
    def __init__(self):
        self.backend = default_backend()

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password.encode())

    def encrypt_data(self, data: Dict[str, Any], password: str) -> bytes:
        json_data = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')

        salt = os.urandom(32)
        key = self._derive_key(password, salt)

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padding_length = 16 - (len(json_data) % 16)
        padded_data = json_data + bytes([padding_length] * padding_length)

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        result = salt + iv + encrypted_data
        return result

    def decrypt_data(self, encrypted_data: bytes, password: str) -> Dict[str, Any]:
        salt = encrypted_data[:32]
        iv = encrypted_data[32:48]
        ciphertext = encrypted_data[48:]

        key = self._derive_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        padding_length = padded_data[-1]
        json_data = padded_data[:-padding_length]

        return json.loads(json_data.decode('utf-8'))

    def verify_password(self, encrypted_data: bytes, password: str) -> bool:
        try:
            self.decrypt_data(encrypted_data, password)
            return True
        except Exception:
            return False