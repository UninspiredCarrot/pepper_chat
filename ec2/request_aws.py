import openai
import os

# Function to interact with the chatbot
def chat_with_bot(user_input, api_key):
    openai.api_key = os.environ['API_KEY']
    # Define a system message to set the bot's behavior
    system_message = "You are a helpful shopping assistant named Pepper."

    # Create a conversation with a user prompt
    conversation = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]

    # Send the conversation to the chatbot
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.4,
        max_tokens=300
    )

    # Extract and return the bot's response
    bot_response = response['choices'][0]['message']['content']
    print(bot_response)
    return bot_response
def req(user_input, api_key):
    print("User: " + user_input)
    return chat_with_bot("User: " + user_input, api_key)

def scribe(path, api_key):
    openai.api_key = api_key
    audio_file = open(path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt="ingredients,help, for, chicken, bread, milk", language="en", temperature=0.2)
    return transcript
