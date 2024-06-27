import unittest
from decryptor import Decryptor

class TestDecryptor(unittest.TestCase):

    def setUp(self):
        # Vorbereiten der Testdateien für Passwort und Passphrase
        pass

    def tearDown(self):
        # Aufräumen der Testdateien
        pass

    def test_decrypt_with_password_success(self):
        # Teste die erfolgreiche Entschlüsselung mit einem Passwort
        result = Decryptor.decrypt('lol', 'testde.cul', 'test_output_file')
        self.assertTrue(result)

    def test_decrypt_with_passphrase_success(self):
        # Teste die erfolgreiche Entschlüsselung mit einer Passphrase
        result = Decryptor.decrypt('mortality compound confound operative amuck', 'test_encrypted_with_passphrase.cul', 'test_output_file')
        self.assertTrue(result)

    def test_decrypt_wrong_password(self):
        # Teste die Reaktion auf ein falsches Passwort
        result = Decryptor.decrypt('wrong_password', 'test_encrypted_with_password.cul', 'test_output_file')
        self.assertFalse(result)

    def test_decrypt_wrong_passphrase(self):
        # Teste die Reaktion auf eine falsche Passphrase
        result = Decryptor.decrypt('wrong passphrase', 'test_encrypted_with_passphrase.cul', 'test_output_file')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
