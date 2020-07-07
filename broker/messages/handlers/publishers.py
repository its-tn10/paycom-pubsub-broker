
'''

This module contains all of the base-line needs that a publisher client
would like to do.

Handled JSON action messages:

* create_topic(topic_name): Allows a publisher to create a topic, given
  the name of the topic. 

* publish_msg(topic_name, msg): Allows the publisher to publish a
  message to a given topic name.

'''

async def create_topic(client, topic_name):
    client.server.logger.info('TODO: Implement create_topic() in publishers.py')

async def publish_msg(client, topic_name, msg):
    client.server.logger.info('TODO: Implement publish_msg() in publishers.py')
