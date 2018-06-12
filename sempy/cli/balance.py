import click
import json
import os
import sys
from sempy.client import Client
from pathlib import Path


@click.command()
@click.option('--address', default=None, help='check balance of a given semux address')
def balance(address):
    server = os.environ['SEMPY_SERVER']
    client = Client(server)
    if address is not None:
        info = client.get_account(address)
        add = info['result']['address']
        available = int(info['result']['available'])/1000000000
        locked = int(info['result']['locked'])/1000000000
        print('address: %s, available: %s, locked: %s'% (add, available, locked))
        sys.exit()
    wallet_dir = os.environ['WALLET_DIR']
    wallet_path = wallet_dir + "\\wallet.txt"
    wallet_file = Path(wallet_path)
    if wallet_file.is_file():
        with open(wallet_path) as f:
            data = json.load(f)
        for i in range(len(data['wallets'])):
            for address in data['wallets'][i].keys():
                info = client.get_account(address)
                add = info['result']['address']
                available = int(info['result']['available'])/1000000000
                locked = int(info['result']['locked'])/1000000000
                print('address: %s, available: %s, locked: %s'% (add, available, locked))
    else:
        print("No wallet file found, create a new wallet: ")
        print("`sempy-cli.py create`")
        print("or view balance using address: ")
        print("`sempy-cli.py balance --address 0xSEMUX_ADDRESS_HERE`")
