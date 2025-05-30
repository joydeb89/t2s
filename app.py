import streamlit as st
import requests
import os
from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Multilingual Text to Speech", page_icon="🎙️")
st.title("🎙️ Multilingual Text to Speech")
st.write("Write your text in Bengali, English, or Hindi and listen/download the audio.")

# Language selection
language_option = st.selectbox("Choose Language / ভাষা নির্বাচন করুন / भाषा चुनें", 
                               options=["Bengali", "English", "Hindi"])

# Language code mapping for gTTS
language_map = {
    "Bengali": "bn",
    "English": "en",
    "Hindi": "hi"
}
selected_lang_code = language_map[language_option]

# Multilingual placeholder
placeholder_text = {
    "Bengali": "এখানে বাংলা লিখুন...",
    "English": "Type your English text here...",
    "Hindi": "यहाँ हिंदी में लिखें..."
}

# Text area for input
text = st.text_area(f"{language_option} Text", 
                    placeholder=placeholder_text[language_option], 
                    height=150)

# Generation Info from DesiVocal
if st.button("🎤 View Generation Info"):
    api_key = os.getenv("X_API_KEY")
    if not api_key:
        st.error("API key not found. Please set X_API_KEY in .env file.")
    else:
        try:
            url = "https://prod-api2.desivocal.com/dv/api/v0/tts_api/generation_info"
            headers = {"X_API_KEY": api_key}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                st.success("✅ Generation Info:")
                st.code(response.text)
            else:
                st.error(f"⚠️ Failed to fetch info. Status: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"Request failed: {e}")

# TTS playback and download
col1, col2 = st.columns(2)

with col1:
    if st.button("🎧 Play"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Generating audio..."):
                try:
                    tts = gTTS(text=text, lang=selected_lang_code)
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)

                    st.audio(mp3_fp, format="audio/mp3")

                    st.download_button(
                        label="⬇️ Download",
                        data=mp3_fp,
                        file_name=f"{language_option.lower()}_speech.mp3",
                        mime="audio/mp3"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
