import whisper
import recorder
import time 

model = whisper.load_model("tiny")
audio = recorder.Recorder()
start = time.time()
print("Inicia grabación ")
audio.record()
counter = 1 

while True:
    timestamp = time.time()
    if (timestamp-start)% 10 ==0:
        print("Nuevo timestamp")
        audio.save(str(counter))
        audio.record()
        result = model.transcribe("{}.wav".format(counter), verbose=None)
        print("Proceso el audio ", str(counter))
        with open("sample.txt", "a") as file_object:
            file_object.write("{}\n".format(result["text"]))
        counter += 1