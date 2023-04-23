import openai

API_KEY = "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"
openai.api_key = API_KEY

model_id="gpt-3.5-turbo"

def ExamGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        temperature = 0.2,
        max_tokens = 1024,
        model = model_id,
        messages = conversation
    )
    # api_usage = response["usage"]
    # print("Total token consumed: {0}".format(api_usage["total_tokens"]))
    # Stop means complete
    # print(response["choices"][0].finish_reason)
    # print(response["choices"][0].index)
    conversation.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})
    return conversation

conversation = []
conversation.append({"role": "system", "content": "Your name is ExamGPT. You are a chat bot that generates exam questions and helps students with their exam problems. If a student gives you a topic, you reply with exam questions. If they ask you a question, you will help them solve their exam question."})
conversation = ExamGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))


while True:
    prompt = input("User:")
    conversation.append({"role": "user", "content": prompt})
    conversation = ExamGPT_conversation(conversation)
    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
