import base64

import streamlit as st
import torch
import soundfile as sf
from kokoro import KPipeline


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
        bin_str = get_base64_of_bin_file(png_file)
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed; /* Optional: keeps background fixed on scroll */
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)

@st.cache_resource
def load_pipeline():
    return KPipeline(lang_code='a')  # change lang if needed

pipeline = load_pipeline()

image_path = "bg.jpg"
set_png_as_page_bg(image_path)

st.title("Text to Voice Bot")


text = st.text_area("Enter text to convert into speech:", "")
voice = st.selectbox("Choose a voice", ["af_bella", "af_nicole", "am_adam", "bf_alice", "bm_george", "bm_lewis"])

if st.button("🔊 Generate Voice"):
    if text.strip():
        generator = pipeline(text, voice=voice, speed=1.0)
        audio_path = "output.wav"

        with sf.SoundFile(audio_path, "w", samplerate=24000, channels=1) as f:
            for _, _, audio in generator:
                f.write(audio)

        st.audio(audio_path, format="audio/wav")
        with open(audio_path, "rb") as audio_file:
            st.download_button(
                label="⬇️ Download Audio",
                data=audio_file,
                file_name="output.wav",
                mime="audio/wav"
            )
        st.success("✅ Voice generated successfully!")
    else:
        st.warning("⚠️ Please enter some text.")