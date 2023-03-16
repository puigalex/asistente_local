import io
import os
import speech_recognition as sr
import whisper
from utils import write_file as wf
import time
import subprocess

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
import openai
import gtts
openai.api_key = ""
import pygame

class Asistente:
    def __init__(self, model, record_timeout, phrase_timeout, energy_threshold, wake_word):
        self.temp_file = NamedTemporaryFile().name
        self.transcription = ['']
        self.audio_model = whisper.load_model(model)
        self.phrase_time = None
        self.last_sample = bytes()
        self.data_queue = Queue() 
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_threshold
        self.recorder.dynamic_energy_threshold = False
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.wake_word = wake_word


    def listen(self):
        self.source = sr.Microphone(sample_rate=16000)
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

            def record_callback(_, audio:sr.AudioData) -> None:
                """
                Threaded callback function to recieve audio data when recordings finish.
                audio: An AudioData containing the recorded bytes.
                """
                # Grab the raw bytes and push it into the thread safe queue.
                data = audio.get_raw_data()
                self.data_queue.put(data)

        #Se deja el microfono escuchando con ayuda de speech_recognition
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)
        start = datetime.utcnow()
        while True:
            try:
                now = datetime.utcnow()
                if ((now - start).total_seconds()%18) == 0:
                    self.write_transcript()
                # Pull raw recorded audio from the queue.
                if not self.data_queue.empty():
                    phrase_complete = False
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        self.last_sample = bytes()
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    self.phrase_time = now

                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        self.last_sample += data


                    audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data.read())

                    result = self.audio_model.transcribe(self.temp_file, language='es')
                    text = result['text'].strip()

                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    
                    if self.wake_word in self.transcription[-1].lower():
                        # Se activo el asistente
                        mensaje = self.transcription[-1].lower().replace(self.wake_word, "")
                        mensaje = "Humano: " + mensaje
                        respuesta = self.call_gpt(mensaje)
                        print(respuesta)
                        self.tts(respuesta)
                        self.play_audio_pygame("audio.mp3")


                    # os.system('cls' if os.name=='nt' else 'clear')
                    # for line in self.transcription:
                    #     print(line)
                    # # Flush stdout.
                    # print('', end='', flush=True)
                    # sleep(0.25)
            except KeyboardInterrupt:
                break


    
    def write_transcript(self):
        print("\n\nTranscripcion:")
        for line in self.transcription:
            print(line)
            wf(line, "transcript", "txt")

    def call_gpt(self, texto):
        # LLamada a GPT3 enviando la ultima oracion transcrita

        print("Comunidando con openai", texto)
        respuesta = openai.Completion.create(
            engine="text-davinci-002",
            prompt=texto,
            temperature=0.5,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
            #stop=["\n", " Humano:", " Inteligencia Artificial:"]
        )
        print("La respuesta fue: ", respuesta["choices"][0]["text"])
        return respuesta["choices"][0]["text"]
    
    def tts(self, texto):
        # LLamada a la API de Google Text to Speech
        tts = gtts.gTTS(texto, lang='es')
        tts.save('audio.mp3')
    
    def play_audio(self, filename):
        # Abre el archivo de audio y lo reproduce
        os.system("mpg123 " + filename)
    
    def play_audio_pygame(self, filename):
        # Abre el archivo de audio y lo reproduce con pygame
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            pygame.time.Clock().tick(10)
    
