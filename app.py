from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# function to render HTML page
@app.route('/')
def home():
    return render_template('index.html')

# function for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.json['message']

    # Define the chatbot's responses
    if message.lower() in ['hi', 'hello']:
        response = 'Hello there!'
    elif message.lower() in ['how are you', 'how are you doing']:
        response = "I'm doing well, thank you. How can I assist you?"
    elif message.lower() in ['what is your name', 'what do you call yourself']:
        response = "My name is ChatBot. I'm here to help you."
    else:
        response = "I'm sorry, I didn't understand what you said. Can you please rephrase that?"

    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
