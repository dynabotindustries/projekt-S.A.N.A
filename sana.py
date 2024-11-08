import sys
import os
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTextEdit, QLabel, QMessageBox, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
import wikipedia
import wolframalpha
import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyautogui

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "Multiple meanings detected. Please specify: " + ", ".join(e.options[:5])
    except wikipedia.exceptions.PageError:
        return "No results found on Wikipedia."

def query_wolfram_alpha(query, app_id):
    client = wolframalpha.Client(app_id)
    try:
        res = client.query(query)
        return next(res.results).text
    except Exception:
        return "No results found on Wolfram Alpha."

def send_whatsapp(number, message):
    try:
        # Use pywhatkit to send a WhatsApp message
        pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
        return f"Message sent to {number}."
    except Exception as e:
        return f"Failed to send message: {str(e)}"

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
        self.engine = pyttsx3.init()  
        self.recognizer = sr.Recognizer()  
        self.initUI()

    def initUI(self):
        # Layouts
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # GIF Label
        self.gifLabel = QLabel(self)
        movie = QMovie('animation.gif') 
        self.gifLabel.setMovie(movie)
        movie.start()
        #self.gifLabel.setFixedSize(200, 200)

        
        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setStyleSheet("background-color: #333; color: white; border-radius: 10px; padding: 10px;")

        
        self.lineEdit = QLineEdit()
        self.lineEdit.setStyleSheet("background-color: #555; color: white; border-radius: 10px; padding: 10px;")

        
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.onSend)
        self.sendButton.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")

        
        self.speakButton = QPushButton('Speak')
        self.speakButton.clicked.connect(self.onSpeak)
        self.speakButton.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")

      
        self.listenButton = QPushButton('Listen')
        self.listenButton.clicked.connect(self.onListen)
        self.listenButton.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")

        
        self.clearButton = QPushButton('Clear History')
        self.clearButton.clicked.connect(self.onClear)
        self.clearButton.setStyleSheet("background-color: rgba(92, 172, 196, 0.5); color: white; border-radius: 10px;")
        self.clearButton.setFixedSize(150, 30)

        
        self.handsfreeCheckbox = QCheckBox('Handsfree Mode')
        self.handsfreeCheckbox.stateChanged.connect(self.toggleHandsfreeMode)
        self.handsfreeCheckbox.setStyleSheet("color: white;")

        
        self.voiceComboBox = QComboBox(self)
        voices = self.engine.getProperty('voices')
        self.voiceComboBox.addItem('Male')
        self.voiceComboBox.addItem('Female')
        self.voiceComboBox.setStyleSheet("background-color: #5CACC4; color: white; border-radius: 10px;")
        self.voiceComboBox.currentIndexChanged.connect(self.changeVoice)

        
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.handsfreeCheckbox)
        topLayout.addStretch()
        topLayout.addWidget(self.clearButton)
        topLayout.addWidget(self.voiceComboBox)

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.lineEdit)
        inputLayout.addWidget(self.sendButton)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.listenButton)
        bottomLayout.addWidget(self.speakButton)

        hbox.addWidget(self.gifLabel)
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

            
            if any(phrase in user_input for phrase in ["who are you", "what are you", "who is this", "what is this", "who is sana", "what is sana"]):
                response = "Hello! I'm S.A.N.A (Secure, Autonomous, Non-intrusive Assistant), an open-source virtual assistant designed to prioritize your privacy and respect your autonomy. I'm here to help you with your tasks and queries without compromising your data or monitoring your activities."
            elif "search" in user_input:
                query = user_input.replace("search", "").strip()
                response = search_wikipedia(query)
            elif "badword" in user_input:
                response = "Inappropriate language detected, halting operation."
            elif "hey sana" in user_input:
                response = "Yes boss, waiting for your command."
            elif "play" in user_input:
                query = user_input.replace("play", "").strip()
                pywhatkit.playonyt(query)
                response = f"Playing {query} on YouTube."
            elif "close" in user_input:
                pyautogui.hotkey('ctrl', 'w')  
                response = "Closing the current tab."
            elif "whatsapp(" in user_input:
                match = re.match(r"whatsapp$(\d+),\s*'(.+?)'$", user_input)
                if match:
                    number = match.group(1)
                    message = match.group(2)
                    response = send_whatsapp(number, message)
                else:
                    response = "Invalid WhatsApp command. Use format: whatsapp(number,'message')"
            else:
                app_id = "PHP8VP-Y7P8Y25TTW"  
                response = query_wolfram_alpha(user_input, app_id)

            self.chatHistory.append("Sana: " + response)
            self.onSpeak(response)  
            if self.handsfreeCheckbox.isChecked():
                self.onListen()

    def onSpeak(self, text=None):
        if text is None:
            latest_response = self.chatHistory.toPlainText().split('Sana:')[-1].strip()
        else:
            latest_response = text

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
                self.onSend() 
            except sr.UnknownValueError:
                self.chatHistory.append("Sana: Sorry, I did not understand the audio.")
            except sr.RequestError:
                self.chatHistory.append("Sana: Could not request results from Google Speech Recognition service.")
            if self.handsfreeCheckbox.isChecked():
                self.onListen()

    def onClear(self):
        self.chatHistory.clear()

    def toggleHandsfreeMode(self, state):
        if state == Qt.Checked:
            self.onListen()

    def changeVoice(self, index):
        voices = self.engine.getProperty('voices')
        if index == 0:
            self.engine.setProperty('voice', voices[0].id)
        else:
            self.engine.setProperty('voice', voices[1].id)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	login = LoginWindow()
	login.show()
	sys.exit(app.exec_())
