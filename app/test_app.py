import pytest
from . import app
from flask_login import LoginManager, login_user
from app.models import customer_data

#---------------------------- FIXTURES -----------------------------------------
@pytest.fixture
def unauthorised_client():
    with app.test_client() as unauthorised_client:
        with app.app_context():
            yield unauthorised_client
            
@pytest.fixture
def authorised_client():
    with app.test_client() as authorised_client:
        with app.app_context():
            # Create a test user and log them in
            user = customer_data(email='randomperson@gmail.com')
            password = 'validpassword'
            user.set_password(password)
            
            with app.test_request_context():
                # Log in the user within the request context
                login_user(user)

            yield authorised_client
            
#---------------------------- UNIT TESTS -----------------------------------------
def test_new_user():
    """
    GIVEN a customer_data model
    WHEN a new user is created
    THEN check the email and password_hash fields are correct
    """
    user = customer_data(email='randomperson@gmail.com')
    password = 'validpassword'
    user.set_password(password)
    assert user.email == 'randomperson@gmail.com'
    assert user.password_hash != 'validpassword'

def test_home_route(authorised_client):
    """
    GIVEN an authorised client
    WHEN they want to access the home page
    THEN check to make sure they can access it
    """
    response = authorised_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome home' in response.data

def test_login_route(authorised_client):  
    """
    GIVEN an authorised client
    WHEN they want to login
    THEN check to make sure they're redirected correctly
    
    COULD USE SOME MORE ASSERTS AS IT DOESN'T CONFIRM A ROUTE IT JUST 
    CONFIRMS IT ENDS UP AT A VALID PLACE
    """     
    response = authorised_client.post('/login', data={'email': 'randomperson@gmail.com', 'password': 'validpassword'}, follow_redirects=True)
    assert response.status_code == 200


#---------------------------- FUNCTIONAL TESTS -----------------------------------------
@pytest.mark.parametrize(("input", "expected"), [
    ("/register", 200),
    ("/login", 200),
])
def test_unauthorised_pages(unauthorised_client, input, expected):
    """
    GIVEN a page 
    WHEN a client tries to render it
    THEN check to see if the page is able to load
    """
    response = unauthorised_client.get(input)
    assert response.status_code == expected
    
@pytest.mark.parametrize(("input", "expected"), [
    ("/", 200),
    ("/history", 200),
])
def test_authenticated_page(authorised_client, input, expected):
    """
    GIVEN a page that requires an account to see
    WHEN a client tries to access it
    THEN check to see if the page is able to load
    """
    # Make the request and follow the redirect
    response = authorised_client.get(input, follow_redirects=True)

    # Assert the final response
    assert response.status_code == expected

def test_invalid_login(unauthorised_client):
    """
    GIVEN invalid credentials
    WHEN a user tries to login
    THEN check to see if it doesn't let them in
    """
    

def test_logout(authorised_client):
    """
    WHEN a user tries to logout
    THEN check to see it does so correctly
    """
    response = authorised_client.get('/logout', follow_redirects=True)
    assert b'You have been logged out' in response.data
    assert response.status_code == 200


def test_registration(unauthorised_client):
    """
    WHEN a user tries to register
    THEN check to see it successfully registers them
    """

        