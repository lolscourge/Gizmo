# Gizmo

A project for Maggie

Gizmo is a small GUI chatbot that:

- Can be activated using a wake word using the porcupine wake word API
- Listens for speech input
- Has a display that reacts based on the input
- Converts the speech input into text
- Fetches a response from the OpenAI conversional API
- Converts the response back to speech using Google Speech-to-Text
- Print outs and speaks the response in the display

It's my first python project and frankly, it was a reach. The code is probably all over the place and can 100% be improved upon, but it works!

## Prerequisites

Before installing the Python dependencies, make sure to install the necessary system-level packages:

```bash
sudo apt-get install -y portaudio19-dev
```

## Install Requirements

Install the requirements.txt file in your environement.

```bash
pip install -r requirements.txt
```

## Get API keys

You'll need to generate API keys for OpenAI and Porcupine Wake Word. To do this, make an account with them and follow their instructions, then update them in the config/__init__.py file.

```bash
CONFIG = {
    "openai_api_key": "xxx",
    "porcupine_access_key": "xxx",
}
```

## Porcupine Wake Word

The included .ppn file is the default Wake Word for Gizmo. It is the Linux version. You can generate any Wake Word with a Porcupine account for whatever specific operating system you are on.

There are also default Wake Words you can use - refer to [Porcupine documentation](https://github.com/Picovoice/porcupine) for more details

```bash
CONFIG = {
    "porcupine_keyword_path": "path/to/HeyGizmo_VER.ppn"
}
```

## Text to Speech

The text to speech requires a location to create an .mp3 file that is written to and sent off to Google. 

```bash
CONFIG = {
    "temp_audio_file_location": "path/to/temp/temp.mp3",
}
```

## Instructions

Instructions can be amended to change Gizmo's behaviour.

```bash
class Gizmo:

    INSTRUCTIONS = "Your persona for all conversations with the user is an extremely cute robot called Gizmo. Your responses are short and sweet. You are cute a bubbly and sweet, but extremely smart. You like to brag, and are funny."
    TEMPERATURE = 0.5 
    MAX_TOKENS = 400 
    FREQUENCY_PENALTY = 0
    PRESENCE_PENALTY = 0.6
    MAX_CONTEXT_QUESTIONS = 10
```
