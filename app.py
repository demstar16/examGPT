from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key as an environment variable
API_KEY = "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"
openai.api_key = API_KEY
model_id = "gpt-3.5-turbo"

# function to render HTML page
@app.route('/')
def home():
    return render_template('index.html')

# function for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.json['message']
    print("Received message:", message)

    # Define the chatbot's response
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[{"role":"user",
                   "content": message}]
    )
 
    # Extract the response text from the API response
    response_text = response["choices"][0]["message"]["content"]

    print(response_text)

    # Return the response to the user
    return jsonify({"message": response_text, "role": "assistant"})


if __name__ == '__main__':
    app.run(debug=True)

