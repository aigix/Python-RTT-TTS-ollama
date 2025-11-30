# LIBS
import ollama
import speech_recognition as sr
import os
from gtts import gTTS
from pydub import AudioSegment

# CONSTS
MODEL_NAME = "llama3:8b" # your chosen model, e.g., "llama3:8b"
MP3_FILE = "response.mp3"
WAV_FILE = "response.wav"
EXIT_CMDS = ["stop", "exit", "quit", "done"]
# DESCRIBE YOUR ASSISTANT'S BEHAVIOR
SYSTEM_PROMPT = (
    "You are a helpful and concise voice assistant. Answer questions directly and naturally, "
    "using clear English. Keep responses short but informative."
)
# GENERATE RESPONSE FUNCTION
def generate_response(prompt):
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}, 
                {"role": "user", "content": prompt}
            ],
            options={}, 
            stream=False
        )
        # EXTRACT AND RETURN ANSWER
        answer = response['message']['content'].strip() 
        if not answer:
             return "I apologize, I could not generate a response. Please try again." 
        return answer
    except Exception as e:
        return f"System error: {e}"

if __name__ == "__main__":
    # INITIALIZE SPEECH RECOGNITION
    recognizer = sr.Recognizer()
    mic_source = sr.Microphone() 
    print(EXIT_CMDS, " - Available stop commands.")

    while True:
        try:
            with mic_source as source:
                print("\n Waiting for input...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)

            prompt = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"You said: **{prompt}**")
            
            if prompt in EXIT_CMDS:
                print("Voice assistant closed.")
                break 
                
            print("⏳ Generating response...")
            answer = generate_response(prompt)
            print(f"Response: {answer}")
            
            myobj = gTTS(text=answer, lang="en", slow=False) 
            myobj.save(MP3_FILE)
            
            sound = AudioSegment.from_mp3(MP3_FILE)
            sound.export(WAV_FILE, format="wav")
            os.system(f"aplay {WAV_FILE} > /dev/null 2>&1")
            
            if os.path.exists(MP3_FILE): os.remove(MP3_FILE)
            if os.path.exists(WAV_FILE): os.remove(WAV_FILE)
            
        except sr.UnknownValueError:
            print("Could not understand. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")