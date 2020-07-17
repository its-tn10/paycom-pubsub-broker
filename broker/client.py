from broker.clientconnection import ClientConnection
from broker.database.publishing import Message, ReadMessage
from broker.database.subscribing import Subscription

class Client(ClientConnection):

    def __init__(self, *args):
        super().__init__(*args)
    
        self.authenticated = False
        self.data = None

        self.subscriptions = []
    
    async def subscriber_init(self):
        if self.data is None or not self.data.subscriber:
            return
        
        await self.load_subscriptions()
        await self.send_unread_msgs()
    
    async def load_subscriptions(self):
        query = Subscription.query.where(Subscription.client_id == self.data.id).gino
        async with self.server.database.transaction():
            async for sub in query.iterate():
                curr_topic = self.server.topics[sub.topic_id]
                self.subscriptions.append(curr_topic)

    async def send_unread_msgs(self):
        db = self.server.database
        for topic in self.subscriptions:
            for message in topic.messages:
                read_message = await db.scalar(db.exists().where(ReadMessage.message_id == message.id).select())

                if not read_message:
                    await ReadMessage.create(client_id = self.data.id, message_id = message.id)
                    await self.send_json(action = 'unread', message = message.message)    