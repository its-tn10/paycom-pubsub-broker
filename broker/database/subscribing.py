from broker.database import db

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    client_id = db.Column(db.ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    topic_id = db.Column(db.ForeignKey('topics.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)

