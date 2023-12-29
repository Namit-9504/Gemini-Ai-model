from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_responce(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input = st.text_input("Input Prompt" , key='input')
uploaded_file = st.file_uploader("Choose an image of the invoice....",type=['jpg','png','jpeg'])
image =''


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)

submit=st.button("tell me about the invoice")

input_prompt="""
you are an expert in understanding invoices. We will Upload a image as invoice
and you will have to answer any question based on the uploaded invoice image.
"""

# after clicking submit

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_responce(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)