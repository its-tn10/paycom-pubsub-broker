import asyncio
import logging

from broker.client import Client
from broker.database import db
from broker.messages.messagehandler import MessageHandler

class Broker:

    def __init__(self):
        self.logger = None

        self.database = db

        self.msg_handler = MessageHandler(self)
        self.server = None

    async def start(self, server_constants, database_constants):
        self.logger = logging.getLogger('broker')
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)-5.5s] %(message)s')

        self.logger.info('Starting broker server...')

        self.server = await asyncio.start_server(self.new_client_connection, \
                            server_constants['SERVER_ADDRESS'], server_constants['SERVER_PORT'])

        self.logger.info(f'Broker server started at {server_constants["SERVER_ADDRESS"]}:{server_constants["SERVER_PORT"]}')

        await self.database.set_bind('postgresql://{}:{}@{}/{}'.format(
                            database_constants['DATABASE_USERNAME'], database_constants['DATABASE_PASSWORD'],
                            database_constants['DATABASE_ADDRESS'], database_constants['DATABASE_NAME']))

        self.logger.info('Connected to PostgreSQL server - all operations good!')

        async with self.server:
            await self.server.serve_forever()
    
    async def new_client_connection(self, reader, writer):
        new_client = Client(self, reader, writer)

        await new_client.keep_connection_alive()