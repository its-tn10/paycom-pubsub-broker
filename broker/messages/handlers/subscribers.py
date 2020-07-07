
'''

This module contains all of the base-line needs that a subscriber client
would like to do.

Handled JSON action messages:

* list_topics(): Broker server returns all of the topics created from publishers. 

* subscribe(topic_name): Allows a subscriber to subscribe to a particular topic,
  and begin receiving messages that get published towards this topic.

* unsubscribe(topic_name): Allows a subscriber to unsubscribe to a particular topic,
  and halt all messages to be received from this particular subscriber in a given topic.

'''

async def list_topics(client):
    client.server.logger.info('TODO: Implement list_topics() in subscribers.py')

async def subscribe(client, topic_name):
    client.server.logger.info('TODO: Implement subscribe() in subscribers.py')

async def unsubscribe(client, topic_name):
    client.server.logger.info('TODO: Implement unsubscribe() in subscribers.py')
