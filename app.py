from flask import Flask, request, jsonify, render_template
from gpt_api import ExamGPT_conversation
#from flask_login import LoginManager, current_user, login_user
#from app.models import User

app = Flask(__name__)

#login = LoginManager(app)

# function to render HTML page
@app.route('/')
def home():
    return render_template('index.html')

# function to render login page
@app.route('/login')
def login():
    return render_template('login.html')

# function to render chatlog history
@app.route('/history')
def history():
    return render_template('history.html')

# Initialize the conversation
global_conversation = [
    {
        "role": "system",
        "content": "Your name is ExamGPT. You are a chat bot that generates exam questions and helps students with their exam problems. If a student gives you a topic, you reply with exam questions. If they ask you a question, you will help them solve their exam question."
    }
]

# function for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    global global_conversation
    message = request.json['message']
    print("User:", message)

    # Add user message to conversation
    global_conversation.append({"role": "user", "content": message})

    # Get the ExamGPT response
    global_conversation = ExamGPT_conversation(global_conversation)
    

    # Extract the response
    response = global_conversation[-1]['content'].strip()
    print("ExamGPT:", response)

    return jsonify({'message': response})


# copied from the lab
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
"""


if __name__ == '__main__':
    app.run(debug=True)

