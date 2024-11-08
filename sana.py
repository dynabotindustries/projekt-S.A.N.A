import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyautogui
import wikipedia
import wolframalpha
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

class ChatbotApp(App):
    def build(self):
        # Initialize the speech engine and recognizer
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        # Set the background color of the window (dark blue/black theme)
        Window.clearcolor = (0.1, 0.1, 0.2, 1)  # Dark blue background color

        # Set the window title and icon
        self.title = 'projekt-S.A.N.A Secure Autonomous Non-Intrusive Assistant'
        Window.set_icon('logo.png')

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Top container with title, handsfree mode, voice dropdown, and clear history button
        top_container = BoxLayout(size_hint_y=0.1, height=60, padding=[10, 5], spacing=10)

        # Title and buttons at the top
        title = Label(text="S.A.N.A Virtual Assistant", size_hint=(0.5, 1), color=(1, 1, 1, 1),
                      font_size='20sp', bold=True, halign="center")
        top_container.add_widget(title)

        top_container.add_widget(self.create_handsfree_checkbox())
        top_container.add_widget(self.create_voice_spinner())
        top_container.add_widget(self.create_clear_button())

        # Create chat history (scrollable area)
        self.chat_history = ScrollView(size_hint=(1, 0.7), do_scroll_y=True)
        self.chat_content = BoxLayout(orientation="vertical", size_hint_y=None)
        self.chat_content.bind(minimum_height=self.chat_content.setter('height'))
        self.chat_history.add_widget(self.chat_content)

        # Create the text input field (same height as send button)
        self.input_field = TextInput(size_hint=(1, None), height=50, multiline=False, hint_text="Type your message...",
                                     foreground_color=(1, 1, 1, 1), background_normal='',
                                     background_color=(0.2, 0.3, 0.4, 1))

        # Create buttons for sending, speaking, and listening
        self.send_button = Button(text="Send", size_hint=(0.3, None), height=50, background_normal='',
                                  background_color=(0.2, 0.6, 0.4, 1))
        self.speak_button = Button(text="Speak", size_hint=(0.3, None), height=50, background_normal='',
                                   background_color=(0.2, 0.6, 0.4, 1))
        self.listen_button = Button(text="Listen", size_hint=(0.3, None), height=50, background_normal='',
                                    background_color=(0.2, 0.6, 0.4, 1))

        # Set up layout for input area (text input and send button in a container)
        input_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        input_layout.add_widget(self.input_field)
        input_layout.add_widget(self.send_button)

        # Button layout for listening and speaking
        button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        button_layout.add_widget(self.speak_button)
        button_layout.add_widget(self.listen_button)

        # Add all components to the main layout
        self.layout.add_widget(top_container)  # Add the top container first
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(input_layout)
        self.layout.add_widget(button_layout)

        # Bind events
        self.send_button.bind(on_press=self.on_send)
        self.speak_button.bind(on_press=self.on_speak)
        self.listen_button.bind(on_press=self.on_listen)

        return self.layout

    def create_handsfree_checkbox(self):
        self.handsfree_checkbox = CheckBox(size_hint=(0.2, 1))
        self.handsfree_label = Label(text="Handsfree Mode", size_hint=(0.8, 1), color=(1, 1, 1, 1))
        handsfree_layout = BoxLayout(size_hint=(0.4, 1), orientation="horizontal")
        handsfree_layout.add_widget(self.handsfree_checkbox)
        handsfree_layout.add_widget(self.handsfree_label)
        return handsfree_layout

    def create_voice_spinner(self):
        self.voice_spinner = Spinner(text='Select Voice', values=('Male', 'Female'), size_hint=(0.5, 1),
                                     background_color=(0.2, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        voice_layout = BoxLayout(size_hint=(0.5, 1), orientation="horizontal")
        voice_layout.add_widget(self.voice_spinner)
        return voice_layout

    def create_clear_button(self):
        self.clear_button = Button(text="Clear History", size_hint=(0.2, 1), background_color=(0.8, 0.1, 0.1, 1))
        self.clear_button.bind(on_press=self.on_clear)
        return self.clear_button

    def on_send(self, instance):
        user_input = self.input_field.text.strip().lower()
        if user_input:
            self.add_message(f"You: {user_input}")

            # Handle specific commands
            response = self.handle_input(user_input)
            self.add_message(f"Sana: {response}")
            self.on_speak(response)

            if self.handsfree_checkbox.active:
                self.on_listen()

    def handle_input(self, user_input):
        # Handle various commands as per the original code
        if "who are you" in user_input or "what are you" in user_input:
            return "Hello! I'm S.A.N.A (Secure, Autonomous, Non-intrusive Assistant)."
        elif "search" in user_input:
            query = user_input.replace("search", "").strip()
            return self.search_wikipedia(query)
        elif "play" in user_input:
            query = user_input.replace("play", "").strip()
            pywhatkit.playonyt(query)
            return f"Playing {query} on YouTube."
        elif "close" in user_input:
            pyautogui.hotkey('ctrl', 'w')
            return "Closing the current tab."
        else:
            return self.query_wolfram_alpha(user_input)

    def search_wikipedia(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return "Multiple meanings detected. Please specify."
        except wikipedia.exceptions.PageError:
            return "No results found on Wikipedia."

    def query_wolfram_alpha(self, query):
        app_id = "YOUR_WOLFRAM_ALPHA_APP_ID"
        client = wolframalpha.Client(app_id)
        try:
            res = client.query(query)
            return next(res.results).text
        except Exception:
            return "No results found on Wolfram Alpha."

    def add_message(self, message):
        label = Label(text=message, size_hint_y=None, height=40, color=(1, 1, 1, 1), halign='left')
        self.chat_content.add_widget(label)

    def on_speak(self, instance=None, text=None):
        if text is None:
            text = self.chat_content.children[0].text
        if text:
            self.engine.say(text)
            self.engine.runAndWait()

    def on_listen(self, instance=None):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                user_input = self.recognizer.recognize_google(audio)
                self.input_field.text = user_input
                self.on_send(None)  # Automatically send the recognized speech
            except sr.UnknownValueError:
                self.add_message("Sana: Sorry, I did not understand the audio.")
            except sr.RequestError:
                self.add_message("Sana: Could not request results from Google Speech Recognition.")

    def change_voice(self, spinner, text):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id if text == 'Male' else voices[1].id)

    def on_clear(self, instance):
        self.chat_content.clear_widgets()


if __name__ == '__main__':
    ChatbotApp().run()
