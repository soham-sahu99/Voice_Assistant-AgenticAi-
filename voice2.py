import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os

# Configure the Gemini API
genai.configure(api_key="AIzaSyCcQS51y3q5UCCSH7EYI4QajqqqGTGffuE")

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.configure_voice()
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def configure_voice(self):
        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)


    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=20)
            
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

    def get_ai_response(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error processing request: {str(e)}"

    def run(self):
        self.speak("Hello Soham! I'm your assistant. How can I help you?")
        
        while True:
            user_input = self.listen()
            if not user_input:
                continue
                
            if "exit" in user_input.lower():
                self.speak("Goodbye!")
                break
                
            response = self.get_ai_response(user_input)
            print(f"AI: {response}")
            self.speak(response)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
