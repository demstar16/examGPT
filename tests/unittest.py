import unittest, os
from app import app, db
from app.models import customer_data, conversation_data, chat_message_data

class CustomerDataCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        c1 = customer_data(customer_id='00000000', email="t1@gmail.com")
        c2 = customer_data(customer_id='11111111', email="t2@gmail.com")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password(self):
        customer = customer_data.query.get('00000000')
        customer.set_password('password')
        self.assertTrue(customer.check_password('password'))
        self.assertFalse(customer.check_password('pass'))
        self.assertFalse(customer.check_password('other'))


if __name__ == '__main__':
    unittest.main()