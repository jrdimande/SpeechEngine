import  pyttsx3
import speech_recognition as sr
import cohere
import API

co = cohere.Client(API.API_key)



#Speak
def speak(audio):
    speak_txt = pyttsx3.init()
    rate = speak_txt.getProperty('rate')
    speak_txt.setProperty('rate', 175  )
    speak_txt.say(audio)
    speak_txt.runAndWait()

#Hear
def mic():
    recognize = sr.Recognizer()

    with sr.Microphone() as source:
        recognize.pause_threshold = 1
        audio = recognize.listen(source)

    try:
        print("Recognizing...")
        command = recognize.recognize_google(audio, language = 'En')
        print(f"Command:{command}")



        response = co.generate(
            model='command-xlarge-nightly',
            prompt=command,
            max_tokens=50
        )
        text = response.generations[0].text
        print(f"Response:{text}")



        speak(text)
    except Exception as e:
        print(e)

while True:
    mic()





