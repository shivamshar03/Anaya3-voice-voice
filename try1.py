import threading
import speech_recognition as sr
import time
import sys

stop_program = False

def listen_microphone():
    global stop_program
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")

    while not stop_program:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=4)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                if "stop" in command:
                    print("Stop command detected. Exiting...")
                    stop_program = True
                    break
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"API error: {e}")
                break

def other_program_task():
    while not stop_program:
        print("Doing some other task...")
        time.sleep(1)

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_microphone)
    task_thread = threading.Thread(target=other_program_task)

    listener_thread.start()
    task_thread.start()

    listener_thread.join()
    task_thread.join()

    print("Program terminated.")
    sys.exit()
