import click
import os
import sys

from sempy.cli.create import create
from sempy.cli.transfer import transfer
from sempy.cli.listacc import listacc
from sempy.cli.balance import balance

@click.group()
@click.option('--server', default='http://45.32.185.200/api', envvar='SEMPY_SERVER', help='url for sempy server ')
@click.option('--wallet-dir', default=None, envvar="WALLET_DIR",help='specify directory where to find wallet.txt, absolute path needed')
def main(server, wallet_dir):
    os.environ['SEMPY_SERVER'] = server
    if wallet_dir is None and ('WALLET_DIR' not in os.environ):
        wallet_dir = os.path.expanduser('~'+os.environ['USERNAME'])
        os.environ['WALLET_DIR'] = wallet_dir
    else:
        if not os.path.isdir(wallet_dir):
            print("error invalid wallet dir %s" % wallet_dir)
            print("set wallet dir using, `sempy-cli.py --wallet-dir WALLET_DIR`")
            sys.exit()

main.add_command(create)
main.add_command(transfer)
main.add_command(listacc)
main.add_command(balance)

if __name__ == '__main__':
    main()
