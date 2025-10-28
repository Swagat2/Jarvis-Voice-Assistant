import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import subprocess
import time



# ---------------- SPEECH ENGINE SETUP ----------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')

if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)


def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()


# ---------------- BASIC FUNCTIONS ----------------
def time_now():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")


def date_now():
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%d %B %Y')}")


def load_name():
    try:
        with open("assistant_name.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Jarvis"


def wishme():
    hour = datetime.datetime.now().hour
    speak("Welcome back, sir.")
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 17:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    name = load_name()
    speak(f"I am {name}. How can I assist you today?")


# ---------------- MICROPHONE INPUT ----------------
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = None
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            speak("I didn’t hear anything, please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable right now.")
        return None


# ---------------- FEATURES ----------------
def screenshot():
    img = pyautogui.screenshot()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.expanduser(f"~\\Pictures\\screenshot_{timestamp}.png")
    img.save(path)
    speak(f"Screenshot saved as screenshot_{timestamp}.png in Pictures folder.")


def play_music(song_name=None):
    music_dir = os.path.expanduser("~\\Music")
    if not os.path.exists(music_dir):
        speak("Music folder not found.")
        return

    songs = os.listdir(music_dir)
    if not songs:
        speak("Your music folder seems to be empty.")
        return

    if song_name:
        songs = [s for s in songs if song_name.lower() in s.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(music_dir, song))
        speak(f"Playing {song}")
    else:
        speak("No song found with that name.")


def set_name():
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as f:
            f.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("I couldn't catch that name.")


def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        print(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except Exception:
        speak("Sorry, I couldn't find anything on Wikipedia.")


# ---------------- APP OPENING ----------------
def open_app(app_name):
    """Open predefined apps using file paths"""
    apps = {
        "vs code": r"C:\Users\Shree\Desktop\Visual Studio Code.lnk",
        "visual studio code": r"C:\Users\Shree\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code.lnk",
        "command prompt": r"C:\Users\Shree\Desktop\Command Prompt.lnk",  # Same as given
        "spotify": r"C:\Users\Shree\Desktop\Spotify - Shortcut.lnk",
        "whatsapp": r"C:\Users\Shree\Desktop\WhatsApp.lnk"
    }

    for key in apps:
        if key in app_name:
            path = apps[key]
            if os.path.exists(path):
                speak(f"Opening {key}")
                os.startfile(path)
            else:
                speak(f"Sorry, I can't find {key} on your system.")
            return

    speak("Sorry, that app is not in my list yet.")


# ---------------- MAIN FUNCTION ----------------
if __name__ == "__main__":
    wishme()
    try:
        while True:
            query = takecommand()
            if not query:
                continue

            if "time" in query:
                time_now()

            elif "date" in query:
                date_now()

            elif "wikipedia" in query:
                query = query.replace("search", "").replace("on", "").replace("about", "").replace("wikipedia", "").strip()
                search_wikipedia(query)

            elif "play music" in query:
                song = query.replace("play music", "").strip()
                play_music(song)

            elif "open youtube" in query:
                speak("Opening YouTube")
                wb.open("https://youtube.com")

            elif "open google" in query:
                speak("Opening Google")
                wb.open("https://google.com")

            elif "open" in query:
                app_name = query.replace("open", "").strip()
                open_app(app_name)

            elif "change your name" in query or "set your name" in query:
                set_name()

            elif "screenshot" in query:
                screenshot()

            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "help" in query or "commands" in query:
                speak("I can tell you the time, date, take screenshots, play music, tell jokes, search Wikipedia, open websites, or launch applications like VS Code, Spotify, or WhatsApp.")

            elif "shutdown" in query:
                speak("Shutting down the system, goodbye!")
                os.system("shutdown /s /f /t 1")
                break

            elif "restart" in query:
                speak("Restarting the system.")
                os.system("shutdown /r /f /t 1")
                break

            elif "exit" in query or "offline" in query or "stop" in query:
                speak("Going offline. Have a great day!")
                break

    except KeyboardInterrupt:
        speak("Goodbye, sir.")
