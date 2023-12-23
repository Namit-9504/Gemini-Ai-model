import streamlit as st
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model=genai.GenerativeModel('gemini-pro-vision')


def get_response(input,image):
    if input !='':
        responce=model.generate_content([input,image])
    else:
        responce=model.generate_content(image)
    return responce.text

st.set_page_config(page_title="Gemini pro vision demo")

st.header('Gemini LLM Application')
input = st.text_input("Input",key='input')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png","jpeg"])
image=''
if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about image")

if submit:
     responce = get_response(input,image)
     st.subheader('The responce from LLM model is ')
     st.write(responce)