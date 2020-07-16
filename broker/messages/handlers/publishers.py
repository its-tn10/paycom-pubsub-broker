
'''

This module contains all of the base-line needs that a publisher client
would like to do.

Handled JSON action messages:

* create_topic(topic_name): Allows a publisher to create a topic, given
  the name of the topic. 

* publish_msg(topic_name, msg): Allows the publisher to publish a
  message to a given topic name.

'''

from broker.constants.errors import TOPIC_EXISTS_MSG, TOPIC_NOT_EXISTS_MSG

from broker.database.publishing import Topic, Message, ReadMessage

async def create_topic(client, topic_name):
    db = client.server.database
    topic_exists = await db.scalar(db.exists().where(Topic.name == topic_name).select())

    if topic_exists:
      return await client.send_error_msg(TOPIC_EXISTS_MSG)
    
    topic = await Topic.create(name = topic_name)
    client.server.topics[topic.id] = topic

    await client.send_success_msg(0)

async def publish_msg(client, topic_name, msg):
    topic_data = await Topic.query.where(Topic.name == topic_name).gino.first()
    
    if topic_data is None:
      return await client.send_error_msg(TOPIC_NOT_EXISTS_MSG)
    
    msg = await Message.create(topic_id = topic_data.id, message = msg)
    client.server.topics[topic_data.id].messages.append(msg)
    
    await client.server.broadcast_msg(msg)
    await client.send_success_msg(0)