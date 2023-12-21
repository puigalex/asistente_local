FROM nvcr.io/nvidia/l4t-pytorch:r35.1.0-pth1.13-py3
LABEL maintainer="Carlos Ruiz <karlosarr[at]protonmail.com>"
ARG DEBIAN_FRONTEND=noninteractive
RUN whoami
RUN apt-get update && \
 apt-get --no-install-recommends install -y ffmpeg \
 libgtk2.0-0 libgtk2.0-common libportaudio2 \
 libportaudiocpp0 portaudio19-dev python3-pyaudio && \
 apt-get clean
RUN pip3 install git+https://github.com/openai/whisper.git 
RUN pip3 install sounddevice
RUN pip3 install scipy
RUN pip3 install typing-extensions --upgrade
RUN mkdir -p /VA
WORKDIR /VA
COPY ./utils /VA/utils
COPY ./asistente.py /VA/asistente.py
COPY ./config.yaml /VA/config.yaml
COPY ./main.py /VA/main.py
COPY ./requirements.txt /VA/requirements.txt
RUN pip3 install -r ./requirements.txt
CMD python3 ./main.py
