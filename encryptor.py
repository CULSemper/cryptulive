import os
from cryptography.fernet import Fernet
import base64
import scrypt

class Encryptor:
    @staticmethod
    def encrypt(passphrase: str, input_file_path: str, output_file_path: str) -> bool:
        salt = os.urandom(16)
        key = scrypt.hash(passphrase.encode(), salt, N=16384, r=8, p=1, buflen=32)
        fernet_key = base64.urlsafe_b64encode(key)
        fernet = Fernet(fernet_key)

        try:
            with open(input_file_path, 'rb') as input_file:
                original_data = input_file.read()
            encrypted_data = fernet.encrypt(original_data)

            with open(output_file_path, 'wb') as output_file:
                output_file.write(salt)  # Speichere das Salt am Anfang der Datei
                output_file.write(encrypted_data)
        except Exception as e:
            print(f'Error during encryption: {e}')
            return False

        return True
