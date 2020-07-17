
'''

This module contains all of the base-line authentication needs before
enduring any actions received from the client. 

Handled JSON action messages:

* create(user_email, user_type): Allows the client to create a user
  account, and will be identified as a pub or a sub with the 'type'
  parameter.

* connect(user_email): Allows the client to login to a created
  user account. Will be identified as a pub or a sub later on.

'''

from broker.constants.general import PUBLISHER_TYPE, SUBSCRIBER_TYPE, USER_TYPES
from broker.constants.errors import EMAIL_EXISTS_MSG, INVALID_USER_TYPE_MSG, USER_NOT_EXIST_MSG

from broker.database.client import Client

async def authenticate_user(client, client_data):
    client.data = client_data
    client.authenticated = True

    await client.send_success_msg(0)

    if client.data.subscriber:
      return await client.subscriber_init()

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

    await authenticate_user(client, account)
    
async def connect(client, user_email):
    client_data = await Client.query.where(Client.email == user_email).gino.first()
    
    if client_data is None:
      return await client.send_error_msg(USER_NOT_EXIST_MSG)
    
    await authenticate_user(client, client_data)
