import unittest, os, time
from app import app, db
from app.models import customer_data, conversation_data, chat_message_data
from selenium import webdriver
from selenium.webdriver.common.by import By

# TestingConfig must be set in __init__.py before running test ----------------------------------------------
# Or else the main db will be used/deleted

class CustomerDataCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir,'chromedriver.exe'))
        if not self.driver:
            self.skipTest("Driver not avaiable")
        else:
            self.app_context = app.app_context()
            self.app_context.push()
            db.create_all()
            customer = customer_data(email="email@gmail.com")
            customer.set_password('password')
            db.session.add(customer)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_registration(self):
        self.driver.get('http://localhost:5000/register')
        self.driver.implicitly_wait(2)
        email_field = self.driver.find_element(By.ID, 'email')
        email_field.send_keys('t1@gmail.com')
        password_field = self.driver.find_element(By.ID, 'password')
        password_field.send_keys('password')
        password2_field = self.driver.find_element(By.ID, 'password2')
        password2_field.send_keys('password')
        self.driver.implicitly_wait(2)
        submit = self.driver.find_element(By.CLASS_NAME, 'login-buttons')
        submit.click()
        self.driver.implicitly_wait(5)
        logout = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Logout')
        self.assertEqual(logout.get_attribute('innerHTML'), 'Logout')
    
    def test_conversation_history(self):
        # Login
        self.driver.get('http://localhost:5000/login')
        self.driver.implicitly_wait(2)
        email_field = self.driver.find_element(By.ID, 'email')
        email_field.send_keys('email@gmail.com')
        password_field = self.driver.find_element(By.ID, 'password')
        password_field.send_keys('password')
        self.driver.implicitly_wait(2)
        submit = self.driver.find_element(By.CLASS_NAME, 'login-buttons')
        submit.click()
        self.driver.implicitly_wait(5)

        # New Conversation
        newC = self.driver.find_element(By.CLASS_NAME, 'new-conversation-button')
        newC.click()
        self.driver.implicitly_wait(2)
        div = self.driver.find_element(By.CLASS_NAME, 'history-conversation')
        name = div.find_element(By.CSS_SELECTOR, 'p')
        self.assertEqual(name.get_attribute('innerHTML'), 'New Conversation')

        # Rename Conversation
        rename = self.driver.find_element(By.CLASS_NAME, 'history-rename-button')
        rename.click()
        self.driver.implicitly_wait(5)
        alert = self.driver.switch_to.alert
        alert.send_keys("Test Conversation")
        alert.accept()
        time.sleep(1)
        self.driver.implicitly_wait(5)
        div = self.driver.find_element(By.CLASS_NAME, 'history-conversation')
        name = div.find_element(By.CSS_SELECTOR, 'p')
        self.assertEqual(name.get_attribute('innerHTML'), 'Test Conversation')
        self.driver.implicitly_wait(5)

        # Delete Conversation
        delete = self.driver.find_element(By.CLASS_NAME, 'history-delete-button')
        delete.click()
        self.driver.implicitly_wait(5)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        self.driver.implicitly_wait(5)
        customer = customer_data.query.first()
        self.assertTrue(customer.conversations.count() == 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)