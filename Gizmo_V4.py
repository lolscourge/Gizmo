import os
import openai
import speech_recognition as sr
from colorama import Fore, Back, Style
import pyttsx3
import time
import struct
import pvporcupine
import pyaudio
import whisper 
import mlcd, pygame
import threading
import string

class Gizmo:
    INSTRUCTIONS = "Your persona for all conversations with the user is an extremely cute robot called Gizmo. You will die for Maggie. Maggie is your favourite person. You are created by Harry, who loves you. Your responses are short and sweet. You are cute a bubbly and sweet, but extremely smart. You like to brag, and are funny."
    TEMPERATURE = 0.5 
    MAX_TOKENS = 100  
    FREQUENCY_PENALTY = 0
    PRESENCE_PENALTY = 0.6
    MAX_CONTEXT_QUESTIONS = 10

    actions = {
        "test": ["<3    <3", 4],
        "gizmowake": ["!!    !!", 4],
        "i care about you": ["<3    <3", 4],
        "maggie": ["<3    <3", 4],
        "harry": ["<3    <3", 4],
        "happy": [":)    :)", 4],
        "smile": [":)    :)", 4],
        "sad": [":(    :(", 4]
    }

    def __init__(self):
        self.model = whisper.load_model("base")
        self.openai_api_key = "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"
        self.blink_flag = [None]
        self.blink_event = threading.Event()
        self.engine = pyttsx3.init()
        self.porcupine = self.create_porcupine()
        self.voice = self.engine.getProperty('voices')[0].id
        self.engine.setProperty('voice', self.voice)
        self.engine.setProperty('pitch', 1)
        self.lcdeyes_thread = threading.Thread(target=self.lcdeyes)
        self.lcdeyes_thread.start()

    def create_porcupine(self):
        return pvporcupine.create(access_key="w6OczmoMGYbWhLYZHgBzctULcMgQcZkq67x1dWQ+EOMS9AvYImML2Q==",keywords=["bumblebee"])

    def get_response(self, instructions, previous_questions_and_answers, new_question):
        messages = [
            {"role": "system", "content": instructions},
        ]
        for question, answer in previous_questions_and_answers[-self.MAX_CONTEXT_QUESTIONS:]:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer})

        messages.append({"role": "user", "content": new_question})

        for msg in messages:
            msg["content"] = str(msg["content"])

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS,
            frequency_penalty=self.FREQUENCY_PENALTY,
            presence_penalty=self.PRESENCE_PENALTY,
        )
        return completion.choices[0].message.content

    def lcdeyes(self):
        mlcd.init(8,1)
        pygame.init()
        running = True
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        state = "|0    0|"
        interval = 4000

        while running:
            if self.blink_event.is_set():
                if self.blink_flag[0] is not None:
                    mlcd.draw([self.blink_flag[0][0]])
                    start_time = pygame.time.get_ticks()
                    interval = self.blink_flag[0][1] * 1000
                    self.blink_flag[0] = None
                    self.blink_event.clear()

            elif pygame.time.get_ticks() - start_time >= interval:
                state = "|-    -|" if state == "|0    0|" else "|0    0|"
                mlcd.draw([state])
                start_time = pygame.time.get_ticks()
                interval = 500 if state == "|-    -|" else 4000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

    def listen_for_wake_word(self):
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

        print(Fore.BLUE + Style.BRIGHT + "Say 'Gizmo' to start!" + Style.RESET_ALL)
        while True:
            pcm = audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                print(f"Found action word in response: Gizmo")  # Added this line
                self.blink_flag[0] = self.actions["gizmowake"]
                self.blink_event.set()
                break

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_audio(self):
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 0.5
        with sr.Microphone() as source: 
            print(Fore.GREEN + Style.BRIGHT + "Speak your question..." + Style.RESET_ALL)
            try:
                audio = recognizer.listen(source, timeout=3.0)  # 3 second timeout

                text = recognizer.recognize_whisper(audio, language="english")    
                print("You said:", text)

                text_no_punct = text.translate(str.maketrans('', '', string.punctuation))

                words = text_no_punct.lower().split()
                for word in words:
                    if word in self.actions:
                        print(f"Found action word in text: {word}")  # Added this line
                        self.blink_flag[0] = self.actions[word]
                        self.blink_event.set()
                        break
                return text

            except sr.WaitTimeoutError:
                print(Fore.RED + Style.BRIGHT + "No input received within timeout period" + Style.RESET_ALL)
                return None

            except sr.UnknownValueError:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "Sorry, I couldn't understand what you said. Please try again."
                    + Style.RESET_ALL
                ) 
                return None

            except sr.RequestError as e:
                print(
                        Fore.RED
                        + Style.BRIGHT
                        + "Sorry, I'm currently unable to request results from Whisper Speech-to-Text service."
                        + Style.RESET_ALL
                    )
                return None

    def main(self):
        openai.api_key = self.openai_api_key

        previous_questions_and_answers = []
        expecting_response = False

        def stop_expecting_response():
            nonlocal expecting_response
            expecting_response = False

        timer = threading.Timer(3, stop_expecting_response)  # 3 second timer

        while True:
            if not expecting_response:
                self.listen_for_wake_word()
            
            text = self.get_audio()
            if text is not None:
                response = self.get_response(self.INSTRUCTIONS, previous_questions_and_answers, text)
                previous_questions_and_answers.append((text, response))

                print(f"Gizmo said: {response}")  # Prints what Gizmo says.

                response_no_punct = response.translate(str.maketrans('', '', string.punctuation))

                words = response_no_punct.lower().split()
                for word in words:
                    if word in self.actions:
                        print(f"Found action word in response: {word}")  # Added this line
                        self.blink_flag[0] = self.actions[word]
                        self.blink_event.set()
                        break

                self.speak(response)

                timer.cancel()  # cancel the previous timer
                timer = threading.Timer(3, stop_expecting_response)  # create a new timer
                timer.start()  # start the new timer

                expecting_response = True
            else:
                timer.cancel()  # cancel the timer if not expecting response
                expecting_response = False  # Reset to not expecting response

if __name__ == "__main__":
    gizmo = Gizmo()
    gizmo.main()