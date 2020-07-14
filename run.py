import asyncio
import logging
import os

from dotenv import load_dotenv

from broker.broker import Broker

load_dotenv()
if __name__ == '__main__':
    logger = logging.getLogger('broker')

    try:
        broker_object = Broker()

        server_constants = {'SERVER_ADDRESS': os.getenv('SERVER_ADDRESS'), \
                            'SERVER_PORT': os.getenv('SERVER_PORT')}
        database_constants = {'DATABASE_ADDRESS': os.getenv('DATABASE_ADDRESS'), \
                            'DATABASE_USERNAME': os.getenv('DATABASE_USERNAME'), \
                            'DATABASE_PASSWORD': os.getenv('DATABASE_PASSWORD'), \
                            'DATABASE_NAME': os.getenv('DATABASE_NAME')}

        asyncio.run(broker_object.start(server_constants, database_constants))
    except KeyboardInterrupt:
        logger.info('Shutting down broker server...')