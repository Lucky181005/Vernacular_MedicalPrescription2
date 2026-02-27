import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_TEST"))

st.title("AI Hackathon Project 🚀")

user_input = st.text_area("Enter your input")

if st.button("Generate"):
    if user_input:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )
        st.write(response.text)
    else:
        st.warning("Please enter some input.")