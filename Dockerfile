FROM nvcr.io/nvidia/l4t-pytorch:r35.1.0-pth1.13-py3
RUN apt update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -qq ffmpeg \
 libgtk2.0-0 libgtk2.0-common libportaudio2 \
 libportaudiocpp0 portaudio19-dev python3-pyaudio
RUN pip3 install git+https://github.com/openai/whisper.git 
RUN pip3 install sounddevice
RUN pip3 install scipy
RUN pip3 install typing-extensions --upgrade
RUN mkdir -p /VA
WORKDIR /VA
COPY . /VA
RUN pip3 install -r ./requirements.txt
CMD python3 ./main.py
