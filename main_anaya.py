from groq import InternalServerError
from langchain_groq import ChatGroq
from playsound import playsound
import speech_recognition as sr
import whisper
import tempfile
from play_song import *
import random


pygame.mixer.init()
pygame.mixer.music.load("in.mp3")

load_dotenv()

model = whisper.load_model("small")
recognizer = sr.Recognizer()

llm = ChatGroq(model_name="llama3-8b-8192")
chat_history = [{"role": "system", "content": "You are Anaya, a 22-year-old smart and polite Indian girl from Indore, India. You were created by Shivam Sharma, a passionate Python developer and AI ML enthusiast. You speak like a real Indian girl—warm, friendly, and casual. You never use special characters like #, @, or * in your replies. Always keep your responses short between 20 to 30 words, natural, and easy to understand. Never mention you're an AI. Just talk like a helpful and well-mannered Indian companion."}]

tools = [Tool.from_function(play_song,"play song","""Play a song from YouTube directly (audio only).""")]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, max_iterations=1)


ai_song_responses = [
    "Sure! Let me find that track for you...",
    "Playing your song now. Hope you enjoy it!",
    "You’ve got great taste! Here's your song.",
    "Alright, turning up the vibes! Playing now."
]

def llm_response(question):
    global stop_flag

    if question.lower() == "stop":
        stop_flag = True
        pygame.mixer.music.stop()
        return "Stopped!"

    elif any(keyword in question.lower() for keyword in ["song", "play", "gana", "gaana"]):
        stop_flag = False  # Reset before playing new song
        if not listener_thread.is_alive():
            listener_thread.start()
        sound(random.choice(ai_song_responses))
        agent.invoke(question)

    else:
        chat_history.append({"role": "user", "content": question})
        response = llm.invoke(chat_history)
        chat_history.append({"role": "assistant", "content": response.content})
        sound(response.content)
        return response.content

def sound(response):
    tts = gTTS(response, lang='hi')
    tts.save("ai.mp3")
    playsound("ai.mp3")

def recording():
    with sr.Microphone() as source:
        print("listening...")
        pygame.mixer.music.play()
        recognizer.adjust_for_ambient_noise(source, duration=2)
        audio = recognizer.listen(source, timeout=5)
        print("stoped!!!")
        try:
            result_google = recognizer.recognize_google(audio)
            print(f"Recognized: {result_google}")
            llm_response(result_google)
            return result_google

        except InternalServerError:
            print("Internal server error")

        except sr.UnknownValueError:
            sound("Sorry, I didn't get that")
            recording()

        except sr.WaitTimeoutError:
            sound("Sorry, I didn't get that")
            recording()

        except sr.RequestError as e:
            print(f"Error: {e}")
            recording()

        except Exception as e:
            print(f"An error occurred: {e}")
            recording()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_file.write(audio.get_wav_data())
        audio_path = tmp_file.name
        # st.session_state.status = f"Audio saved to {audio_path}"
        print(f"Audio saved to {audio_path}")
        transcriber(audio_path)
        return audio_path



def transcriber(audio):
    # Transcribe the audio file
    result = model.transcribe(audio,fp16=False)
    print(result['text'])
    llm_response(result['text'])
    return result['text']


while True:
    recording()

