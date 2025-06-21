import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
from datetime import datetime

# Ollama API details
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"


def say(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    female_voice = None
    for voice in voices:
        if "Zira" in voice.name:
            female_voice = voice
            break

    if female_voice:
        engine.setProperty('voice', female_voice.id)
    else:
        print("Female voice not found, using default voice.")

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """Listen to the user's voice and return recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: '{query}'")
            return query.lower()
        except Exception as e:
            print("Error during recognition:", e)
            return "Some error occurred."


def tell_time():
    """Tell the current time."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    say(f"The time is {current_time}, Sir.")
    print(f"The time is {current_time}.")


def query_deepseek(user_input):
    """Query DeepSeek-R1 using Ollama and return the AI's response directly."""

    # Speak "Let me think, Rushi Sir..." before AI responds
    say("Let me think, Rushi Sir...")

    payload = {
        "model": MODEL_NAME,
        "prompt": f"Answer directly without explanation: {user_input}",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response received.")
    else:
        return f"Error: {response.text}"


if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am Rishi's assistant. You can call me Sanjana!")

    # List of websites
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.com",
        "google": "https://www.google.com"
    }

    # Music directory path
    musicPath = r"music\music.mp3"

    while True:
        query = takeCommand()
        if query == "Some error occurred.":
            continue

        # Open websites
        for site in sites:
            if f"open {site}" in query:
                say(f"Opening {site}, Sir...")
                webbrowser.open(sites[site])
                break
        else:
            if "what's the time" in query or "what time is it" in query:
                tell_time()

            elif "open music" in query:
                if os.path.exists(musicPath):
                    say("Opening your music, Sir...")
                    os.startfile(musicPath)
                else:
                    say("I couldn't find the music file, Sir. Please check the path.")

            else:
                # **Now AI will say "Let me think, Rushi Sir..." before answering**
                ai_response = query_deepseek(query)
                say(ai_response)
                print("AI Response:", ai_response)
