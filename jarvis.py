import speech_recognition as sr
# import pyttsx3
# import pyaudio
import music_lib
import requests
from gtts import gTTS
import pygame
import time
import os



import webbrowser

r = sr.Recognizer()
# engine = pyttsx3.init()
newsapi = '2fb318336c8c47ce8d32d6ba188b7db7'

def aiProcess(command): 
    response = requests.post(
        "https://api.aimlapi.com/v1/chat/completions",
        headers={
            "Content-Type":"application/json", 

            # Insert your AIML API Key instead of <YOUR_AIMLAPI_KEY>:
            "Authorization":"Bearer 07308d90102d4dc3b398e3dfe4738f92",
            "Content-Type":"application/json"
        },
        json={
            "model":"cohere/command-r-plus",
            "messages":[
                {
                    "role":"user",

                    # Insert your question for the model here, instead of Hello:
                    "content": command
                }
            ]
        }
    )

    data = response.json()
    if 'choices' in data and len(data['choices']) > 0:
        generated = data['choices'][0]['message']['content']
        return generated
    else:
        return "No content found in the response"


# def speak_old(text):
#     engine.say(text)
#     engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    filename = "temp.mp3"
    tts.save(filename)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Wait until playback finishes
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"Audio playback error: {e}")

    finally:
        # Cleanup: stop music and delete temp file
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        if os.path.exists(filename):
            os.remove(filename)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open ai" in c.lower():
        webbrowser.open("https://www.chatgpt.com")
    elif "open allen" in c.lower():
        webbrowser.open("https://www.allen.in")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music_lib.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        data = r.json()

    # Get and print all titles
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            for i, article in enumerate(articles, 1):
                speak(f"{i}. {article.get('title', 'No Title')}")
    else:
        # let openai handle the request
        output = aiProcess(c)
        speak(output)
        print(f"Jarvis: {output.capitalize()}")


if __name__ == "__main__":
    speak("Initialising Jarvis....")
    # Listen for the wake word 'jarvis'
    while True:
        print("Recognizing...")
        # recognize speech 
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if (word.lower()=='jarvis'):
                speak("Ya!!")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=2)
                    command = r.recognize_google(audio)
                    print(f"YOU: {command.capitalize()}")
                    

                    processCommand(command)

        except Exception as e:
            print("Error {0}".format(e))
        
