from google import genai
from dotenv import load_dotenv
import os, io
from gtts import gTTS
import streamlit as st
import gtts

# loading the environment variable
load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")
# initailizing a client
client = genai.Client(api_key= my_api_key)
# note generator 
def note_generator(images):
    prompt = """Summarize the pictures in note format at max 100 words, 
    make sure to add necessary markdown to 
    differenciate different section"""

    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[images, prompt])
    
    return response.text
# audio generator
def audio_transcription(text):
    speech = gtts.gTTS(text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer

# quiz generator
def quiz_generator(image, difficulty):
    prompt = f"""Generate 5 quizes based on the {difficulty}.
    Generate a multiple-choice quiz.write answer below after each question and options completed.
    make sure to add markdown to differentiate the options """

    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[image, prompt])
        
    return response.text