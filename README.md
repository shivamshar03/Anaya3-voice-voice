# 🎙️ Anaya - Your Voice-Based AI Assistant

**Anaya** is an AI-powered voice assistant built using Python. It lets you speak naturally to interact with an LLM (Groq + LLaMA), get intelligent responses, and even play music from YouTube using just your voice. It's your own personal AI you can talk to, built for desktop systems.

---

## 📌 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Environment Setup](#-environment-setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Sample Commands](#-sample-commands)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

- 🎧 **Voice Input:** Speak naturally to give commands  
- 🧠 **LLM Conversations:** Context-aware AI chat via LangChain + Groq + LLaMA  
- 🔊 **Voice Responses:** Replies generated using `gTTS` and spoken aloud  
- 🎵 **YouTube Music Playback:** Stream audio using `yt-dlp`  
- 🛑 **Voice Stop Command:** Say "Stop" to stop any music or playback  
- 🗂️ **Modular Codebase:** Easily maintainable and scalable structure  

---

## 🛠️ Tech Stack

- **Python 3.8+**
- [OpenAI Whisper](https://github.com/openai/whisper) – Speech-to-Text  
- [gTTS](https://pypi.org/project/gTTS/) – Text-to-Speech  
- [pygame](https://www.pygame.org/) / `playsound` – Audio playback  
- [LangChain](https://www.langchain.com/) – LLM orchestration  
- [Groq API](https://groq.com/) – Fast LLaMA-3 based LLM  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – YouTube audio extraction  

---

## 📦 Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/anaya-ai-assistant.git
cd anaya-ai-assistant
```

## Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

## Install required packages:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Setup

Create a .env file in the root directory with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

## ▶️ Usage

Run the assistant with:
```
python main.py
```
Speak into your microphone and try commands like:

- **"What's the weather like today?"**
- **"Tell me a joke"**
- **"Play the song Closer"**
- **"Stop"**

## 📁 Project Structure

```bash
anaya/
├── main.py                # Main entry point
├── agent.py               # LangChain agent setup
├── play_song.py           # YouTube music streaming
├── speak.py               # gTTS-based speech
├── recognize.py           # Whisper transcription
├── requirements.txt
├── .env                   # API keys and config
└── README.md              # This file
```
---

## 💡 Sample Commands

| Command                            | Action                        |
|------------------------------------|-------------------------------|
| "Hello Anaya"                      | General chat                  |
| "Play the song Counting Stars"     | Stream song from YouTube      |
| "Stop"                             | Stop any music                |
| "Tell me about Python"             | AI answers using LLM          |
| "Who is Elon Musk?"                | Returns intelligent response  |

---

## 🛠️ Troubleshooting

- **Microphone not working?**  
  Ensure microphone access is enabled in your system settings.

- **Song playback stuck or repeating?**  
  Use `pygame.mixer.stop()` or handle thread cleanup properly.

- **Whisper too slow or errors?**  
  Use smaller models like `base` or `tiny` for faster results.

---

## 🤝 Contributing

Feel free to fork the repo and create pull requests. You can help with:

- 🆕 New features like calendar/reminders  
- 🐞 Bug fixes and audio enhancements  
- 🧩 Plugins (weather, news, etc.)  
- 🖥️ Adding GUI (Streamlit or Tkinter)

---

## 📜 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for full terms.

---

## 📬 Contact

Created with ❤️ by **Shivam Sharma**  
For collaboration or queries, connect via [GitHub](https://github.com/shivamshar03) or [LinkedIn](https://www.linkedin.com/in/shivam-sharma-ab489721b/?originalSubdomain=in).

---

## 🚀 Future Plans

- 📅 Google Calendar & Reminder integration  
- 🌐 Web interface with Streamlit or Flask  
- 🔌 Plugin-based extensibility  
- 🎮 Voice-controlled mini-games

---

> “Anaya aims to be the voice you trust – for help, learning, and daily tasks.”


