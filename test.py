import tkinter as tk
from tkinter import scrolledtext, DISABLED, NORMAL, END
import threading
import pyttsx3
import datetime
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
import wikipedia
import webbrowser as wb
import random
import pyautogui
import pyjokes
import customtkinter as ctk


# ---------------- LOAD API KEY ----------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key not found! Please check your .env file for GEMINI_API_KEY.")
else:
    print("Gemini API key loaded successfully!")
    genai.configure(api_key=api_key)


# ---------------- AI REPLY FUNCTION (Gemini) ----------------
def ai_reply(prompt):
    """
    Gets the AI response from the Gemini API.
    """
    if not api_key:
        return "Sorry, the Gemini API key is not configured."
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="You are Jarvis, a helpful and concise AI assistant."
        )
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        answer = response.text
        return answer
    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"Sorry, I encountered an error with Gemini: {e}"


# ---------------- GUI APPLICATION ----------------
class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Assistant (Gemini + Local)")
        self.root.geometry("600x500")

        # --- Setup speech engine ---
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        try:
            self.engine.setProperty('voice', voices[1].id)
        except IndexError:
            self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170)

        # --- Setup recognizer ---
        self.recognizer = sr.Recognizer()

        # Create GUI widgets
        self.create_widgets()

        # Start with a greeting
        self.root.after(100, self.start_greeting_thread)

    def create_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=DISABLED, font=("Arial", 11),
                                                   bg="#2B2B2B", fg="#E0E0E0", insertbackground="white")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.listen_button = tk.Button(self.root, text="Listen 🎙️", font=("Arial", 14, "bold"),
                                       command=self.start_listening_thread, bg="#007AFF", fg="white", relief=tk.FLAT,
                                       width=20, activebackground="#0056B3", activeforeground="white")
        self.listen_button.pack(pady=10)

        self.root.config(bg="#1C1C1C")

    # --- Core Speech and GUI Methods ---

    def speak(self, text):
        """
        Speaks the given text *and* adds it to the chat.
        (This simplifies the logic)
        """
        self.add_to_chat(f"Jarvis: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech Error: {e}")
            self.add_to_chat(f"System Error: Could not speak. {e}")

    def add_to_chat(self, message, tag=None):
        """
        Safely adds a message to the chat area from any thread.
        """

        def _add():
            self.chat_area.config(state=NORMAL)
            if tag == "user":
                self.chat_area.insert(END, message + "\n\n", "user_tag")
            else:
                self.chat_area.insert(END, message + "\n\n")
            self.chat_area.config(state=DISABLED)
            self.chat_area.see(END)

        # Configure tag for user text
        self.chat_area.tag_config("user_tag", foreground="#90CAF9", font=("Arial", 11, "bold"))
        self.root.after(0, _add)

    def listen_from_mic(self):
        """
        Listens for audio from the microphone and recognizes it.
        """
        with sr.Microphone() as source:
            self.add_to_chat("Listening...")
            self.recognizer.pause_threshold = 1
            self.recognizer.energy_threshold = 400
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                self.add_to_chat("Listening timed out. Please try again.")
                return ""

        try:
            self.add_to_chat("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            self.add_to_chat(f"You: {query}\n", "user")
            return query.lower()
        except sr.UnknownValueError:
            self.speak("I didn’t hear anything clearly, please try again.")
            return ""
        except sr.RequestError as e:
            self.add_to_chat(f"Speech service error: {e}")
            return ""
        except Exception as e:
            self.add_to_chat(f"Recognition error: {e}")
            return ""

    # --- Threading ---

    def start_listening_thread(self):
        self.listen_button.config(text="Listening...", state=DISABLED, bg="#555555")
        threading.Thread(target=self.process_commands, daemon=True).start()

    def start_greeting_thread(self):
        threading.Thread(target=self.initial_greeting, daemon=True).start()

    # --- LOCAL ACTION FUNCTIONS (from your 2nd script) ---
    # Note: They are now methods of the class, so they use `self`.

    def time_now(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {current_time}")

    def date_now(self):
        now = datetime.datetime.now()
        self.speak(f"Today is {now.strftime('%d %B %Y')}")

    def search_wikipedia(self, query):
        try:
            self.speak("Searching Wikipedia...")
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(results)
        except wikipedia.exceptions.DisambiguationError:
            self.speak("There are multiple results. Please be more specific.")
        except Exception:
            self.speak("Sorry, I couldn't find anything on Wikipedia.")

    def play_music(self, song_name=None):
        music_dir = os.path.expanduser("~\\Music")
        if not os.path.exists(music_dir):
            self.speak("Music folder not found.")
            return
        songs = [s for s in os.listdir(music_dir) if s.endswith(('.mp3', '.wav'))]
        if not songs:
            self.speak("Your music folder seems to be empty.")
            return

        found_songs = []
        if song_name:
            found_songs = [s for s in songs if song_name.lower() in s.lower()]

        if found_songs:
            song_to_play = random.choice(found_songs)
            os.startfile(os.path.join(music_dir, song_to_play))
            self.speak(f"Playing {song_to_play}")
        elif not song_name:  # Play random if no name given
            song_to_play = random.choice(songs)
            os.startfile(os.path.join(music_dir, song_to_play))
            self.speak(f"Playing a random song: {song_to_play}")
        else:
            self.speak(f"Sorry, no song found with the name {song_name}.")

    def open_app(self, app_name):
        # IMPORTANT: Update these paths to match YOUR system
        apps = {
            "vs code": r"C:\Users\Shree\Desktop\Visual Studio Code.lnk",
            "visual studio code": r"C:\Users\Shree\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code.lnk",
            "command prompt": r"C:\Users\Shree\Desktop\Command Prompt.lnk",
            "spotify": r"C:\Users\Shree\Desktop\Spotify - Shortcut.lnk",
            "whatsapp": r"C:\Users\Shree\Desktop\WhatsApp.lnk"
        }

        found = False
        for key in apps:
            if key in app_name:
                path = apps[key]
                if os.path.exists(path):
                    self.speak(f"Opening {key}")
                    os.startfile(path)
                    found = True
                else:
                    self.speak(f"Sorry, I can't find {key} at the path: {path}")
                return

        if not found:
            self.speak("Sorry, that app is not in my list yet.")

    def screenshot(self):
        try:
            img = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.expanduser(f"~\\Pictures\\screenshot_{timestamp}.png")
            img.save(path)
            self.speak(f"Screenshot saved to your Pictures folder.")
        except Exception as e:
            self.speak(f"Sorry, I couldn't take a screenshot. Error: {e}")

    # --- Main Logic Functions ---

    def initial_greeting(self):
        if not api_key:
            self.speak("ERROR. Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
            return

        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"

        self.speak(f"Welcome back, sir. {greeting}")
        self.speak("I am Jarvis, powered by Gemini and local commands. How can I assist you today?")

    def process_commands(self):
        """
        This is the main logic loop.
        It checks for local commands first, then asks the AI.
        """
        if not api_key:
            self.root.after(0, self.enable_button)
            return

        query = self.listen_from_mic()

        if query:
            # --- Local Command Check (from your 2nd script) ---
            if "time" in query:
                self.time_now()

            elif "date" in query:
                self.date_now()

            elif "wikipedia" in query:
                search_query = query.replace("search", "").replace("on", "").replace("about", "").replace("wikipedia",
                                                                                                          "").strip()
                if search_query:
                    self.search_wikipedia(search_query)
                else:
                    self.speak("What would you like me to search on Wikipedia?")

            elif "play music" in query:
                song = query.replace("play music", "").strip()
                self.play_music(song)

            elif "open youtube" in query:
                self.speak("Opening YouTube")
                wb.open("https://youtube.com")

            elif "open google" in query:
                self.speak("Opening Google")
                wb.open("https://google.com")

            elif "open" in query:
                app_name = query.replace("open", "").strip()
                self.open_app(app_name)

            elif "screenshot" in query:
                self.screenshot()

            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                self.speak(joke)

            elif "shutdown" in query:
                self.speak("Shutting down the system, goodbye!")
                os.system("shutdown /s /f /t 1")
                self.root.after(2000, self.root.destroy)
                return

            elif "restart" in query:
                self.speak("Restarting the system.")
                os.system("shutdown /r /f /t 1")
                self.root.after(2000, self.root.destroy)
                return

            elif "exit" in query or "quit" in query or "stop" in query or "offline" in query:
                self.speak("Goodbye sir, have a nice day!")
                self.root.after(2000, self.root.destroy)
                return

            # --- If NO local command, ask Gemini ---
            else:
                self.speak("One moment, I'm thinking...")
                response = ai_reply(query)
                self.speak(response)

        # Re-enable the button when done
        self.root.after(0, self.enable_button)

    def enable_button(self):
        """Helper to re-enable the listen button."""
        self.listen_button.config(text="Listen 🎙️", state=NORMAL, bg="#007AFF")


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    if not api_key:
        print("CRITICAL: Gemini API key not found. Please create a .env file with GEMINI_API_KEY=your_key_here")

    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()