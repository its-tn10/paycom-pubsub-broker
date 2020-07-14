
'''

This module contains all of the base-line authentication needs before
enduring any actions received from the client. 

Handled JSON action messages:

* create(email, type): Allows the client to create a user
  account, and will be identified as a pub or a sub with the 'type'
  parameter.

* connect(email): Allows the client to login to a created
  user account. Will be identified as a pub or a sub later on.

* disconnect(): Allows the client to disconnect from the broker server.

'''

async def create(client, email, type):
    client.server.logger.info('TODO: Implement create() in authentication.py')

async def connect(client, email):
    client.server.logger.info('TODO: Implement connect() in authentication.py')

async def disconnect(client):
    client.server.logger.info('TODO: Implement disconnect() in authentication.py')
