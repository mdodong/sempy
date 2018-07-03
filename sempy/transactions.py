import sys
import time
import binascii

from semux.hash import hash256
from semux.key import Key
from sempy.utils import SimpleEncoder
from sempy.client import Client

SERVER = "http://45.32.185.200/api"


TRANSACTION_TYPE = {
    "COINBASE" : 0x00,
    "TRANSFER" : 0x01,
    "DELEGATE" : 0x02,
    "VOTE"     : 0x03,
    "UNVOTE"   : 0x04,
    "CREATE"   : 0x05,
    "CALL"     : 0x06
    }

NETWORK = {
    'mainnet':0x00,
    'testnet':0x01,
    'devnet' :0x02}

NET = NETWORK['mainnet']

class Transactions:
    def __init__(self, networkId, txType, sendTo, value, fee, nonce,
                 timestamp=None, data=None):
        """
        Create and initialize a transaction object

        Args:
            networkId (int): {"mainnet":0, "testnet":1, "devnet":2}
            txType    (int): see TRANSACTION_TYPE
            sendTo    (str): semux address(without the 0x)
            value     (int): value in NANO sem
            fee       (int): transaction fee in NANO sem
            nonce     (int): nonce from the sending account
            timestamp (int): timestamp in milliseconds int(time.time()*1000)
            data      (bytearray): data string encoded in bytearray('data'.encode())
        """
        self.networkId = networkId
        self.txType = txType
        self.sendTo = sendTo
        self.value = value
        self.fee = fee
        self.nonce = nonce
        
        if timestamp is None:
            self.timestamp = int(time.time()*1000)
        else:
            self.timestamp = timestamp
        
        if data is None:
            self.data = bytearray(b'')
        else:
            self.data = data
        

        # encode Transaction Data
        enc = SimpleEncoder()
        enc.writeByte(networkId)
        enc.writeByte(txType)
        enc.writeBytes(bytearray.fromhex(sendTo)) 
        enc.writeAmount(value)
        enc.writeAmount(fee)
        enc.writeLong(nonce)
        enc.writeLong(timestamp)
        enc.writeBytes(data)
        
        self.encoded = enc.toBytes()
        self.txHash = hash256(self.encoded)
        self.signed = False

    def signTx(self, account):
        self.signed = True
        self.signature = account.signTx(self.txHash)

    def getTxHash(self):
        return binascii.hexlify(self.toBytes()).decode()

    def txUnsigned(self):
        return self.encoded

    def isSigned(self):
        return self.signed

    def toBytes(self):
        if self.isSigned():
            enc = SimpleEncoder()
            enc.writeBytes(self.txHash)
            enc.writeBytes(self.encoded)
            enc.writeBytes(self.signature.to_bytes())
            return enc.toBytes()
        else:
            return self.encoded

    
        
class Executor:
    def __init__(self, account):
        self.client = Client(SERVER)
        self.account = account
        self.address = account.getAddress()
        account = self.client.get_account(self.address)
        self.nonce = int(account['result']['nonce'])
        self.available_balance = int(account['result']['available'])
        self.locked_balance = int(account['result']['locked'])
        self.total_balance = self.available_balance + self.locked_balance

    def send(self, sendTo, amount, fee=0.05, data=''):
        SEND = TRANSACTION_TYPE['TRANSFER']
        if sendTo[:2] == '0x':
            address = sendTo[2:]
        else:
            address = sendTo

        amount = int(amount * 1000000000)
        fee = int(fee * 100000000)
        ts = int(time.time() * 1000)
        if data is not '':
            data = bytearray(data.encode())
        if self.total_balance < (amount+fee):
            return 'Insufficient Funds'
        else:
            sendTx = Transactions(NET, SEND, address, amount, fee, self.nonce, ts, data)
            sendTx.signTx(self.account)
            raw = '0x' + sendTx.getTxHash()
            return self.client.broadcast_rawtx(raw)

    def vote(self, voteTo, amount, fee=0.05, data=''):
        VOTE = TRANSACTION_TYPE['VOTE']
        if voteTo[:2] == '0x':
            address = voteTo[2:]
        else:
            address = voteTo

        amount = int(amount * 1000000000)
        fee = int(fee * 100000000)
        ts = int(time.time() * 1000)
        if data is not '':
            data = bytearray(data.encode())
        if self.total_balance < (amount+fee):
            return 'Insufficient Funds'
        else:
            voteTx = Transactions(NET, VOTE, address, amount, fee, self.nonce, ts, data)
            voteTx.signTx(self.account)
            raw = '0x' + voteTx.getTxHash()
            return self.client.broadcast_rawtx(raw)

    def unvote(self, voteTo, amount, fee=0.05, data=''):
        UNVOTE = TRANSACTION_TYPE['UNVOTE']
        if sendTo[:2] == '0x':
            address = voteTo[2:]
        else:
            address = voteTo
            
        active_votes = 
        amount = int(amount * 1000000000)
        fee = int(fee * 100000000)
        ts = int(time.time() * 1000)
        if data is not '':
            data = bytearray(data.encode())

        if self.locked_balance == 0:
            return 'You have no active votes'
        
        elif amount > self.locked_balance:
            return 'Insuficient Votes! You can only UNVOTE <= %f' %(amount/1000000000)

        else:
            active_votes = int(self.client.get_vote(voteTo, self.address)['result'])
            if amount > active_votes:
                return 'Insuficient Votes! You can only UNVOTE <= %f' %(amount/1000000000)
            else:
                unvoteTx = Transactions(NET, VOTE, address, amount, fee, self.nonce, ts, data)
                unvoteTx.signTx(self.account)
                raw = '0x' + unvoteTx.getTxHash()
                return self.client.broadcast_rawtx(raw)

        
        
