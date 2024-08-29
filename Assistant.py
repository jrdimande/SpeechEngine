import speech_recognition as sr
import  pyttsx3
import cohere
import API
import datetime
import os
import platform
import webbrowser
import  subprocess
import time

co = cohere.Client(API.API_key)

# Function to Speak
def speak(audio):
    speak_txt = pyttsx3.init()
    rate = speak_txt.getProperty('rate')
    voices = speak_txt.getProperty('voices')
    speak_txt.setProperty('voice', voices[0].id)
    speak_txt.setProperty('rate', 173)
    speak_txt.say(audio)
    speak_txt.runAndWait()

# Function to get Time
def get_time():
    concurrent_time = datetime.datetime.now().strftime("%H : %M")
    speak(f"its now {concurrent_time}")

# OS
def adjust_brightness(level):
    try:
        if platform.system() == "Windows":
            os.system(f"powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
            speak(f"Brightness set to {level}%")
    except Exception as e:
        speak(f"Failed to adjust brightness. Error: {str(e)}")


def restart_computer():
    speak("I will restart your device in 3 seconds")
    for c in range(1, 4):
        speak(c)
        time.sleep(1)

    subprocess.call(["shutdown", "-r", "-t", "0"])





# Function to open apps
def open_application(app_name):
    try:
        if platform.system() == "Windows":
            os.system(f'start {app_name}')

        speak(f"Opening {app_name}")
    except Exception as e:
        speak(f"I couldn't open {app_name}. Error: {str(e)}")



# Functions to open web Aplications
def open_youtube():
        url = "https://www.youtube.com"
        speak("Opening youtube")
        webbrowser.open(url)

def open_google():
        url = "https://google.com"
        speak("opening google")
        webbrowser.open(url)

def open_github():
    url = "https://github.com/login"
    speak("opening github")
    webbrowser.open(url)

def open_stack_overflow():
    url = "https://stackoverflow.com"
    speak("opening stackoverflow")
    webbrowser.open(url)

def open_chatgpt():
    url = "https://chatgpt.com"
    speak("opening chat gpt")
    webbrowser.open(url)

def open_instagram():
    url = "https://instagram.com/login"
    speak("Open instagram login page")
    webbrowser.open(url)


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

        # Get time
        if command == "what time is it":
            get_time()

        # Set brightness
        elif 'set brightness to' in command.lower():
            try:
                level = int(command.lower().replace('set brightness to', '').strip().replace('%', ''))
                adjust_brightness(level)
            except ValueError:
                speak("Please provide a valid brightness level.")
            return

        # Restart computer
        elif 'restart device' in command.lower():
            restart_computer()



        # Open web aplications
        elif 'open' in command.lower():
            app_name = command.lower().replace('open', '').strip()
            open_application(app_name)

        elif 'youtube' in command.lower():
            open_youtube()

        elif 'google' in command.lower():
            open_google()

        elif 'github' in command.lower():
            open_github()

        elif 'stackoverflow' in command.lower():
            open_stack_overflow()

        elif 'instagram' in command.lower():
            open_instagram()

        elif 'ai' in command.lower():
            open_chatgpt()

        # Stop execution
        elif 'stop running' in command.lower():
            flag = False


        else:
            while True:
                # Generate response using cohere API
                response = co.generate(
                    model='command-xlarge-nightly',
                    prompt=command,
                    max_tokens=120
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




