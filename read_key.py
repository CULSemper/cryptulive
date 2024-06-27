import os
import scrypt
import base64

def read_key_from_file(passphrase: str, file_path: str):
    try:
        with open(file_path, 'rb') as file:
            salt = file.read(16)  # Angenommene Länge des Salt
            key = scrypt.hash(passphrase.encode(), salt, N=16384, r=8, p=1, buflen=32)
            print(f"Key for {file_path}: {base64.urlsafe_b64encode(key).decode()}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def read_keys_from_folder(passphrase: str, folder_path: str):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            read_key_from_file(passphrase, file_path)

def main():
    passphrase_or_password = input("Enter 'passphrase' or 'password' to indicate the method used: ")
    passphrase = input(f"Enter the {passphrase_or_password} used for encryption: ")
    path = input("Enter the path to the file or folder: ")

    if os.path.isdir(path):
        read_keys_from_folder(passphrase, path)
    elif os.path.isfile(path):
        read_key_from_file(passphrase, path)
    else:
        print("Invalid path")

if __name__ == "__main__":
    main()
