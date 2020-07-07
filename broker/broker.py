import asyncio
import logging

from broker.clientconnection import ClientConnection
from broker.messages.messagehandler import MessageHandler

class Broker:

    def __init__(self):
        self.logger = None

        self.msg_handler = MessageHandler(self)
        self.server = None

    async def start(self, server_addr, server_port):
        self.logger = logging.getLogger('broker')
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)-5.5s] %(message)s')

        self.logger.info('Starting broker server...')

        self.server = await asyncio.start_server(self.new_client_connection, \
                            server_addr, server_port)

        self.logger.info(f'Broker server started at {server_addr}:{server_port}')

        async with self.server:
            await self.server.serve_forever()
    
    async def new_client_connection(self, reader, writer):
        new_client = ClientConnection(self, reader, writer)

        await new_client.keep_connection_alive()