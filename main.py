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
    import pyttsx3
    from googletrans import Translator
except ImportError:
    print("Error: PyAudio and SpeechRecognition packages are needed.\
    \nPlease run $ pip install pyaudio speechrecognition googletrans pyttsx3");
    sys.exit();

def userInput(recordChoice):
    global rawFile
    if recordChoice == "y" or recordChoice == "yes":
        fileName = input("What is the name of the file you would like translated? ")
        rawFile = sr.AudioFile(fileName)
    else:
        import recorder
        duration = input("How many seconds will you take to record your audio clip? ")
        recorder.RECORD_SECONDS = int(duration)
        print("\nPrepare to record a " + duration + " second audio clip.")
        time.sleep(2)
        print("\nStarting in...")
        for i in range(5, 0, -1):
            print("\t" + str(i))
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


def processAudio(audio, r, ss, lang):
    try:
        print("\nProcessing audio...")
        processed = r.recognize_google(audio, language = lang[0])
        # profanity is automatically filtered
        # r.recognize_google(audio, language="fr-FR")
        # https://cloud.google.com/speech-to-text/docs/languages
        print("Audio processed.")
        print("\nTranscription of audio:\n")
        print(processed)
        ss.say(processed)
        ss.runAndWait()
    except sr.UnknownValueError:
        print("Sorry, audio was unable to be processed. Verify language \
        selections and check for excessive background noise.")

def getLang(prompt):
    lang = None
    print("This program supports the following languages:\
    \n\t1. English\
    \n\t2. Spanish\
    \n\t3. German\
    \n\t4. French\
    \n\t5. Mandarin Chinese\
    \n\t6. Japanese\
    \n\t7. Russian")

    while lang == None:
        choice = input(prompt).lower()
        if choice == "english" or choice == "1":
            lang = ["en-US", "en_US"]
        elif choice == "spanish" or choice == "2":
            lang = ["es-ES", "es_ES"]
        elif choice == "german" or choice == "3":
            lang = ["de-DE", "de_DE"]
        elif choice == "french" or choice == "4":
            lang = ["fr-FR", "fr_FR"]
        elif choice == "mandarin chinese" or choice == "5":
            lang = ["zh-CN", "zh_CN"]
        elif choice == "japanese" or choice == "6":
            lang = ["ja-JP", "ja_JP"]
        elif choice == "russian" or choice == "7":
            lang = ["ru-RU", "ru_RU"]
    return lang

def main():
    # Instantiation of modules
    language = getLang("What is the target language? ")
    r = sr.Recognizer()
    tl = Translator()
    ss = pyttsx3.init()

    voices = ss.getProperty('voices')
    for voice in voices:
        if any(i.lower() in ''.join(voice.languages).lower() for i in language):
            ss.setProperty('voice', voice.id)
            break
        elif any(i.lower() in voice.id.lower() for i in language):
            ss.setProperty('voice', voice.id)
            break

    recordChoice = input("\nDo you have a file you would like translated? ").lower()
    rawFile = userInput(recordChoice)
    audio = readFile(rawFile, r)
    processAudio(audio, r, ss, language)

    print("\nTerminating program.")
    sys.exit()

main()
