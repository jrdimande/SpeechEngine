import pyttsx3
import speech_recognition as sr


#Speak
def speak(audio):
    speak_txt = pyttsx3.init()
    speak_txt.say(audio)
    speak_txt.runAndWait()

#Hear
def mic():
    recognize = sr.Recognizer()

    with sr.Microphone() as source:
        recognize.pause_threshold = 1
        audio = recognize.listen(source)

    try:
        print(" Recognizing....")
        command = recognize.recognize_google(audio, language = 'En')
        print(command)
    except Exception as e:
        print(e)



