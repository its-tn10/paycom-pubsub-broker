from broker.database import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    publisher = db.Column(db.Boolean, nullable=False)
    subscriber = db.Column(db.Boolean, nullable=False)
