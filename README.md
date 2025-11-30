# Python-RTT-TTS: Ollama Voice Interface

This project implements a fully functional, real-time voice assistant capable of processing user input in Romanian. It utilizes a local Large Language Model (LLM) served by Ollama for natural language processing and generates responses using Google Text-to-Speech (gTTS).

The system is designed for Linux environments, focusing on stability and utilizing robust audio libraries (`pydub`, `aplay`) to bypass common audio driver issues often encountered with real-time speech processing frameworks.

---

## 🚀 Features

- **Offline LLM Processing**
  Leverages a local Llama 3 model via Ollama for privacy and low-latency responses.

- **Real-Time ASR (Automatic Speech Recognition)**
  Uses `speech_recognition` and Google’s engine for accurate Romanian voice transcription.

- **Robust TTS Playback**
  Converts generated text into audio using gTTS and plays it back using `pydub` and the `aplay` utility.

- **Custom Persona Integration**
  Configurable via the `SYSTEM_PROMPT` variable.

---

## 📋 Prerequisites

### Software Requirements

- Ollama
- Python 3.8+
- Docker (recommended)
- FFmpeg
- alsa-utils

### System Dependencies Installation (Linux)

```bash
sudo apt update
sudo apt install ffmpeg
sudo apt install alsa-utils
```

---

## ⚙️ Setup Guide

### 4.1. Ollama and Model Deployment

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3:8b
```

---

## 4.2. Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install ollama SpeechRecognition gTTS pydub
```

---

## 4.3. Architecture Overview

Pipeline:
speech → ASR → LLM → TTS → WAV → aplay → cleanup

---

## 5. Usage

```bash
python assistant_vocal.py
```
---

## 6. Code Structure Overview

### generate_response(prompt)

- Sends text to Ollama.
- Handles persona.
- Guarantees non-empty return string.

### Main Execution Loop

- Captures audio via speech_recognition.
- Processes through LLM.
- Generates MP3 with gTTS.
- Converts MP3→WAV with pydub.
- Plays WAV via `aplay`.
- Removes temp files.

---