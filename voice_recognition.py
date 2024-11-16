import speech_recognition as sr
from python_event_bus import EventBus

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        print("Ajustando microfono para ruido ambiental... Por favor espere.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Microfono ajustado.")

    def recognize_command(self):
        with self.microphone as source:
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio)
            if command == "click":
                EventBus.call('click')
            # print(f"Comando reconocido: {command}")
        except sr.UnknownValueError:
            # print("No se pudo reconocer el comando.")
            pass
        except sr.RequestError:
            print("No se pudo obtener respuesta del servidor.")
        except Exception as e:
            print(f"Ocurrio un error: {e}")
    
    def voice_req_loop(self):
        while True:
            self.recognize_command()
