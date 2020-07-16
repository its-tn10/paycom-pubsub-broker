import asyncio
import logging

from broker.client import Client
from broker.database import db
from broker.database.publishing import Topic, Message
from broker.messages.messagehandler import MessageHandler

class Broker:

    def __init__(self):
        self.logger = None

        self.clients = []
        self.database = db
        self.topics = {}

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

        self.logger.info('Connected to PostgreSQL server')

        await self.load_data()

        self.logger.info('All operations are running! Listening to clients...')

        async with self.server:
            await self.server.serve_forever()
    
    async def load_data(self):
        await self.load_topics()
        await self.load_messages()

        self.logger.info(f'Pre-loaded {len(self.topics)} topics their respective messages')

    async def load_topics(self):   
        async with self.database.transaction():
            async for topic in Topic.query.order_by(Topic.id).gino.iterate():
                self.topics[topic.id] = topic
    
    async def load_messages(self):
        async with self.database.transaction():
            async for msg in Message.query.order_by(Message.id).gino.iterate():
                self.topics[msg.topic_id].messages.append(msg)

    async def new_client_connection(self, reader, writer):
        new_client = Client(self, reader, writer)
        self.clients.append(new_client)
        
        await new_client.keep_connection_alive()