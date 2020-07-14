from broker.database import client
from broker.clientconnection import ClientConnection

class Client(ClientConnection, client.Client):

    def __init__(self, *args):
        super().__init__(*args)
    