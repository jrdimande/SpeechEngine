import  pyttsx3
import speech_recognition as sr
import cohere
import API
import datetime
import os
import platform

co = cohere.Client(API.API_key)

#Speak
def speak(audio):
    speak_txt = pyttsx3.init()
    rate = speak_txt.getProperty('rate')
    voices = speak_txt.getProperty('voices')
    speak_txt.setProperty('voice', voices[1].id)
    speak_txt.setProperty('rate', 175)
    speak_txt.say(audio)
    speak_txt.runAndWait()

def get_time():
    concurrent_time = datetime.datetime.now().strftime("%H : %M")
    speak(f"its now {concurrent_time}")

def adjust_brightness(level):
    try:
        if platform.system() == "Windows":
            os.system(f"powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
            speak(f"Brightness set to {level}%")
    except Exception as e:
        speak(f"Failed to adjust brightness. Error: {str(e)}")




























# Listen and recognize commands
def mic():
    recognize = sr.Recognizer()

    with sr.Microphone() as source:
        recognize.pause_threshold = 1
        audio = recognize.listen(source)

    try:
        print("Recognizing...")
        command = recognize.recognize_google(audio, language = "En")
        print(f"Command:{command}")

        # Instructions
        if command == "what time is it":
            get_time()

        elif 'set brightness to' in command.lower():
            try:
                level = int(command.lower().replace('set brightness to', '').strip().replace('%', ''))
                adjust_brightness(level)
            except ValueError:
                speak("Please provide a valid brightness level.")
            return














        else:
            while True:
                # Generate response using cohere API
                response = co.generate(
                    model='command-xlarge-nightly',
                    prompt=command,
                    max_tokens=100
                )
                text = response.generations[0].text
                print(f"Response:{text}")
                speak(text)
                break




    except Exception as e:
        print(e)


flag = True
while flag:
    mic()




