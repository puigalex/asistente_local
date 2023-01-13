import io
import os
import speech_recognition as sr
import whisper
from utils import write_file as wf


from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep


class Asistente:
    def __init__(self, model, record_timeout, phrase_timeout, energy_threshold, wake_word):
        temp_file = NamedTemporaryFile().name
        self.transcription = ['']
        audio_model = whisper.load_model(model)

        phrase_time = None
        last_sample = bytes()
        data_queue = Queue()

        # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
        recorder = sr.Recognizer()
        recorder.energy_threshold = energy_threshold
        recorder.dynamic_energy_threshold = False

        source = sr.Microphone(sample_rate=16000)
        with source:
            recorder.adjust_for_ambient_noise(source)

            def record_callback(_, audio:sr.AudioData) -> None:
                """
                Threaded callback function to recieve audio data when recordings finish.
                audio: An AudioData containing the recorded bytes.
                """
                # Grab the raw bytes and push it into the thread safe queue.
                data = audio.get_raw_data()
                data_queue.put(data)

        #Se deja el microfono escuchando con ayuda de speech_recognition
        recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)
        start = datetime.utcnow()
        while True:
            try:
                now = datetime.utcnow()
                if ((now - start).total_seconds()%18) == 0:
                    self.write_transcript()
                # Pull raw recorded audio from the queue.
                if not data_queue.empty():
                    phrase_complete = False
                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        last_sample = bytes()
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    phrase_time = now

                    while not data_queue.empty():
                        data = data_queue.get()
                        last_sample += data


                    audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    with open(temp_file, 'w+b') as f:
                        f.write(wav_data.read())

                    result = audio_model.transcribe(temp_file, language='es')
                    text = result['text'].strip()

                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    
                    if wake_word in self.transcription[-1].lower():
                        print("Hola")
                        # Aqui se integraran los llamados a las acciones que podra hacer el asistente

                    os.system('cls' if os.name=='nt' else 'clear')
                    for line in self.transcription:
                        print(line)
                    # Flush stdout.
                    print('', end='', flush=True)
                    sleep(0.25)
            except KeyboardInterrupt:
                break


    
    def write_transcript(self):
        print("\n\nTranscripcion:")
        for line in self.transcription:
            print(line)
            wf(line, "transcript", "txt")