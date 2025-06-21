import requests
import json

# Define Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Your model name (ensure DeepSeek-R1 is installed in Ollama)
MODEL_NAME = "deepseek-r1:8b"

# Define the input messages
messages = [
    {"role": "system", "content": "You are an AI assistant."},
    {"role": "user", "content": "Hello, how are you?"}
]

# Convert messages into Ollama-compatible prompt
prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages])

# Define the payload for Ollama
payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False  # Set to True if you want streaming responses
}

# Make the request to Ollama
response = requests.post(OLLAMA_URL, json=payload)

# Parse and display the response
if response.status_code == 200:
    result = response.json()
    print("AI Response:", result.get("response", "No response received."))
else:
    print("Error:", response.text)
