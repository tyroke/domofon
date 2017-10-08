import speech_recognition as sr


class Rozpoznawacz:
    def __init__(self):
        self.r = sr.Recognizer()
        self.audio = None

    def zapisz(self, nazwa):
        with open(nazwa, 'wb') as f:
            f.write(self.audio.get_wav_data())

    def otworz(self, nazwa):
        with sr.AudioFile(nazwa) as source:
            self.audio = self.r.record(source)

    def nagraj(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print('Dawaj leszczu!')
            self.audio = self.r.listen(source)
            print('Brawo leszczu!')

    def rozpoznaj(self):
        try:
            # print("You said: " + r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY"))
            print('You said: ' + self.r.recognize_google(self.audio))
        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand audio')
        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition service; {0}'.format(e))


def odtworz(nazwa):
    import pyaudio
    import wave

    chunk = 1024

    wf = wave.open(nazwa, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()

rec = Rozpoznawacz()
plik = 'nagrywka.wav'
rec.nagraj()
rec.zapisz(plik)
odtworz(plik)
