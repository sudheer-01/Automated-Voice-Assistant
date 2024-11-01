import speech_recognition as aa
import pyttsx3 
import datetime
import wikipedia
import webbrowser
import requests
import os
import pywhatkit
import pyautogui

r = aa.Recognizer()
machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    global instruction
    try:
        with aa.Microphone() as origin:
            print("listening..")
            audio = r.listen(origin)
            instruction = r.recognize_google(audio)
            instruction = instruction.lower()
            if "chitti" in instruction:
                instruction = instruction.replace('chitti', '')
                print(instruction)
            return instruction
    except aa.UnknownValueError:
        print("Google Speech Recognition could not understand your audio")
    except aa.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    talk("Screenshot taken and saved as screenshot.png")

def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    data = response.json()
    if "title" not in data:
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        talk(f"The definition of {word} is {meaning}")
        print(f"The definition of {word} is  {meaning}")
    else:
        talk("Word not found")

def play_chitti():
    instruction = input_instruction()
    if instruction is None:
        return
    print(instruction)
    if "play" in instruction:
        song = instruction.replace('play', "")
        talk("playing" + song)
        pywhatkit.playonyt(song)
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('current time' + time)
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date" + date)
    elif 'how are you' in instruction:
        talk('I am fine, how about you?')
    elif 'what is your name' in instruction:
        talk('I am chitti 2.0, What can I do for you?')
    elif 'who is' in instruction:
        human = instruction.replace('who is', " ")
        info = wikipedia.summary(human, 1)
        print(info)
        talk(info)
    elif 'youtube' in instruction:
        talk("Opening YouTube")
        webbrowser.open('https://www.youtube.com')
    elif 'instagram' in instruction:
        talk("Opening Instagram")
        webbrowser.open('https://www.instagram.com')
    elif 'open chrome' in instruction:
        talk("Opening Chrome")
        webbrowser.open('https://www.google.com/chrome')
    elif 'open google' in instruction:
        talk("Opening Google")
        webbrowser.open('https://www.google.com')
    elif 'tell me a joke' in instruction:
        joke = "Why don't scientists trust atoms? Because they make up everything!"
        talk(joke)
    elif 'search google for' in instruction:
        query = instruction.replace('search google for', "")
        talk("Searching Google for" + query)
        pywhatkit.search(query)
    elif 'set a timer for' in instruction:
        try:
            duration = int(instruction.replace('set a timer for', "").strip())
            talk(f"Setting a timer for {duration} seconds")
            time.sleep(duration)
            talk(f"{duration} seconds timer is up")
        except ValueError:
            talk("I couldn't understand the duration. Please try again.")
    elif 'open facebook' in instruction:
        talk("Opening Facebook")
        webbrowser.open('https://www.facebook.com')
    elif 'take a screenshot' in instruction:
        take_screenshot()
    elif 'define' in instruction:
        word_to_define = instruction.replace('define', "").strip()
        define_word(word_to_define)
    else:
        talk('Please repeat')

play_chitti()
