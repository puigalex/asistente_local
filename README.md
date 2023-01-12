# Asistente Virtual Local 
Proyecto educativo ([Lista de reprodicción en Youtube](https://www.youtube.com/watch?v=SaoDps2QBsI&list=PLA050nq-BHwN5CJuPAsFkBTrW_4Xxso_4)) para poder correr un asistente virtual de manera local. Integra distintos modelos de machine learning para poder brindar distintas funcionalidades.

## Modelos utilizados
- [X] STT: Transcripción de audio a texto
- [ ] NER: Modelo para encontrar elementos clave en peticiones
- [ ] TTS: Conversión de audio a texto 
- [ ] Detección de objectos: Deteccion de personas y otros elementos de interés

## Hardware / software requerido
Dependiendo de las funcionalidades que se requieran. 

### Necesarias
- Computadora:
    - De preferencia con GPU NVIDIA
    - ARM o x86 
    - Microfono o webcam
    - Ubuntu
    - Docker
    - NVIDIA Container toolkit (para x86 con GPU)

### Opcionales (Funcionalidades que usaran esto aun no desarrolladas)
- Camaras USB o capaces de enviar comunicacion por RTSP
- Bocina 

## Correr el asistente
Para facilitar la configuracion de los ambientes se tiene dos contenedores de Docker distintos. Uno corre en maquinas con procesadores ARM con Ubuntu (Jetson Nano, Xavier u Orin). El otro corre en procesadores x86 (AMD / Intel)

Aqui hay una [guía para instalar/configurar Docker para ML](https://www.youtube.com/watch?v=keGTBSVoHeU)

### ARM

### x86

## Aportaciones
Este proyecto esta abierto a aportaciones asi que si quieres mejorar o agregar funcionalidades haz un pull request.

# To Do:
- [X] Detectar palabra clave para que el asistente sepa que se le esta hablando 
- [ ] Crear Dockerfile para no requerir pull
- [ ] API OpenAI GPT-3 (No es local, pero si uso sera limitado)
- [ ] Probar en Jetson Nano
- [X] Parametros dentro de YAML

