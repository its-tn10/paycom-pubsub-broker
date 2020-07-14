from broker.database import db

class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.ForeignKey('topics.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    message = db.Column(db.String, nullable=False)

class ReadMessage(db.Model):
    __tablename__ = 'read_messages'

    client_id = db.Column(db.ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)
    message_id = db.Column(db.ForeignKey('messages.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, primary_key=True)

