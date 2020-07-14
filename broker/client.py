from broker.clientconnection import ClientConnection

class Client(ClientConnection):

    def __init__(self, *args):
        super().__init__(*args)
    
        self.authenticated = False
        self.data = None