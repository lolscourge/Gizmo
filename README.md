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

## Install Requirements

Install the requirements.txt file in your environement.

## Get API keys

You'll need to generate API keys for OpenAI and Porcupine Wake Word. To do this, make an account with them and follow their instructions, then update them in the Gizmo.py file.

## Porcupine Wake Word

The included .ppn file is the default Wake Word for Gizmo. It is the Linux version. You can generate any Wake Word with a Porcupine account for whatever specific operating system you are on.

## Instructions

You can ammend how Gizmo behaves by changing the instructions. If you want him to be able to tell the time, I'd leave the first instrcution "if you are asked a question about the time, respond with [current time] - it's clunky but it works.

