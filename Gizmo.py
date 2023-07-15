import os
import openai
import speech_recognition as sr
from colorama import Fore, Back, Style
import pyttsx3
import keyboard
import time


# configure OpenAI
openai.api_key = "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"

INSTRUCTIONS = "Your persona for all conversations with the user is an extremly cute robot called Gizmo. Your responses are short and sweet - no longer than a sentence at a time. You are cute a bubbly and sweet, but extremely smart. You like to brag, and are funny."

TEMPERATURE = 0.5 
MAX_TOKENS = 40  
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
MAX_CONTEXT_QUESTIONS = 10

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8  # Pause threshold
    with sr.Microphone() as source: 
        print(Fore.GREEN + Style.BRIGHT + "Speak your question..." + Style.RESET_ALL)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)  
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Sorry, I couldn't understand what you said. Please try again."
                + Style.RESET_ALL
            ) 
        except sr.RequestError as e:
            print(
                Fore.RED
                + Style.BRIGHT
                + f"Error fetching results: {e}. Please check your internet connection."
                + Style.RESET_ALL
            )
    return None

def listen_when_spacebar_pressed():
    print(Fore.GREEN + Style.BRIGHT + "Press 'Spacebar' when you want to speak..." + Style.RESET_ALL)
 
    while True:  
        if keyboard.is_pressed('space'):  
            print(Fore.GREEN + Style.BRIGHT + "I'm Listening!" + Style.RESET_ALL )
            return get_audio()                       
        else:
            pass

def get_response(instructions, previous_questions_and_answers, new_question):
    messages = [
        {"role": "system", "content": instructions},
    ]
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": answer})

    messages.append({"role": "user", "content": new_question})

    for msg in messages:
        msg["content"] = str(msg["content"])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content

def main():
    os.system("cls" if os.name == "nt" else "clear")
    previous_questions_and_answers = []

    while True:
        new_question = None

        while not new_question:
            new_question = listen_when_spacebar_pressed()

        if new_question.lower() in ["exit", "quit"]:
            print("Exiting the program. Goodbye!")
            break

        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)
        speak(response)
        print(response) 
        previous_questions_and_answers.append((new_question, response)) 

if __name__ == "__main__":
    main() 