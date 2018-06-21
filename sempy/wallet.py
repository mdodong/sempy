import os
import sys
import json
import string

from sempy.account import Account
from sempy.encryption import encrypt, decrypt

WALLET_VERSION = 1
NETWORK = "MAINNET"

class Wallet():
    def __init__(self, password, wallet_file=None, privk=None):
        if wallet_file is None:
            self.wallet = sys.path[0] + "\\wallet.json"
        else:
            self.wallet = wallet_file

        if os.path.isfile(self.wallet):
            self.validateWallet(self.wallet)
        else:
            if privk is None:
                self.createNewWallet(password)
            else:
                self.createNewWallet(password, privk)

    def createNewWallet(self, password, privk=None):
        self.wallet_version = WALLET_VERSION
        self.network = NETWORK
        self.salt = os.urandom(16)
        self.iv = os.urandom(16)
        account = self.createNewAccount(password, privk)
        self.wallet_data = {
            "version": self.wallet_version,
            "network": self.network,
            "cipher": {
                "salt": self.salt.hex(),
                "iv": self.iv.hex()
                },
            "accounts": [
                {
                    "address": account["address"],
                    "encrypted": account["encrypted"]
                }
            ]
        }

        self.wallet = sys.path[0] + "\\wallet.json"
        with open(self.wallet, 'w') as outfile:
            json.dump(self.wallet_data, outfile, indent=4)

        


    def validateWallet(self, walletfile):
        try:
            with open(walletfile, 'rb') as w:
                self.wallet_data = w.read()
            if self.wallet_data["version"] != WALLET_VERSION:
                raise Exception("Unrecognized wallet file version.")
            elif self.wallet_data["network"].upper() != NETWORK:
                raise Exception("Invalid Network!. Must use {}".format(NETWORK))
            elif "cipher" not in self.wallet_data:
                raise Exception("missing, 'cipher'")
            elif "salt" not in self.wallet_data["cipher"]:
                raise Exception("missing, cipher['salt']")
            elif "iv" not in self.wallet_data["cipher"]:
                raise Exception("missing, cipher['iv']")
            elif not isinstance(wallet_data["accounts"], list):
                raise Exception("Invalid 'accounts' format")
            elif len(wallet_data["accounts"]) < 1:
                raise Exception("Empty 'accounts' on wallet.")
            elif "address" not in wallet_data["accounts"][0]:
                raise Exception("Missing accounts['address'] on wallet.")
            elif "encrypted" not in wallet_data["accounts"][0]:
                raise Exception("Missing accounts['encrypted'] on wallet.")
            else:
                self.wallet_version = self.wallet_data["version"]
                self.network = self.wallet_data["network"].upper()
                self.salt = self.wallet_data["cipher"]["salt"]
                self.iv = self.wallet_data["cipher"]["iv"]
                self.accounts = wallet_data["accounts"]
        except:
            print("Error, Invalid Wallet Format!")


    def createNewAccount(self, password, privk=None):
        acc = Account(privk)
        pk = acc.getPrivateKey()[2:]
        print(pk, self.salt.hex(), self.iv.hex())
        encrypted = encrypt(password, self.salt, self.iv, pk.encode())
        address = acc.getAddress()
        return {"address": address, "encrypted": encrypted.hex()}


    def is_hex(self, s):
        hex_digits = set(string.hexdigits)
        # if s is long, then it is faster to check against a set
        return all(c in hex_digits for c in s)

    
