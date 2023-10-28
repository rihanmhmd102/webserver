import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
from datetime import datetime, timedelta

st.title("Mood Analyzer")

mood_data = {'Happy': 0, 'Sad': 0, 'Neutral': 0}
weekly_mood = []

def update_mood(text):
    global mood_data
    global weekly_mood

    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    if sentiment > 0:
        mood = 'Happy'
    elif sentiment < 0:
        mood = 'Sad'
    else:
        mood = 'Neutral'

    mood_data[mood] += 1
    weekly_mood.append(mood)

def get_weekly_mood():
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_mood = [mood_data[m] for m in weekly_mood if (datetime.now() - timedelta(days=datetime.now().weekday())) <= week_start]
    weekly_mood.clear()

    if not week_mood:
        return "No data"
    
    avg_mood = sum(week_mood) / len(week_mood)
    
    if avg_mood > 0:
        return 'Happy'
    elif avg_mood < 0:
        return 'Sad'
    else:
        return 'Neutral'

def record_and_analyze():
    user_input = speech_to_text()
    update_mood(user_input)
    update_gui()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something about your day...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech not recognized"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def update_gui():
    st.write("Mood statistics updated.")

if st.button("Record and Analyze"):
    record_and_analyze()

weekly_mood_text = get_weekly_mood()
st.write(f"Weekly Overall Mood: {weekly_mood_text}")
