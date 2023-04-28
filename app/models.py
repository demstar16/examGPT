from app import db

class customer_data(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class conversation_data(db.Model):
    conversation_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_data.customer_id'))
    conversation_name = db.Column(db.String(128))

    def __repr__(self):
        return '<Conversation {}>'.format(self.conversation_name)

class chat_message_data(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation_data.conversation_id'))
    message_number = db.Column(db.Integer)
    sender = db.Column(db.String(8)) #Either User or Chat
    message = db.Column(db.String(1024)) #Whats the max message length?

    def __repr__(self):
        return '<Message {}>'.format(self.message)