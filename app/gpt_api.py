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
    conversation.append({"role": response.choices[0].message.role, "content": response.choices[0].message.content})
    return conversation