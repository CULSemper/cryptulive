import random
import qrcode

def generate_passphrases(num_words: int, num_passphrases: int, use_numbers: bool, word_list: list) -> list:
    passphrases = []
    for _ in range(num_passphrases):
        passphrase = ''
        for _ in range(num_words):
            if use_numbers:
                word = random.choice(word_list) + str(random.randint(0, 9))
            else:
                word = random.choice(word_list)
            passphrase += word + ' '
        passphrases.append(passphrase.strip())
    return passphrases


def save_passphrase_as_text(passphrase: str, output_file_path: str):
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(passphrase)
        print(f"Passphrase saved as text file: {output_file_path}")
    except Exception as e:
        print(f"Error writing the passphrase to a text file: {e}")


def save_passphrase_as_qrcode(passphrase: str, output_file_path: str):
    qr = qrcode.QRCode()
    qr.add_data(passphrase)
    qr.make(fit=True)
    try:
        image = qr.make_image(fill_color="black", back_color="white")
        image.save(output_file_path)
        print(f"Passphrase saved as QR code: {output_file_path}")
    except Exception as e:
        print(f"Error saving the passphrase as a QR code: {e}")