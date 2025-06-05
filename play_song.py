
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
import os
import sys
import threading
import warnings
import yt_dlp
import pygame
from gtts import gTTS
from dotenv import load_dotenv
from langchain.tools import tool


load_dotenv()
pygame.mixer.init()

stop_flag = False  # GLOBAL STOP FLAG

@tool
def play_song(song_name: str) -> str:
    """Play a song from YouTube."""
    global stop_flag
    if stop_flag:
        return "Playback stopped."

    play_song_sound(f"Searching for song: {song_name}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
        'outtmpl': 'downloaded.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_name, download=True)
            title = info.get('title', 'Unknown')
            artist = info.get('uploader', 'Unknown Artist')

        play_song_sound(f"Now playing: {title} by {artist}")
        pygame.time.wait(2000)

        if stop_flag:
            return "Stopped before playback."

        pygame.mixer.music.load("downloaded.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if stop_flag:
                pygame.mixer.music.stop()
                break
            pygame.time.wait(100)

        if os.path.exists("downloaded.mp3"):
            os.remove("downloaded.mp3")

        return f"Played: {title} by {artist}"

    except Exception as e:
        return f"Failed to play song: {str(e)}"

def play_song_sound(text: str):
    global stop_flag
    if stop_flag:
        return

    tts = gTTS(text, lang='en')
    tts.save("ai.mp3")
    pygame.mixer.music.load("ai.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if stop_flag:
            pygame.mixer.music.stop()
            break
        pygame.time.wait(100)
    if os.path.exists("ai.mp3"):
        os.remove("ai.mp3")


def listen_microphone():
    global stop_flag
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Always Listening...")

    while True:
        if stop_flag:
            print("Listener stopped.")
            break

        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=4)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                if "stop" in command:
                    print("Stop command detected.")
                    stop_flag = True
                    pygame.mixer.music.stop()
                    break
            except:
                continue

listener_thread = threading.Thread(target=listen_microphone)
warnings.filterwarnings("ignore", category=UserWarning)
