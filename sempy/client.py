import requests

class Client:
    def __init__(self, host=None):
        if host is None:
            self.host = "http://localhost:5000/api"
        else:
            self.host = host
            
    def client(self, command=None, method='GET'):
        if command is None:
            self.url = self.host
        else:
            self.url = self.host + command
        if method=='POST':
            return requests.post(self.url).json()
        else:
            return requests.get(self.url).json()

    def get_info(self):
        return self.client()

    def get_account(self, address):
        command = '/account/' + str(address)
        return self.client(command)

    def get_pending_tx(self):
        command = '/transactions/pending'
        return self.client(command)

    def broadcast_rawtx(self, rawtx):
        command = '/broadcast/' + str(rawtx)
        return self.client(command, 'POST')
