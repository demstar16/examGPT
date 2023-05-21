from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class customer_data(UserMixin, db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    conversations = db.relationship('conversation_data', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.customer_id

class conversation_data(db.Model):
    conversation_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_data.customer_id'))
    conversation_name = db.Column(db.String(128))

    def __repr__(self):
        return '<Conversation {}>'.format(self.conversation_name)
    
    def get_messages(self):
        return chat_message_data.query.filter_by(conversation_id=self.conversation_id).order_by(chat_message_data.message_number).all()
    
    def add_message(self, message, sender):
        number = len(self.get_messages())
        m = chat_message_data(conversation_id=self.conversation_id, message_number=number, sender=sender, message=message)
        db.session.add(m)
        db.session.commit()

class chat_message_data(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation_data.conversation_id'))
    message_number = db.Column(db.Integer)
    sender = db.Column(db.String(8)) #Either User, Chatbot or System
    message = db.Column(db.String(1024)) #Whats the max message length?

    def __repr__(self):
        return '<Message {}>'.format(self.message)
    
@login.user_loader
def load_user(id):
    return customer_data.query.get(int(id))