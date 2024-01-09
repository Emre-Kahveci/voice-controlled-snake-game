import speech_recognition as sr

class SpeechToText:
    def __init__(self, device_index=1):
        self.r = sr.Recognizer()  # Recognizer nesnesi oluşturma
        self.microphone = sr.Microphone(device_index=device_index) # Mikrofon nesnesi oluşturma
        self.calibrate_microphone() # Mikrofonu kalibre etme

    def calibrate_microphone(self):
        with self.microphone as source:
            print("Mikrofon kalibre ediliyor. Lütfen sessiz olunuz")
            self.r.adjust_for_ambient_noise(source, duration=2) # Mikrofonu kalibre etme
            self.r.energy_threshold += 75 # Mikrofon kalibrasyonu için eşik değerini ayarlama
            self.calculated_energy_threshold = self.r.energy_threshold # Eşik değerini kaydetme

    def speech_to_text(self, audio):
        if not isinstance(audio, sr.AudioData): # Dosyanın ses dosyası olduğunu kontrol etme
            print("Dosya bir ses dosyası değil.")
            return

        try:
            return self.r.recognize_google(audio, language='tr-TR') # Ses dosyasını metne çevirme
        except sr.UnknownValueError:
            return "Anlaşılamayan ses."
        except sr.RequestError:
            return "Zaman aşımı"

    def listen_command(self):
        audio = self.record_audio() # Ses kaydı alma
        if audio: # Ses kaydı alınmışsa
            text = self.speech_to_text(audio).lower() # Ses kaydını metne çevirme
            return self.process_text_command(text) # Metni döndürme
        else:
            return False

    def record_audio(self):
        self.r.energy_threshold = self.calculated_energy_threshold # Eşik değerini ayarlama
        self.r.dynamic_energy_threshold = False # Eşik değerinin dinamik olmamasını sağlama
        try:
            print("Sesli komut bekleniyor.")
            with self.microphone as source:
                return self.r.listen(source, 10, 1) # Ses kaydı alma
        except sr.WaitTimeoutError:
            return False

    def process_text_command(self, text):
        if "yukarı" in text: # Metin içerisinde yukarı kelimesi varsa
            return 1
        elif "aşağı" in text: # Metin içerisinde aşağı kelimesi varsa
            return 2
        elif "sol" in text: # Metin içerisinde sol kelimesi varsa
            return 3
        elif any(key in text for key in ["sağ", "saha"]): # Metin içerisinde sağ veya saha kelimelerinden biri varsa
            return 4
        else: # Yukarı, aşağı, sol veya sağ kelimelerinden biri yoksa
            print(text) 
            return False