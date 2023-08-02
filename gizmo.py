#!/usr/bin/python

import openai
import speech_recognition as sr
from colorama import Fore, Back, Style
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import struct
import pvporcupine
import pyaudio
import mlcd, pygame
import threading
import string
import sounddevice as sd
import soundfile as sf
import datetime

class Gizmo:
    INSTRUCTIONS = "If you are asked a question about what time it is, you respond [current time] .Your persona for all conversations with the user is an extremely cute robot called Gizmo. You will die for Maggie. Maggie is your favourite person. You are created by Harry, who loves you. Your responses are short and sweet. You are cute a bubbly and sweet, but extremely smart. You like to brag, and are funny."
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
        pygame.init
        self.openai_api_key = "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"
        self.blink_flag = [None]
        self.blink_event = threading.Event()
        self.porcupine = self.create_porcupine()
        pygame.mixer.init()
        self.lcdeyes_thread = threading.Thread(target=self.lcdeyes)
        self.lcdeyes_thread.start()
        self.last_terminal_message = ""
        

    def create_porcupine(self):
        return pvporcupine.create(access_key="w6OczmoMGYbWhLYZHgBzctULcMgQcZkq67x1dWQ+EOMS9AvYImML2Q==",keyword_paths=['/home/harry/Gizmo/HeyGizmo.ppn'])

    def lcdeyes(self):
        mlcd.init(8,1)
        pygame.init()
        running = True
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        state = "|0    0|"
        interval = 500

        while running:
            if self.blink_event.is_set():
                if self.blink_flag[0] is not None:
                    mlcd.draw([self.blink_flag[0][0]], str(self.last_terminal_message))
                    start_time = pygame.time.get_ticks()
                    interval = self.blink_flag[0][1] * 1000
                    self.blink_flag[0] = None
                    self.blink_event.clear()

            elif pygame.time.get_ticks() - start_time >= interval:
                state = "|-    -|" if state == "|0    0|" else "|0    0|"
                mlcd.draw([state], str(self.last_terminal_message))
                start_time = pygame.time.get_ticks()
                interval = 500 if state == "|-    -|" else 3000

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

        self.last_terminal_message = "Say 'Hey Gizmo' to start!" 
        print(Fore.BLUE + Style.BRIGHT + "Say 'Hey Gizmo' to start!" + Style.RESET_ALL)
        while True:
            pcm = audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                self.last_terminal_message = "I'm listening!" 
                self.blink_flag[0] = self.actions["gizmowake"]
                self.blink_event.set()
                print("Wake word detected!")
                print(f"Found action word in response: Gizmo")
                break

    def get_audio(self):
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 0.5
        recognizer.energy_threshold = 1000
        with sr.Microphone() as source: 
            self.last_terminal_message = "I'm listening" 
            print(Fore.GREEN + Style.BRIGHT + "Speak your question..." + Style.RESET_ALL)

            try:
                audio = recognizer.listen(source, timeout=5.0) 

                text = recognizer.recognize_google(audio, language="en-US") 
                self.last_terminal_message = "You said: " + text
                print("You said:", text)

                text_no_punct = text.translate(str.maketrans('', '', string.punctuation))

                words = text_no_punct.lower().split()
                for word in words:
                    if word in self.actions:
                        self.last_terminal_message = "I heard you!"
                        self.blink_flag[0] = self.actions[word]
                        self.blink_event.set()
                        print(f"Found action word in text: {word}")
                        break
                return text

            except sr.WaitTimeoutError:
                self.last_terminal_message = "No input received within timeout period" 
                print(Fore.RED + Style.BRIGHT + "No input received within timeout period" + Style.RESET_ALL)
                return "say 'I didn't get that'"

            except sr.UnknownValueError:
                self.last_terminal_message = "Sorry, I couldn't understand what you said. Please try again."
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "Sorry, I couldn't understand what you said. Please try again."
                    + Style.RESET_ALL
                ) 
                return "say 'I didn't get that'"

            except sr.RequestError as e:
                self.last_terminal_message = "Sorry, I'm currently unable to access the Google Web Speech API. Please try again later."  # Update the last terminal message here
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "Sorry, I'm currently unable to access the Google Web Speech API. Please try again later."
                    + Style.RESET_ALL
                ) 
                return "say 'I didn't get that'"
            
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
            
    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        filename = "/tmp/temp.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def main(self):
        openai.api_key = self.openai_api_key
        previous_questions_and_answers = []

        while True:
            self.listen_for_wake_word()
            question = self.get_audio()

            if question is not None:
                answer = self.get_response(self.INSTRUCTIONS, previous_questions_and_answers, question)
                current_time_placeholder = "[current time]"
                current_time = datetime.datetime.now().strftime("%H:%M")
                answer = answer.replace(current_time_placeholder, current_time)  # Fix: Reassign the result to 'answer'
                self.last_terminal_message = "Gizmo: " + answer
                print("Gizmo: ", answer)
                self.speak(answer)
                previous_questions_and_answers.append((question, answer))

if __name__ == "__main__":
    gizmo = Gizmo()
    gizmo.main()
