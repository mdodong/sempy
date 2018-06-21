import click
import os
import json
import sys
import time
import binascii

from sempy.client import Client
from sempy.account import Account
from sempy.transactions import Transactions, NETWORK, TRANSACTION_TYPE
from pathlib import Path

from sempy.cli.cliutils import checkWallet
from sempy.cli.cliutils import checkAccount
from sempy.cli.cliutils import checkAddress


@click.command('transfer')
@click.option('--f', default=0, help="address to send from, index from `sempy-cli.py listacc`")
@click.option('--to', default=None, help="address to recieve the transaction")
@click.option('--amount', default=0.00, help="amount to transact")
@click.option('--fee', default=0.005, help="fee to use")
@click.option('--data', default='', help='data string to be added to the transaction')
def transfer(f, to, amount, fee, data):
    if to is None:
        sys.exit('no sendTo address')
    else:
        if not checkAddress(to):
            sys.exit('invalid sendTo address')
        else:
            sendTo = to[2:] if to[:2] == '0x' else to
    server = os.environ['SEMPY_SERVER']
    acc = checkAccount(f)
    add = acc.getAddress()
    client = Client(server)
    info = client.get_account(add)
    balance = int(info['result']['available'])/1000000000
    nonce = int(info['result']['nonce'])
    ts = int(time.time()*1000)
    d = bytearray(data.encode())
    if(
        balance <= 0 or
        balance < (amount+fee)
        ):
        sys.exit('error: insufficient balance, you have %f sems in your wallet %s' % (balance, info['result']['address']))
    else:
        print('you are now transferring sems')
        print('from: %s -> to: %s' % (add, to))
        print('amount: %f, using fee: %f' % (amount, fee))
        if click.confirm('Do you want to continue sending?', abort=True):
            tx  = Transactions(NETWORK['mainnet'], TRANSACTION_TYPE['TRANSFER'],
                               sendTo, int(amount*1000000000), int(fee*1000000000),
                               nonce, ts, d)
            tx.signTx(acc)
            signedTx = '0x' + binascii.hexlify(tx.toBytes()).decode()
            #point of no return
            print('txid: %s' % client.broadcast_rawtx(signedTx)['result'])






        
            

    
    
