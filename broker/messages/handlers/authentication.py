
'''

This module contains all of the base-line authentication needs before
enduring any actions received from the client. 

Handled JSON action messages:

* create(user_email, user_type): Allows the client to create a user
  account, and will be identified as a pub or a sub with the 'type'
  parameter.

* connect(user_email): Allows the client to login to a created
  user account. Will be identified as a pub or a sub later on.

* disconnect(): Allows the client to disconnect from the broker server.

'''

from broker.constants.general import PUBLISHER_TYPE, SUBSCRIBER_TYPE, USER_TYPES
from broker.constants.errors import EMAIL_EXISTS_MSG, INVALID_USER_TYPE_MSG

from broker.database.client import Client

async def create(client, user_email, user_type):
    db = client.server.database
    email_exists = await db.scalar(db.exists().where(Client.email == user_email).select())

    if email_exists:
      return await client.send_error_msg(EMAIL_EXISTS_MSG)
    
    if user_type.lower() not in USER_TYPES:
      return await client.send_error_msg(INVALID_USER_TYPE_MSG)
    
    is_publisher = user_type.lower() == PUBLISHER_TYPE
    is_subscriber = user_type.lower() == SUBSCRIBER_TYPE

    account = await Client.create(email = user_email, publisher = is_publisher, \
                        subscriber = is_subscriber)

    client.__dict__.update(**account.to_dict())
    await client.send_success_msg(0)
    
async def connect(client, user_email):
    client.server.logger.info('TODO: Implement connect() in authentication.py')

async def disconnect(client):
    client.server.logger.info('TODO: Implement disconnect() in authentication.py')
