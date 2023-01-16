import os
import bcrypt
import base64
import tkinter as tk
from tkinter import filedialog
from colorama import Fore, Style
from cryptography.fernet import Fernet

def encrypt(password: object, input_file_path: object, output_file_path: object) -> object:

    # Generating a random salt value
    salt = os.urandom(16)

    # Create the key with Bcrypt
    key = bcrypt.kdf(
        password=password.encode(),  # Password is converted to bytes
        salt=salt,
        desired_key_bytes=32,
        rounds=1000
    )



    # Determine the file type
    _, file_extension = os.path.splitext(input_file_path)

    # Encode file type as string
    file_extension_encoded = file_extension.encode('utf-8')

    # Base64-encode the key and convert it to bytes
    key_base64 = base64.b64encode(key).decode('utf-8')
    key_bytes = key_base64.encode('utf-8')

    # Create the Fernet object with the encrypted key
    fernet = Fernet(key_bytes)


    # Attempt to open and read the file
    try:
        with open(input_file_path, 'rb') as input_file:
            data = input_file.read()
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error reading the file: {e}' + Style.RESET_ALL)
        return

    # Attempt to encrypt the data
    try:
        encrypted_data = fernet.encrypt(data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error encrypting the file: {e}' + Style.RESET_ALL)
        return

    # Attempt to write the encrypted data to a new file
    try:
        with open(output_file_path, 'wb') as output_file:
            # Write salt value and file type at the beginning of the file
            output_file.write(salt)
            output_file.write(file_extension.encode())
            output_file.write(encrypted_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error writing the encrypted file {output_file_path}: {e}' + Style.RESET_ALL)
        return


def decrypt(password, input_file_path, output_file_path):
    # Read the salt value and file type from the encrypted file
    try:
        with open(input_file_path, 'rb') as input_file:
            salt = input_file.read(16)
            file_extension = input_file.read(4).decode() # Decode the file extension
            encrypted_data = input_file.read()
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error reading the encrypted file: {e}' + Style.RESET_ALL)
        return

    # Check if the salt value is 16 bytes long
    if len(salt) != 16:
        print(Fore.LIGHTRED_EX + "Error: Invalid salt length." + Style.RESET_ALL)
        return

    # Create the key with Bcrypt
    key = bcrypt.kdf(
        password=password.encode(),  # Password is converted to bytes
        salt=salt,
        desired_key_bytes=32,
        rounds=1000
    )

    # Check if the key is actually 32 bytes long
    if len(key) != 32:
        print(Fore.LIGHTRED_EX + "Error: Invalid key length." + Style.RESET_ALL)
        return

    # Base64-encode the key and convert it to bytes
    key_base64 = base64.b64encode(key).decode('utf-8')
    key_bytes = key_base64.encode('utf-8')

    # Create the Fernet object with the encrypted key
    fernet = Fernet(key_bytes)

    # Attempt to decrypt the data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error decrypting the file: {e}' + Style.RESET_ALL)
        return

    # Attempt to write the decrypted data to a new file with the file extension
    try:
        with open(output_file_path + file_extension, 'wb') as output_file:
            output_file.write(decrypted_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error writing the decrypted file {output_file_path}: {e}' + Style.RESET_ALL)
        return


def get_file_path(file_type: str) -> str:
    # Creating the file selection dialog
    root = tk.Tk()
    root.withdraw()

    if file_type == 'input':
        file_path = filedialog.askopenfilename(title='Select the input file')
    elif file_type == 'output':
        file_path = filedialog.asksaveasfilename(title='Select the output file location')

    return file_path

def main():
    os.system("title CryptULive")

    while True:
        print(Fore.LIGHTWHITE_EX + "+-------------+-------------------------+" + Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + "| Option      | Description             |" + Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + "+-------------+-------------------------+" + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "| 1           | Encrypt a file          |" + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "| 2           | Decrypt a file          |" + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "| 3           | Exit                    |" + Style.RESET_ALL)
        print(Fore.LIGHTWHITE_EX + "+-------------+-------------------------+" + Style.RESET_ALL)

        choice = input(Fore.LIGHTMAGENTA_EX + "Enter your choice: ")

        if choice == '1':
            password = input(Fore.LIGHTWHITE_EX + "Enter the password: ")
            input_file_path = get_file_path('input')
            if not input_file_path:
                return
            output_file_path = get_file_path('output')
            if not output_file_path:
                return

            output_file_path = output_file_path + '.cul'
            encrypt(password, input_file_path, output_file_path)
            print(Fore.LIGHTGREEN_EX + "File Encrypted successfully!")
        elif choice == '2':
            password = input("Enter the password: ")
            input_file_path = get_file_path('input')
            if not input_file_path:
                return
            output_file_path = get_file_path('output')
            if not output_file_path:
                return

            decrypt(password, input_file_path, output_file_path)
            print(Fore.LIGHTGREEN_EX + "File Decrypted successfully!")
        elif choice == '3':
            print(Fore.LIGHTYELLOW_EX + "Exiting..." + Style.RESET_ALL)
            break
        else:
            print(Fore.LIGHTRED_EX + 'Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
