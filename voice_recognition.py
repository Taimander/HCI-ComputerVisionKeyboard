from pocketsphinx import LiveSpeech
from python_event_bus import EventBus

class VoiceRecognition:
    def __init__(self):
        self.speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            keyphrase="click",   # Set the keyphrase
            kws_threshold=1e-20  # Adjust sensitivity
        )

    def recognize_command(self):
        EventBus.call('click')
    
    def voice_req_loop(self):
        for speech in self.speech:
            print("Comando:",speech)
            self.recognize_command()
