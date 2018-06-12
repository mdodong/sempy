import os
import json
import sys
import string

from sempy.client import Client
from sempy.account import Account
from sempy.transactions import Transactions
from pathlib import Path

def checkWallet():
    """
    Check if wallet file exists in the  wallet_dir
    """
    wallet_file = Path((os.environ['WALLET_DIR'] + "\\wallet.txt"))
    return wallet_file.is_file()


def checkAccount(accountIndex=0):
    """
    Check if wallet.txt contains valid addresses and private key

    returns an Account object if all checks are done correctly
    """
    if checkWallet():
        wallet_file = os.environ['WALLET_DIR'] + "\\wallet.txt"
        with open(wallet_file) as f:
            data = json.load(f)
    else:
        sys.exit('wallet file not found')
    if type(data).__name__ != 'dict':
        sys.exit('invalid wallet format')
    elif 'wallets' not in data.keys():
        sys.exit('invalid wallet format')
    elif type(data['wallets']).__name__ != 'list':
        sys.exit('invalid wallet format')
    elif len(data['wallets']) <= 0:
        sys.exit('no {address:private_key} found on wallet.txt')
    else:
        for k, v in data['wallets'][accountIndex].items():
            add = k[2:] if k[:2] == '0x' else k
            privk = v[2:] if v[:2] == '0x' else v

    # check if address and private key is has the correct length
    if len(add) is not 40:
        sys.exit('invalid address length')
    elif len(privk) is not 96:
        sys.exit('invalid private key length')
    else:
        return Account(privk)

def checkAddress(address):
    """
    Check if address is a valid semux address
    """
    add = address[2:] if address[:2] == '0x' else address
    if len(add) != 40:
        return False
    elif not is_hex(add):
        return False
    else:
        return True

def is_hex(s):
     hex_digits = set(string.hexdigits)
     # if s is long, then it is faster to check against a set
     return all(c in hex_digits for c in s)



