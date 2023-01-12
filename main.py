import os
import bcrypt
import base64
import tkinter as tk
from tkinter import filedialog
from colorama import Fore, Style
from cryptography.fernet import Fernet

def encrypt(password: object, input_file_path: object, output_file_path: object) -> object:
    # Erstellen eines zufälligen Saltwerts
    salt = os.urandom(16)

    # Erstellen des Schlüssels mit Bcrypt
    key = bcrypt.kdf(
        password=password.encode(),  # Passwort wird in Bytes umgewandelt
        salt=salt,
        desired_key_bytes=32,
        rounds=1000
    )



    # Ermitteln des Dateityps
    _, file_extension = os.path.splitext(input_file_path)

    # Dateityp als Zeichenfolge codieren
    file_extension_encoded = file_extension.encode('utf-8')

    # Base64-codieren des Schlüssels und Konvertierung in bytes
    key_base64 = base64.b64encode(key).decode('utf-8')
    key_bytes = key_base64.encode('utf-8')

    # Erstellen des Fernet-Objekts mit dem codierten Schlüssel
    fernet = Fernet(key_bytes)


    # Versuch, die Datei zu öffnen und zu lesen
    try:
        with open(input_file_path, 'rb') as input_file:
            data = input_file.read()
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error reading the file: {e}' + Style.RESET_ALL)
        return

    # Versuch, die Daten zu verschlüsseln
    try:
        encrypted_data = fernet.encrypt(data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error encrypting the file: {e}' + Style.RESET_ALL)
        return

    # Versuch, die verschlüsselten Daten in eine neue Datei zu schreiben
    try:
        with open(output_file_path, 'wb') as output_file:
            # Schreibe Saltwert und Dateityp am Anfang der Datei
            output_file.write(salt)
            output_file.write(file_extension.encode())
            output_file.write(encrypted_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error writing the encrypted file {output_file_path}: {e}' + Style.RESET_ALL)
        return


def decrypt(password, input_file_path, output_file_path):
    # Lesen des Saltwerts und des Dateityps aus der verschlüsselten Datei
    try:
        with open(input_file_path, 'rb') as input_file:
            salt = input_file.read(16)
            file_extension = input_file.read(4)
            encrypted_data = input_file.read()
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error reading the encrypted file: {e}' + Style.RESET_ALL)
        return

    # Überprüfen, ob der Saltwert 16 Bytes lang ist
    if len(salt) != 16:
        print(Fore.LIGHTRED_EX + "Error: Invalid salt length." + Style.RESET_ALL)
        return

    # Erstellen des Schlüssels mit Bcrypt
    key = bcrypt.kdf(
        password=password.encode(),  # Passwort wird in Bytes umgewandelt
        salt=salt,
        desired_key_bytes=32,
        rounds=1000
    )

    # Überprüfen, ob der Schlüssel tatsächlich 32 Bytes lang ist
    if len(key) != 32:
        print(Fore.LIGHTRED_EX + "Error: Invalid key length." + Style.RESET_ALL)
        return

    # Base64-codieren des Schlüssels und Konvertierung in bytes
    key_base64 = base64.b64encode(key).decode('utf-8')
    key_bytes = key_base64.encode('utf-8')

    # Erstellen des Fernet-Objekts mit dem codierten Schlüssel
    fernet = Fernet(key_bytes)

    # Ausgabe des Dateityps am Anfang der Datei
    print(Fore.LIGHTWHITE_EX + f'File extension: {file_extension.decode()}')

    # Versuch, die verschlüsselten Daten zu entschlüsseln
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error decrypting the file: {e}' + Style.RESET_ALL)
        return

    # Versuch, die entschlüsselten Daten in eine neue Datei zu schreiben
    try:
        with open(output_file_path, 'wb') as output_file:
            output_file.write(decrypted_data)
            output_file.write(b'.')
            output_file.write(file_extension)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'Error writing the decrypted file {output_file_path}: {e}' + Style.RESET_ALL)
        return

    # Fragen, ob die ursprüngliche verschlüsselte Datei gelöscht werden soll
    delete_input_file = input(Fore.LIGHTYELLOW_EX + 'Do you want to delete the original encrypted file? (y/n) ' + Style.RESET_ALL)
    if delete_input_file.lower() == 'y':
        try:
            os.remove(input_file_path)
            print(Fore.LIGHTGREEN_EX + f'The file {input_file_path} has been successfully deleted.' + Style.RESET_ALL)
        except OSError:
            print(Fore.LIGHTRED_EX + f'Error deleting the file {input_file_path}' + Style.RESET_ALL)

def get_file_path(file_type: str) -> str:
    # Erstellen des Dialogs zur Dateiauswahl
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
        print(Fore.LIGHTGREEN_EX + "+-------------+-------------------------+")
        print(Fore.LIGHTGREEN_EX + "| Option      | Description             |")
        print(Fore.LIGHTGREEN_EX + "+-------------+-------------------------+")
        print(Fore.LIGHTBLUE_EX + "| 1           | Encrypt a file          |")
        print(Fore.LIGHTBLUE_EX + "| 2           | Decrypt a file          |")
        print(Fore.LIGHTBLUE_EX + "| 3           | Exit                    |")
        print(Fore.LIGHTGREEN_EX + "+-------------+-------------------------+")

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
