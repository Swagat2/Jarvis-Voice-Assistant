Jarvis AI Assistant (Powered by Google Gemini)

Jarvis AI is a voice-controlled desktop assistant built using Python and Google’s Gemini API.
It can open applications, respond intelligently to questions, and interact with you via voice — just like a personal assistant!

🚀 Features

🎙️ Voice recognition using SpeechRecognition

💬 Smart replies using Gemini 1.5 Flash

🔊 Text-to-Speech responses with pyttsx3

🖥️ Control apps — open Notepad, Command Prompt, Spotify, WhatsApp, VS Code, etc.

🧩 Fully automatic responses (no typing required)

🌙 Simple, modern, and extendable design

🗂️ Project Structure
Jarvis Ai/
│
├── main.py               # Main Jarvis Assistant code
├── .env                  # Stores your Gemini API key securely
├── requirements.txt       # List of dependencies
└── README.md             # Project documentation

⚙️ Installation Guide
1️⃣ Clone or Download
git clone https://github.com/<your-username>/Jarvis-AI-Assistant.git
cd Jarvis-AI-Assistant

2️⃣ Install Requirements
pip install -r requirements.txt


If you don’t have a requirements.txt, create one with:

google-generativeai
speechrecognition
pyttsx3
python-dotenv
pyaudio

🔑 Setup Your Gemini API Key

Visit https://makersuite.google.com/app/apikey

Sign in with your Google account

Click Create API key

Copy your key

Then create a file named .env in your project folder and paste:

GEMINI_API_KEY=your_api_key_here

▶️ Run the Assistant
python main.py


Jarvis will greet you and start listening for voice commands 🎧
Example commands:

“Open Notepad”

“Open WhatsApp”

“Tell me a joke”

“What is artificial intelligence?”

“Exit” (to quit)

⚙️ Example Output
✅ Gemini API key loaded successfully!
Jarvis: Welcome back, sir.
Jarvis: Good morning!
Jarvis: I am Jarvis. How can I assist you today?

Listening...
Recognizing...
You said: tell me a joke

Jarvis: Why did the computer show up at work late? It had a hard drive! 😄

💡 Customization

You can easily:

Add new app shortcuts (edit the file paths inside main.py)

Change Jarvis’s voice or speed (via pyttsx3 properties)

Add GUI (Tkinter or PyQt) for chat-style interaction

🧰 Tech Stack
Component	Technology
AI Model	Google Gemini 1.5 Flash
Language	Python
Voice Recognition	SpeechRecognition + PyAudio
Speech Output	pyttsx3
Config	dotenv
💬 Author

👤 Shreeman Swagat
📍 Built with Python & Gemini API
🔗 GitHub Profile

✨ “Your voice, your command — Jarvis listens.”
