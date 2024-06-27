import os
from decryptor import Decryptor

def decrypt_folder(passphrase: str, input_folder_path: str, output_folder_path: str):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            input_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(input_file_path, input_folder_path)
            output_file_path = os.path.join(output_folder_path, relative_path)
            output_file_dir = os.path.dirname(output_file_path)

            if not os.path.exists(output_file_dir):
                os.makedirs(output_file_dir)

            Decryptor.decrypt(passphrase, input_file_path, output_file_path)

    return True
