import os
import click
import json

from sempy.account import Account
from pathlib import Path

@click.command()
@click.option('--privk', default=None, help='user privk')
def create(privk):
    wallet_dir = os.environ['WALLET_DIR']
    wallet_path = wallet_dir + "\\wallet.txt"
    wallet_file = Path(wallet_path)
    w = new_wallet(privk)
    if wallet_file.is_file():
        # read existing wallet
        with open(wallet_path) as f:
            data = json.load(f)
            # add new wallet to wallet data
            data['wallets'].append(w)
        # write wallet data to wallet file
        with open(wallet_path, 'w') as outfile:
            json.dump(data, outfile)
        print('added new wallet in ', wallet_dir)
    else:
        data = {"wallets":[w]}
        with open(wallet_path, 'w') as outfile:
            json.dump(data, outfile)
            print('new wallet created in ', wallet_dir)


def new_wallet(privk):
    acc = Account(privk)
    add = acc.getAddress()
    priv_k = acc.getPrivateKey()
    return {add:priv_k}
