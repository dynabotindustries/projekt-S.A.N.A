import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTextEdit, QLabel, QMessageBox)
from PyQt5.QtGui import QPixmap
import wikipedia
import wolframalpha
import pyttsx3
import speech_recognition as sr
import pywhatkit

# Function to search Wikipedia
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "Multiple meanings detected. Please specify: " + ", ".join(e.options[:5])
    except wikipedia.exceptions.PageError:
        return "No results found on Wikipedia."

# Function to query Wolfram Alpha
def query_wolfram_alpha(query, app_id):
    client = wolframalpha.Client(app_id)
    try:
        res = client.query(query)
        return next(res.results).text
    except Exception:
        return "No results found on Wolfram Alpha."

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.usernameEdit = QLineEdit(self)
        self.usernameEdit.setPlaceholderText('Username')
        layout.addWidget(self.usernameEdit)

        self.passwordEdit = QLineEdit(self)
        self.passwordEdit.setPlaceholderText('Password')
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordEdit)

        self.loginButton = QPushButton('Login', self)
        self.loginButton.clicked.connect(self.checkCredentials)
        layout.addWidget(self.loginButton)

        self.setLayout(layout)

    def checkCredentials(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        if username == 'test' and password == 'testing':
            self.chatWindow = ChatWindow()
            self.chatWindow.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect Username or Password')

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.engine = pyttsx3.init()  # Initialize text-to-speech engine
        self.recognizer = sr.Recognizer()  # Initialize speech recognizer

    def initUI(self):
        # Layouts
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Image Label
        self.imageLabel = QLabel(self)
        pixmap = QPixmap('image.png')  # Ensure this image is in your working directory
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setFixedSize(200, 200)
        self.imageLabel.setStyleSheet("border-radius: 25px;")

        # Text Edit (Chat History)
        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setStyleSheet("background-color: #333; color: white; border-radius: 10px; padding: 10px;")

        # Line Edit (Input field)
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet("background-color: #555; color: white; border-radius: 10px; padding: 10px;")

        # Send Button
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.onSend)
        self.sendButton.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")

        # Speak Button
        self.speakButton = QPushButton('Speak')
        self.speakButton.clicked.connect(self.onSpeak)
        self.speakButton.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")

        # Listen Button
        self.listenButton = QPushButton('Listen')
        self.listenButton.clicked.connect(self.onListen)
        self.listenButton.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")

        # Clear History Button
        self.clearButton = QPushButton('Clear History')
        self.clearButton.clicked.connect(self.onClear)
        self.clearButton.setStyleSheet("background-color: rgba(92, 172, 196, 0.5); color: white; border-radius: 10px;")
        self.clearButton.setFixedSize(150, 30)  # Adjust the size as needed

        # Adding widgets to layout
        topLayout = QHBoxLayout()
        topLayout.addStretch()
        topLayout.addWidget(self.clearButton)

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.lineEdit)
        inputLayout.addWidget(self.sendButton)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.listenButton)
        bottomLayout.addWidget(self.speakButton)

        hbox.addWidget(self.imageLabel)
        hbox.addStretch()
        hbox.addWidget(self.chatHistory, 1)

        vbox.addLayout(topLayout)
        vbox.addLayout(hbox)
        vbox.addLayout(inputLayout)
        vbox.addLayout(bottomLayout)

        self.setLayout(vbox)
        self.setWindowTitle('Projekt S.A.N.A.')
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: #222;")

    def onSend(self):
        user_input = self.lineEdit.text().strip().lower()
        if user_input:
            self.chatHistory.append("You: " + user_input)
            self.lineEdit.clear()
            
            # Custom response for "who are you" or similar queries
            if any(phrase in user_input for phrase in ["who are you", "what are you", "who is this", "what is this", "who is sana", "what is sana"]):
                response = "Hello! I'm S.A.N.A (Secure, Autonomous, Non-intrusive Assistant), an open-source virtual assistant designed to prioritize your privacy and respect your autonomy. I'm here to help you with your tasks and queries without compromising your data or monitoring your activities."
            elif "search" in user_input:
                query = user_input.replace("search", "").strip()
                response = search_wikipedia(query)
            elif "play" in user_input:
                query = user_input.replace("play", "").strip()
                pywhatkit.playonyt(query)
                response = f"Playing {query} on YouTube."
            else:
                app_id = "PHP8VP-Y7P8Y25TTW"  # Replace with your actual API key
                response = query_wolfram_alpha(user_input, app_id)
            
            self.chatHistory.append("Sana: " + response)

    def onSpeak(self):
        latest_response = self.chatHistory.toPlainText().split('Sana:')[-1].strip()
        if latest_response:
            self.engine.say(latest_response)
            self.engine.runAndWait()

    def onListen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                user_input = self.recognizer.recognize_google(audio)
                self.lineEdit.setText(user_input)
            except sr.UnknownValueError:
                self.chatHistory.append("Sana: Sorry, I did not understand the audio.")
            except sr.RequestError:
                self.chatHistory.append("Sana: Could not request results; check your network connection.")

    def onClear(self):
        self.chatHistory.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
