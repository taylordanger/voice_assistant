import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time

# Initialize the speech recognizer and engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice assistant's name
assistant_name = "Voice Assistant"

# Define a function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to greet the user
def greet():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"Hello! I am {assistant_name}. The current time is {current_time}. How may I assist you?")

# Define a function to listen for user commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I did not understand that. Please try again.")
        query = None

    return query

# Define a function to set a reminder
def set_reminder():
    speak("What would you like me to remind you about?")
    reminder = listen()

    if reminder:
        speak("When should I remind you?")
        time_str = listen()

        try:
            reminder_time = datetime.datetime.strptime(time_str, "%I:%M %p")
            now = datetime.datetime.now()

            while now.time() < reminder_time.time():
                now = datetime.datetime.now()
                time.sleep(1)

            speak(f"Reminder: {reminder}")
        except Exception as e:
            speak("Sorry, I was unable to set the reminder.")

# Define a function to create a to-do list
def create_todo_list():
    speak("What should I add to your to-do list?")
    todo_item = listen()

    if todo_item:
        with open("todo.txt", "a") as f:
            f.write(f"- {todo_item}\n")
            speak(f"Added {todo_item} to your to-do list.")

# Define a function to read the to-do list
def read_todo_list():
    try:
        with open("todo.txt", "r") as f:
            todo_list = f.read()
            if todo_list:
                speak("Here is your to-do list:")
                speak(todo_list)
            else:
                speak("Your to-do list is empty.")
    except Exception as e:
        speak("Sorry, I was unable to read your to-do list.")

# Define a function to search the web
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here is what I found for {query} on Google.")

# Greet the user when the program starts
greet()

# Start the main loop
while True:
    query = listen()

    if query:
        if "set a reminder" in query:
            set_reminder()
        elif "add to my to-do list" in query:
            create_todo_list()
        elif "read my to-do list" in query:
            read_todo_list()
        elif "search the web for" in query:
            search_query = query.replace("search the web for", "")
            search_web(search_query)
        elif "stop" in query:
            speak("Goodbye!")
            break
