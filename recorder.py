import sounddevice as sd
from scipy.io.wavfile import write
import time

class Recorder:
    def __init__(self):
        self.fs = 44100
        self.seconds = 10

    def record(self):
        self.recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=1)

    def save(self, filename="timestamp"):
        self.filename = filename
        write("{}.wav".format(filename), self.fs, self.recording)
