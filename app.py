from flask import Flask, request, jsonify, render_template
from gpt_api import ExamGPT_conversation

app = Flask(__name__)

# function to render HTML page
@app.route('/')
def home():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)

