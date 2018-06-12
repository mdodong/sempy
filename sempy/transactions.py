from semux.hash import hash256
from semux.key import Key
from .utils import SimpleEncoder


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

class Transactions:
    def __init__(self, networkId, txType, sendTo, value, fee, nonce,
                 timestamp, data):
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
        self.timestamp = timestamp
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
        self.signature = account.sign(self.txHash)

    def txHash(self):
        return self.txHash

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

    
        
