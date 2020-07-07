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
    import moviepy.editor as mp
    from punctuator import Punctuator
except ImportError:
    print("Error: PyAudio, SpeechRecognition, GoogleTrans, pyttsx3, and MoviePy packages are needed.\
    \nPlease run $ pip install pyaudio speechrecognition googletrans pyttsx3 moviepy punctuator\
    \nIn addition, please install a punctuator training model such as:\
    \n\t $ mkdir -p ~/.punctuator\
    \n\t $ cd ~/.punctuator\
    \n\t $ gdown https://drive.google.com/uc?id=0B7BsN5f2F1fZd1Q0aXlrUDhDbnM");
    terminate()

def userInput():
    global rawFile
    recordChoice = input("\nDo you have a file you would like translated? ").lower()
    if recordChoice == "y" or recordChoice == "yes":
        fileName = input("What is the name of the file you would like translated? ")
        type = input("What format is the file in? (wav or mp4) ").lower()
        if type == "wav" or type == ".wav":
            rawFile = sr.AudioFile(fileName)
        elif type == "mp4" or type == ".mp4":
            clip = mp.VideoFileClip(fileName)
            clip.audio.write_audiofile("audio.wav")
            rawFile = sr.AudioFile("audio.wav")
        else:
            print("Apologies, the program only supports .wav and .mp4\n")
            terminate()
    elif recordChoice == "n" or recordChoice == "no":
        import recorder
        # Clean int input
        duration = input("How many seconds will you take to record your audio clip? ")
        recorder.RECORD_SECONDS = int(duration)
        print("\nPrepare to record a " + duration + " second audio clip.")
        time.sleep(2)
        print("\nStarting in ... 5")
        time.sleep(1)
        for i in range(4, 0, -1):
            print("\t\t" + str(i))
            time.sleep(1)
        recorder.record()
        rawFile = sr.AudioFile(recorder.WAVE_OUTPUT_FILENAME)
    else:
        rawFile = userInput()
    return rawFile

def readFile(rawFile, r):
    print("\nReading audio file ...")
    try:
        with rawFile as source:
            audio = r.record(rawFile)
        print("Audio file read.")
        return audio
    except FileNotFoundError:
        print("File could not be found.")
        terminate()

def processAudio(audio, r, ss, p, lang):
    try:
        print("\nProcessing audio ...")
        processed = r.recognize_google(audio, language = lang[0])
        # profanity is automatically filtered
        # r.recognize_google(audio, language="fr-FR")
        # https://cloud.google.com/speech-to-text/docs/languages
        processed = p.punctuate(processed)
        print("Audio processed.")
        print("\nTranscription of audio:\n")
        print(processed)
        return processed
    except sr.UnknownValueError:
        print("Sorry, audio was unable to be processed. Verify language \
        selections and check for excessive background noise.")

def intro():
    print("\nVideo Language Flipper (VLF) is a program used to translate various languges.")
    print("\nThis program supports the following languages:\
    \n\t1. English\
    \n\t2. Spanish\
    \n\t3. German\
    \n\t4. French\
    \n\t5. Mandarin Chinese\
    \n\t6. Japanese\
    \n\t7. Russian\n")

def getLang(prompt):
    lang = None
    while lang == None:
        choice = input(prompt).lower()
        if choice == "english" or choice == "1":
            lang = ["en-US", "en_US", "en"]
        elif choice == "spanish" or choice == "2":
            lang = ["es-ES", "es_ES", "es"]
        elif choice == "german" or choice == "3":
            lang = ["de-DE", "de_DE", "de"]
        elif choice == "french" or choice == "4":
            lang = ["fr-FR", "fr_FR", "fr"]
        elif choice == "mandarin chinese" or choice == "5":
            lang = ["zh-CN", "zh_CN", "zh-cn"]
        elif choice == "japanese" or choice == "6":
            lang = ["ja-JP", "ja_JP", "ja"]
        elif choice == "russian" or choice == "7":
            lang = ["ru-RU", "ru_RU", "ru"]
    return lang

def translateText(originalTranscript, origin, target, tl):
    print("\nTranslating audio transcription to target language ...")
    translation = tl.translate(originalTranscript, dest = target[2], src = origin[2]).text
    print("Translation complete!")
    print("\nTranslation:\n")
    print(translation)

    return translation

def speakTranslation(translation, ss):
    ss.say(translation)
    ss.save_to_file(translation, "output.wav")

    print("\nReading translation and saving to output.wav ...")
    ss.runAndWait()
    print("File saved.\n")

def terminate():
    print("\nTerminating program.\n")
    sys.exit()

def main():
    # Instantiation of modules
    intro()
    origin = getLang("What is the original language? ")
    target = getLang("What is the target language? ")
    r = sr.Recognizer()
    tl = Translator()
    ss = pyttsx3.init()
    p = Punctuator('Demo-Europarl-EN.pcl')

    ss.setProperty('rate', 140)
    voices = ss.getProperty('voices')
    for voice in voices:
        if any(i.lower() in ''.join(voice.languages).lower() for i in target):
            ss.setProperty('voice', voice.id)
            break
        elif any(i.lower() in voice.id.lower() for i in target):
            ss.setProperty('voice', voice.id)
            break

    rawFile = userInput()
    audio = readFile(rawFile, r)
    originalTranscript = processAudio(audio, r, ss, p, origin)
    translation = translateText(originalTranscript, origin, target, tl)
    speakTranslation(translation, ss)

main()
