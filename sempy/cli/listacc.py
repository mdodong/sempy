import click
from pathlib import Path
import json
import os

@click.command()
def listacc():
    wallet_dir = os.environ['WALLET_DIR']
    wallet_path = wallet_dir + "\\wallet.txt"
    wallet_file = Path(wallet_path)
    if wallet_file.is_file():
        with open(wallet_path) as f:
            data = json.load(f)
        for i in range(len(data['wallets'])):
            for address in data['wallets'][i].keys():
                print(i, address)
    else:
        print("No wallet file found, create a new wallet: ")
        print("`sempy-cli.py create`")
