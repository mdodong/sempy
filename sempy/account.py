from semux.key import Key, verify_message
from semux.encoding import from_pkcs8
from semux.hash import hash256
from semux.signature import Signature
import binascii

class Account:
    def __init__(self, privk=None):
        if privk is None:
            self.acc = Key.from_random()
        else:
            if privk[:2] == '0x':
                self.acc = Key.from_seed(from_pkcs8(binascii.unhexlify(privk[2:])))
            else:
                self.acc = Key.from_seed(from_pkcs8(binascii.unhexlify(privk)))
        self.address = '0x' + self.acc.to_address().decode()
        self.privk = '0x' + binascii.hexlify(self.acc.encoded_private).decode()

    def getAddress(self):
        return self.address

    def getPrivateKey(self):
        return self.privk

    def signTx(self, tx):
        """
        Sign a tx from sempy.transaction.Transactions()
        Args:
            tx (Transactions.txHash): Unsigned Transaction Hash
        Returns:
            signature (Transactions.signature): signature to be added on Transaction data 
        """
        return self.acc.sign(tx)
    
    def signMessage(self, message):
        """
        Sign a plain text message.
        Args:
            message (str): plain text message
        Returns:
            hex. signed message in hex format.
        """
        sig = self.acc.sign(hash256(message.encode()))
        return binascii.hexlify(sig.to_bytes())
