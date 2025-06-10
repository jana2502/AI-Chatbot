from ollama import Client

def generate_ai_response(messages_history, user_message):
    client = Client()  # Local Ollama client
    # Example: using 'llama3' model (you can use 'mistral', 'gemma', etc.)
    response = client.chat(
        model='llama3', 
        messages=[{"role": "user", "content": user_message}]
    )
    return response['message']['content']
