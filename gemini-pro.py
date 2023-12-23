import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

### function to load Gemini pro model and get response
model=genai.GenerativeModel('gemini-pro')

def get_response(input_text):
    responce=model.generate_content(input_text)
    return responce.text

st.set_page_config(page_title="Q&A Demo")
st.header('Gemini LLM Application')

input = st.text_input("Input",key='input')
submit=st.button("Ask the Question")

if submit:
    responce = get_response(input)
    st.subheader('This is the answer')
    st.write(responce)

