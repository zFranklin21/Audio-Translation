# Imports
import wave
import os
import sys
import subprocess
import time
from time import sleep

# Package imports
try:
    import pyaudio
    import speech_recognition as sr
    from googletrans import Translator
except ImportError:
    print("Error: PyAudio and SpeechRecognition packages are needed.\
    \nPlease run $ pip install pyaudio speechrecognition googletrans");
    sys.exit();

def userInput(recordChoice):
    global rawFile
    if recordChoice == "y" or recordChoice == "yes":
        fileName = input("What is the name of the file you would like translated? ")
        rawFile = sr.AudioFile(fileName)
    else:
        import recorder
        print("\nPrepare to record a 10 second audio clip.")
        time.sleep(2)
        print("Starting in...")
        for i in range(5, 0, -1):
            print(i)
            time.sleep(1)
        recorder.record()
        rawFile = sr.AudioFile(recorder.WAVE_OUTPUT_FILENAME)
    return rawFile

def readFile(rawFile, r):
    print("\nReading audio file...")
    with rawFile as source:
        audio = r.record(rawFile)
    print("Audio file read.")
    return audio


def processAudio(audio, r):
    try:
        print("\nProcessing audio...")
        processed = r.recognize_google(audio)
        # r.recognize_google(audio, language="fr-FR")
        # https://cloud.google.com/speech-to-text/docs/languages
        print("Audio processed.")
        print("\nTranscription of audio:\n")
        print(processed)
    except sr.UnknownValueError:
        print("Sorry, audio was unable to be processed. Check for excessive background noise.")

def main():
    # Instantiation of modules
    r = sr.Recognizer()
    tl = Translator()

    recordChoice = input("\nDo you have a file you would like translated? ").lower()
    rawFile = userInput(recordChoice)
    audio = readFile(rawFile, r)
    processAudio(audio, r)

    print("\nTerminating program.")
    sys.exit()

main()
