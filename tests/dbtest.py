import unittest, os

from app import app, db
from app.models import customer_data, conversation_data, chat_message_data

class CustomerDataCase(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        customer = customer_data(customer_id=0, email='t1@gmail.com')
        db.session.add(customer)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password(self):
        customer = customer_data.query.get(0)
        customer.set_password('password')
        self.assertTrue(customer.check_password('password'))
        self.assertFalse(customer.check_password('pass'))
        self.assertFalse(customer.check_password('other'))
    
    def test_data_comitting(self):
        customer = customer_data.query.first()
        conversation = conversation_data(conversation_id=0, customer_id=customer.customer_id)
        db.session.add(conversation)
        db.session.flush()
        message1 = chat_message_data(message_id=0, conversation_id=conversation.conversation_id)
        message2 = chat_message_data(message_id=1, conversation_id=conversation.conversation_id)
        db.session.add(message1)
        db.session.add(message2)
        db.session.commit()
        self.assertTrue(customer.conversations.count() == 1)
        self.assertTrue(len(customer.conversations.first().get_messages()) == 2)
    
    def test_adding_messages(self):
        customer = customer_data.query.first()
        conversation = conversation_data(conversation_id=0, customer_id=customer.customer_id)
        messages = conversation.get_messages()
        self.assertTrue(len(messages) == 0)
        db.session.add(conversation)
        db.session.flush()
        conversation.add_message("message1", "user")
        conversation.add_message("message2", "chatbot")

        messages = conversation.get_messages()
        self.assertTrue(len(messages) == 2)
        message1 = messages[0]
        message2 = messages[1]
        self.assertTrue(message1.message == "message1")
        self.assertTrue(message1.sender == "user")
        self.assertTrue(message1.message_number == 0)
        self.assertTrue(message2.message_number == 1)



if __name__ == '__main__':
    unittest.main(verbosity=2)