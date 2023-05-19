from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, session
from .gpt_api import ExamGPT_conversation
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import models
from app.models import customer_data, conversation_data, chat_message_data
from app.forms import LoginForm, RegistrationForm

# function to render HTML page
@app.route('/')
@login_required
def home():
    flash("Welcome home")
    return render_template('history2.html')

@app.route('/index/<conversation_id>')
@login_required
def chat(conversation_id):
    conversation = conversation_data.query.filter_by(conversation_id=conversation_id).first_or_404()
    messages = conversation.get_messages()
    return render_template('index.html', messages=messages)

# function to render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('history'))
    form = LoginForm()
    if form.validate_on_submit():
        user = customer_data.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('history')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# function to render register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = customer_data(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# function to render history page
@app.route('/history')
@login_required
def history():
    return render_template('history2.html', email=current_user.email, conversations=current_user.get_conversations())
    #return render_template('history.html', email=current_user.email)

#logout current user
@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))

# Initialize the conversation
system_prompt = {
    "role": "system",
    "content": "Your name is ExamGPT. You are a chat bot that generates exam questions and helps students with their exam problems. If a student gives you a topic, you reply with exam questions. If they ask you a question, you will help them solve their exam question."
}


# function for the chatbot
@app.route('/chatbot/<conversation_id>', methods=['POST'])
def chatbot(conversation_id):
    message = request.json['message']
    print("User:", message)

    # Get conversation and add users message to database
    conversation = conversation_data.query.filter_by(conversation_id=conversation_id).first_or_404()
    conversation.add_message(message=message, sender="user")

    # Get a list of all the messages in the conversation
    prompts = []
    prompts.append(system_prompt)
    for messages in conversation.get_messages():
        # May want to change all code where "chatbot" is written to "assistant"
        prompt = {"role": messages.sender if messages.sender != "chatbot" else "assistant", "content": messages.message}
        prompts.append(prompt)

    # Get the ExamGPT response
    response = ExamGPT_conversation(prompts)
    
    # Extract the response
    response = response[-1]['content'].strip()
    print("ExamGPT:", response)
    # Add response to database
    conversation.add_message(message=response, sender="chatbot")

    return jsonify({'message': response})



if __name__ == '__main__':
    app.run(debug=True)

