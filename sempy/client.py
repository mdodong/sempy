import requests

class Client:
    def __init__(self, host=None):
        if host is None:
            self.host = "http://localhost:5000/api"
        else:
            self.host = host
            
    def client(self, command=None, params_=None, method='GET'):
        if command is None:
            self.url = self.host
        else:
            self.url = self.host + command
        if method=='POST':
            return requests.post(self.url, params=params_).json()
        else:
            return requests.get(self.url, params=params_).json()

    def get_info(self):
        return self.client()

    def get_server_info(self):
        return self.client('/info')

    
    def get_delegates(self):
        return self.client('/delegates')

    def get_votes(self, delegate):
        params = {'delegate' : delegate}
        return self.client('/votes', params)

    def get_account(self, address):
        params = {'address' : address}
        return self.client('/account', params)

    def get_balance(self, address):
        info = self.get_account(address)
        return {'available':info['result']['available'], 'locked':info['result']['locked']}

    def get_nonce(self, address):
        info = self.get_account(address)
        return {'nonce':info['result']['nonce']}

    def get_transaction_count(self, address):
        info = self.get_account(address)
        return {'transactionCount':info['result']['transactionCount']}

    def get_account_transactions(self, address, start, end):
        params = {'address' : address, 'from': start, 'to':end}
        return self.client('/account/transactions', params)

    def broadcast_rawtx(self, rawtx):
        params = {'raw' : rawtx}
        return self.client('/transaction/raw', params, 'POST')
