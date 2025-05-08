import datetime
import os
import webbrowser
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import random
import tkinter as tk
from tkinter import messagebox


def say(text):
    os.system(f"say {text}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Sorry, I am unable to understand that."

def get_news(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()

    articles = news_data.get('articles', [])

    if not articles:
        return "Sorry, I couldn't fetch the news at the moment."

    news_info = "Here are the top 5 news headlines:\n"
    for i, article in enumerate(articles[:5]):
        news_info += f"{i + 1}. {article['title']}\n"

    return news_info

def get_weather():
    url = "https://www.weather.com/en-IN/weather/today/l/28.7041,77.1025"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    temperature = soup.find('span', {'data-testid': 'TemperatureValue'}).text
    condition = soup.find('div', {'data-testid': 'wxPhrase'}).text
    return f"The current temperature is {temperature} and the condition is {condition}"

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why don't oysters donate to charity? Because they are shellfish!",
        "How does a penguin build its house? Igloos it together!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    joke = random.choice(jokes)
    print(joke)
    say(joke)

def wake_up_gui():
    wake_up_label.config(text="Listening for 'hello friday' or 'hi friday'...")

    while True:
        print("Listening for 'hello friday' or 'hi friday'...")
        query = takeCommand()
        
        if any(phrase in query.lower() for phrase in ["hello friday", "hey friday", "hi friday"]):
            wake_up_label.config(text="FRIDAY is awake!")
            say("Hello, I am FRIDAY. How can I assist you?")
            listen_for_commands()

def listen_for_commands():
    while True:
        query = takeCommand().lower()
        if "friday" in query and "stand for" in query:
            response = "It stands for Futuristic Responsive Intelligent Digital Assistant for you."
            print(response)
            say(response)

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["google", "https://www.google.com"],
            ["netflix", "https://www.netflix.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["twitter", "https://twitter.com"],
            ["reddit", "https://www.reddit.com"],
            ["linkedin", "https://www.linkedin.com"],
            ["amazon", "https://www.amazon.com"],
            ["stack overflow", "https://stackoverflow.com"],
            ["medium", "https://medium.com"],
            ["spotify", "https://www.spotify.com"],
            ["weather.com", "https://weather.com"],
            ["bbc news", "https://www.bbc.com/news"]
        ]

        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} for you...")
                webbrowser.open(site[1])

        if "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")

        if "weather update" in query:
            weather_info = get_weather()
            print(weather_info)
            say(weather_info)

        if "news update" in query:
            news_info = get_news(news_api_key)
            print(news_info)
            say(news_info)

        if "tell me a joke" in query:
            tell_joke()


# GUI Setup
root = tk.Tk()
root.title("FRIDAY Voice Assistant")
root.geometry("500x400")
root.config(bg="red")

# GUI Components
wake_up_label = tk.Label(root, text="Waiting for 'hello friday' or 'hi friday'...", font=("Helvetica", 14), bg="red", fg="white")
wake_up_label.pack(pady=20)

# Start the wake-up process
root.after(1000, wake_up_gui)

# Run the GUI
root.mainloop()
