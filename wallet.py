import binascii
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

class Wallet:

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if not self.private_key or not self.private_key:
            print('Error getting the keys. Wallet not saved')
            return False

        try:
            with open('wallet.txt', mode='w') as file:
                file.write(self.public_key)
                file.write('\n')
                file.write(self.private_key)
            return True
        except (IOError, IndexError):
            print('Saving wallet failed')
            return False

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as file:
                keys = file.readlines()
                self.public_key = keys[0][:-1]  # remove the \n
                self.private_key = keys[1]
            return True
        except (IOError, IndexError):
            print('Loading wallet failed')
            return False

    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()

        private_key_str = binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
        public_key_str = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')

        return private_key_str, public_key_str

    def sign_transaction(self, sender, recepient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        hashed_message = SHA256.new((str(sender) + str(recepient) + str(amount)).encode('utf8'))
        signature = signer.sign(hashed_message)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)

        hashed_message = SHA256.new((str(transaction.sender) + 
                                     str(transaction.recipient) + 
                                     str(transaction.amount)).encode('utf8'))

        return verifier.verify(hashed_message, binascii.unhexlify(transaction.signature))
