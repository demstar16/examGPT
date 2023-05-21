# cits3403-project

## How to setup:
1. Make sure python and pip are installed

2. Create your own python virtual environment by typing the following:  
Linux/MacOS
```bash
python3 -m venv venv
```
Windows
```bash
python3 -m venv env
```

3. Connect to the virtual environment:  
Linux/MacOS
```bash
source /venv/bin/activate (The path to your activate file)
```
Windows (CMD)
```bash
env\Scripts\activate
```

4. Check if you have connected correctly:  
Linux/MacOS
```bash
which python3
/home/adam/OneDrive/SEM12023/CITS3404 Agile Web Development/cits3403-project/venv/bin/python3
```

Windows (CMD)
```bash
where python
```
This should display the path to the project if connected correctly.

4. Install dependencies.  
(If new dependencies are added to the project, add them to the requirements.txt file):
```bash
pip install -r requirements.txt
```

5. Run the flask app:
```bash
flask run
```
6. When you are done in the python virtual environment. Type:
```bash
deactivate
```
This will change your python environment back to the default location.

## TO DO:
- [x] Create development environment
- [x] Create a Flask app that will serve as the backend of the chat application.
- [x] Design the user interface of the chat application using HTML and CSS. The UI should have a chatbox, a message input field, and a send button.
- [x] Use JQuery to handle user interactions on the front-end.
- [x] Set up routes in Flask to handle different HTTP requests. 
- [x] Set Up Log In / Account features
- [x] Proper design or the web page (make it look nice)
- [x] Create / Find a proper chatbot for questions
- [x] Create a database schema to store chat messages, user information, and exam questions.
- [ ] Add an admin page to manage accounts (only we know the admin login details)
- [x] Implement authentication to ensure that only registered users can access the chat application.
- [ ] Deploy the application on a server.
- [x] Create Unit Tests
- [x] Add an alert for the logout button (a way so if u accidently click it you're not just logged out)
- [ ] Add constraints to make the bot more specific, so its not just chatGPT (if that makes sense)
- [ ] Forgot password functionality
- [ ] Delete any Redundant files


