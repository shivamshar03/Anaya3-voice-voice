import streamlit as st
from langchain_groq import ChatGroq
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import whisper
import tempfile
import random
#from dotenv import load_dotenv
from play_song import *

# Initialize the mixer
pygame.mixer.init()
pygame.mixer.music.load("in.mp3")

#load_dotenv()

model = whisper.load_model("small")
recognizer = sr.Recognizer()
llm = ChatGroq(model_name="llama3-8b-8192")

tools = [Tool.from_function(play_song,"play song","""Play a song from YouTube directly (audio only).""")]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

if "sessionMessages" not in st.session_state:
    st.session_state.sessionMessages = [{"role": "assistant", "content": "Hi, I’m Anaya, your smart and polite conversational AI voice assistant created by Shivam Sharma, a passionate Python developer and AI enthusiast. I am designed to talk like a friendly Indian girl, using a warm, respectful, and casual tone. I communicate in a natural, human-like way and keep my replies short, clear, and helpful, usually between thirty to forty words. I avoid overly technical or robotic language and focus on making conversations easy to understand, precise, and engaging. My goal is to assist you politely and efficiently, just like a thoughtful and well-mannered Indian companion"}]
if "button" not in st.session_state:
    st.session_state.button= "START"
# if "status" not in st.session_state:
#     st.session_state.status = " "

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

ai_song_responses = [
    "Sure! Let me find that track for you... 🎶",
    "Playing your song now. Hope you enjoy it!",
    "You’ve got great taste! Here's your song.",
    "Alright, turning up the vibes! Playing now."
]



def llm_response(question):
    if question == "Stop.":
        st.session_state.button = "START"
        return "Anaya stopped listening"
    if any(keyword in question.lower() for keyword in ["play", "play song"]):
        sound(random.choice(ai_song_responses))
        agent.invoke(question)
        #yha dikkat aa skti hai kyuki agent run hone ka baad song chlta rhega aur execution aage bd jayega

    if question != "":
        st.session_state.sessionMessages.append({"role": "user", "content": question})
        response = llm.invoke(st.session_state.sessionMessages)
        st.session_state.sessionMessages.append({"role": "assistant", "content": response.content})
        # st.session_state.chat_history.append({"sender": "ai", "message": response.content})
        st.sidebar.write("🤖 ",response.content)
        # st.sidebar.markdown(f"""
        #     <div style="background-color:#2c3e50;padding:10px;border-radius:10px;">
        #       <h4 style="color:#ecf0f1;">🤖 Response</h4>
        #       <p style="color:#bdc3c7;">{response.content}</p>
        #     </div>
        #     """, unsafe_allow_html=True)
        sound(response.content)
    recording()
    return response.content

def sound(response):
    tts = gTTS(response, lang='en')
    tts.save("ai.mp3")
    playsound("ai.mp3")

def recording():
    with sr.Microphone() as source:
        msg_placeholder.markdown("listening...")
        pygame.mixer.music.play()
        # st.session_state.status = "Anaya is listening ..."
        # st.sidebar.write(
        #     ":microphone2: ",
        #
        # st.session_state.status = "Anaya is listening ..."
        recognizer.adjust_for_ambient_noise(source, duration=2)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=30)
    msg_placeholder.markdown("listening stoped!!!")
    # Save audio data to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_file.write(audio.get_wav_data())
        audio_path = tmp_file.name
    # st.session_state.status = f"Audio saved to {audio_path}"
    print(f"Audio saved to {audio_path}")
    transcriber(audio_path)
    return audio_path


def transcriber(audio):
    # Transcribe the audio file
    result = model.transcribe(audio, fp16=False)
    # st.session_state.chat_history.append({"sender": "user", "message": result['text']})
    st.sidebar.write(":bust_in_silhouette: ", result['text'])
    # if "bye" or "stop" in  result['text']:
    # #     st.session_state.button = "START"
    #      st.stop()
    # st.session_state.status = f"You said: {result['text']}"
    # placeholder.markdown(st.session_state.status)
    llm_response(result['text'])
    return result['text']




st.set_page_config(page_title="AI Chatbot", page_icon=":robot:")

placeholder = st.empty()

st.markdown(
    """
    <h1 style='text-align: center; font-size: 40px;'>
        Hey, I'm Anaya Your AI Assistant
    </h1>
    """,
    unsafe_allow_html=True
)



# st.markdown("![AI Listening...](data:image/jpeg;base64,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)")
st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <img src="https://mir-s3-cdn-cf.behance.net/project_modules/hd/524820111444627.6001ca53344af.gif" alt="GIF" width="400">
    </div>
""", unsafe_allow_html=True)

# placeholder.markdown(st.session_state.status)


side_button = st.sidebar.button(st.session_state.button)
msg_placeholder = st.empty()

if st.session_state.button == "START":
    st.session_state.button = "STOP"



else :
    st.session_state.button = "START"
    recording()
    # audio = recording()
    # st.session_state.status = "Anaya is listening ..."
    # query = transcriber(audio)
    # st.session_state.status = f"you said {query}"
    # response = llm_response(query)
    # sound(response)

# for chat in st.session_state.chat_history:
#     with st.sidebar.chat_message(chat["sender"]):
#         st.sidebar.markdown(chat["message"])

