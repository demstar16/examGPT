import pytest
from . import app

def get_app_instance():
    app_instance = app.test_client()
    return app_instance

# Each page that I want to make sure can be rendered
@pytest.mark.parametrize(("input", "expected"), [
    ("/register" , 200),   
    ("/login" , 200),
])
def test_page_rendering(input, expected):
    # Create instance of the application
    client = get_app_instance()
    # Get the response (success or failure) of rendering each page
    response = client.get(input)
    assert response.status_code == expected