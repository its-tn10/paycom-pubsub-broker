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
        asyncio.run(broker_object.start(os.getenv('SERVER_ADDRESS'), os.getenv('SERVER_PORT')))
    except KeyboardInterrupt:
        logger.info('Shutting down broker server...')