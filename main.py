import os
import logger
from colorama import Fore, Style
from encryptor import Encryptor
from decryptor import Decryptor
from folder_decryptor import decrypt_folder
from file_handler import get_file_path, get_folder_path
from folder_encryptor import encrypt_folder
from passphrase_manager import generate_passphrases, save_passphrase_as_text, save_passphrase_as_qrcode

word_list = []

def process_encryption(word_list):
    encryption_method = input("Select encryption method (1: passphrase, 2: password): ")
    if encryption_method == '1':
        passphrase_choice = input("Enter the passphrase or generate it (g): ")
        if passphrase_choice.lower() == 'g':
            num_words = int(input("Enter the number of words per passphrase: "))
            num_passphrases = 1
            use_numbers = input("Include numbers at the end of words? (y/n): ").lower() == 'y'
            passphrases = generate_passphrases(num_words, num_passphrases, use_numbers, word_list)
            print("Generated Passphrase:")
            for passphrase in passphrases:
                print(passphrase)
            passphrase = passphrases[0]
        else:
            passphrase = passphrase_choice.strip()
    elif encryption_method == '2':
        passphrase = input("Enter the password: ")

    method = input("Choose method (1: File, 2: Folder): ")
    if method == '1':
        # Datei verschlüsseln
        input_file_path = get_file_path('input')
        output_file_path = get_file_path('output') + '.cul'
        Encryptor.encrypt(passphrase, input_file_path, output_file_path)
        print("File Encrypted successfully!")
    elif method == '2':
        # Ordner verschlüsseln
        input_folder_path = get_folder_path()
        output_folder_path = get_folder_path()
        encrypt_folder(passphrase, input_folder_path, output_folder_path)
        print("Folder Encrypted successfully!")

    # Speichern der Passphrase/Passworts
    save_choice = input("Do you want to save the passphrase/password? (y/n): ")
    if save_choice.lower() == 'y':
        save_format = input("Select passphrase/password save format (text/qr): ")
        if save_format == 'text':
            output_passphrase_path = get_file_path('output') + '_passphrase.txt'
            save_passphrase_as_text(passphrase, output_passphrase_path)
        elif save_format == 'qr':
            output_passphrase_path = get_file_path('output') + '_passphrase.png'
            save_passphrase_as_qrcode(passphrase, output_passphrase_path)

def process_decryption():
    method = input("Choose method (1: File, 2: Folder): ")
    passphrase = input("Enter the passphrase or password: ")

    if method == '1':
        # Einzelne Datei entschlüsseln
        input_file_path = get_file_path('input')
        output_file_path = get_file_path('output')
        Decryptor.decrypt(passphrase, input_file_path, output_file_path)
    elif method == '2':
        # Ordner entschlüsseln
        input_folder_path = input("Enter the input folder path: ")
        output_folder_path = input("Enter the output folder path: ")
        decrypt_folder(passphrase, input_folder_path, output_folder_path)

def main():
    global word_list
    os.system("title CryptULive")

    word_list_path = "wordlist.txt"
    # Versuche, die Wortliste zu laden.
    try:
        with open(word_list_path, 'r') as word_list_file:
            word_list = [line.strip() for line in word_list_file]
    except Exception as e:
        print(f"Error loading the word list: {e}")
        return  # Oder handle den Fehler, anstatt zu beenden.

    while True:

            print(Fore.LIGHTWHITE_EX + "+-------------+-------------------------+" + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + "| Option      | Description             |" + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + "+-------------+-------------------------+" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "| 1           | Encrypt file/folder     |" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "| 2           | Decrypt file/folder     |" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "| 3           | Exit                    |" + Style.RESET_ALL)
            print(Fore.LIGHTWHITE_EX + "+-------------+-------------------------+" + Style.RESET_ALL)

            choice = input(Fore.LIGHTMAGENTA_EX + "Enter your choice: ")

            if choice == '1':
                process_encryption(word_list)  # Übergib word_list hier
            elif choice == '2':
                process_decryption()  # Angenommen, diese Funktion braucht kein word_list
            elif choice == '3':
                print(Fore.LIGHTYELLOW_EX + "Exiting..." + Style.RESET_ALL)
                break

if __name__ == '__main__':
    main()