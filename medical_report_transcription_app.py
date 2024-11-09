
# Requirements: Python, Streamlit, Whisper Model

# Step 1: Backend Implementation
# Install necessary libraries
# pip install streamlit openai pydub

import streamlit as st
import openai
from pydub import AudioSegment
import tempfile

# Streamlit UI - User Friendly Design
st.set_page_config(page_title="Medical Report Transcription", page_icon="📝", layout="centered")
st.title("📝 Medical Report Transcription")
st.markdown("Welcome to the **Medical Report Transcription** app! Easily convert your medical audio files into text with just a few clicks.")

# Add sidebar for better navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Use this menu to navigate through the app.")

# Input OpenAI API Key from user
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# File uploader or live recording
audio_file = st.file_uploader("📁 Upload an audio file for transcription (wav, mp3, m4a)", type=["wav", "mp3", "m4a"])
record_audio = st.button("🎙️ Record Audio Live")

if record_audio:
    st.warning("Live audio recording is not yet implemented. Please upload an audio file.")

report_type = st.selectbox("📝 Select the Report Type", ["USG", "X-Ray", "MRI", "CT Scan", "Other"])
user_id = st.text_input("👤 Enter Your User ID", placeholder="e.g., user123")

st.markdown("---")
st.info("✨ **Tip**: Upload a clear audio file for the best transcription results.")

if st.button("🚀 Start Transcription"):
    if api_key and audio_file is not None and user_id:
        openai.api_key = api_key  # Set API key provided by user
        with st.spinner("Transcribing... Please wait..."):
            try:
                # Convert audio file to compatible format for Whisper
                with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                    audio = AudioSegment.from_file(audio_file)
                    audio.export(temp_audio.name, format="wav")
                    temp_audio_path = temp_audio.name

                # Transcribe the audio file using Whisper
                with open(temp_audio_path, "rb") as audio_data:
                    transcription_result = openai.Audio.transcribe("whisper-1", audio_data)
                
                # Get the transcribed text
                transcript_text = transcription_result['text']

                # Customize output based on report type
                if report_type == "USG":
                    transcript_text = f"[Ultrasound Report]\n{transcript_text}"
                elif report_type == "X-Ray":
                    transcript_text = f"[X-Ray Report]\n{transcript_text}"
                elif report_type == "MRI":
                    transcript_text = f"[MRI Report]\n{transcript_text}"
                elif report_type == "CT Scan":
                    transcript_text = f"[CT Scan Report]\n{transcript_text}"
                else:
                    transcript_text = f"[General Report]\n{transcript_text}"
                
                st.success("✅ Transcription Successful!")
                st.text_area("📄 Transcription Result", transcript_text, height=200)
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter your API key, upload an audio file, and enter your User ID.")

# Footer with additional info
st.markdown("---")
st.markdown("👨‍⚕️ **Medical Report Transcription** - Making your medical documentation easier. Developed with ❤️ to help healthcare professionals.")

# Step 2: Hosting Options
# 1. Deploy Streamlit App using Streamlit Cloud
#    - Create an account on https://streamlit.io/cloud
#    - Push your code to a GitHub repository
#    - Connect your GitHub repository to Streamlit Cloud and deploy.
#    - Steps to deploy:
#      1. Go to Streamlit Cloud and create a new app.
#      2. Connect your GitHub repository.
#      3. Set the branch and path to your `app.py` file.
#      4. Click **Deploy** and wait for the deployment to complete.

# Notes:
# - Secure the Streamlit app before deploying to production.
