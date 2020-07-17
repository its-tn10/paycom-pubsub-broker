
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

from broker.constants.errors import ALREADY_SUBSCRIBED_MSG, CANT_SUBSCRIBE_MSG, \
                                    NOT_SUBSCRIBED_MSG

from broker.database.publishing import Topic, ReadMessage
from broker.database.subscribing import Subscription

async def read_all_topic_msgs(client, topic_id):
    if topic_id in client.server.topics:
        messages = client.server.topics[topic_id].messages
        for message in messages:
            await ReadMessage.create(client_id = client.data.id, message_id = message.id)

async def list_topics(client):
    topic_names = [topic.name for topic in client.server.topics.values()]
    await client.send_json(action = 'list_topics', topics = topic_names)

async def subscribe(client, topic_name):
    topic_data = await Topic.query.where(Topic.name == topic_name).gino.first()
    
    if topic_data is None:
        return await client.send_error_msg(CANT_SUBSCRIBE_MSG)

    has_subscribed = any([topic.name == topic_name for topic in client.subscriptions])
    if has_subscribed:
        return await client.send_error_msg(ALREADY_SUBSCRIBED_MSG)
    
    await Subscription.create(client_id = client.data.id, topic_id = topic_data.id)
    
    topic_cached = client.server.topics[topic_data.id]
    client.subscriptions.append(topic_cached)

    await read_all_topic_msgs(client, topic_data.id)
    await client.send_success_msg(0)

async def unsubscribe(client, topic_name):
    has_subscribed = any([topic.name == topic_name for topic in client.subscriptions])
    if not has_subscribed:
        return await client.send_error_msg(NOT_SUBSCRIBED_MSG)

    topic_data = await Topic.query.where(Topic.name == topic_name).gino.first()
    await Subscription.delete.where((Subscription.client_id == client.data.id) &
                                    (Subscription.topic_id == topic_data.id)).gino.status()
    
    for message in client.server.topics[topic_data.id].messages:
        await ReadMessage.delete.where((ReadMessage.client_id == client.data.id) &
                                    (ReadMessage.message_id == message.id)).gino.status()
                
    await client.send_success_msg(0)