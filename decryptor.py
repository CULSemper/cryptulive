import os
from cryptography.fernet import Fernet
import base64
import scrypt

class Decryptor:
    @staticmethod
    def decrypt(passphrase: str, input_file_path: str, output_folder_path: str) -> bool:
        try:
            with open(input_file_path, 'rb') as encrypted_file:
                salt = encrypted_file.read(16)  # Angenommene Länge des Salt
                encrypted_data = encrypted_file.read()

            key = scrypt.hash(passphrase.encode(), salt, N=16384, r=8, p=1, buflen=32)
            fernet_key = base64.urlsafe_b64encode(key)
            fernet = Fernet(fernet_key)

            decrypted_data = fernet.decrypt(encrypted_data)

            file_name, original_data = decrypted_data.split(b' ', 1)
            output_file_name = os.path.basename(file_name.decode())
            output_file_path = os.path.join(output_folder_path, output_file_name)

            # Protokolliere den Ausgabepfad
            print(f"Decrypted file will be saved to: {output_file_path}")

            # Stelle sicher, dass der Ausgabeordner existiert
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)

            with open(output_file_path, 'wb') as output_file:
                output_file.write(original_data)

            return True
        except Exception as e:
            print(f"Error decrypting the file: {e}")
            return False
