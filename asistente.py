import io
import os
import speech_recognition as sr
import whisper
from utils import write_file as wf


from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
import openai
import gtts


class Asistente:
    def __init__(self, model, record_timeout, phrase_timeout, energy_threshold, wake_word):
        self.temp_file = NamedTemporaryFile().name
        self.transcription = ['']
        self.audio_model = whisper.load_model(model)
        self.phrase_time = None
        self.last_sample = bytes()
        self.data_queue = Queue() 
        recorder = sr.Recognizer()
        recorder.energy_threshold = energy_threshold
        recorder.dynamic_energy_threshold = False
        openai.api_key = ""

    def listen(self):
        source = sr.Microphone(sample_rate=16000)
        with source:
            self.recorder.adjust_for_ambient_noise(source)

            def record_callback(_, audio:sr.AudioData) -> None:
                """
                Threaded callback function to recieve audio data when recordings finish.
                audio: An AudioData containing the recorded bytes.
                """
                # Grab the raw bytes and push it into the thread safe queue.
                data = audio.get_raw_data()
                self.data_queue.put(data)

        #Se deja el microfono escuchando con ayuda de speech_recognition
        self.recorder.listen_in_background(source, record_callback, phrase_time_limit=self.record_timeout)
        start = datetime.utcnow()
        while True:
            try:
                now = datetime.utcnow()
                if ((now - start).total_seconds()%18) == 0:
                    self.write_transcript()
                # Pull raw recorded audio from the queue.
                if not self.data_queue.empty():
                    phrase_complete = False
                    if phrase_time and now - phrase_time > timedelta(seconds=self.phrase_timeout):
                        last_sample = bytes()
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    phrase_time = now

                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        last_sample += data


                    audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
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
                        mensaje = "Human: " + mensaje
                        respuesta = self.call_gpt(mensaje)
                        print(respuesta)


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
        respuesta = openai.Completion.create(
            engine="ada",
            prompt=texto,
            temperature=0.9,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n", " Human:", " AI:"]
        )
        return respuesta["choices"][0]["text"]
    
    def tts(self, texto):
        # LLamada a la API de Google Text to Speech
        tts = gtts.gTTS(texto, lang='es')
        tts.save('audio.mp3')
    
    def play_audio(self, filename):
        # Abre el archivo de audio y lo reproduce
        os.system('mpg123 -q ' + filename)


        


