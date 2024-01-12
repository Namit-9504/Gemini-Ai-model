import streamlit as st
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
import os
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


input_prompt="""
        You are an expert in calorie counter. you need to tell calories present in the food.
        analyze the image of the food and calculate calorie. 
        Also tell me the calories of the each item.Don't Skip any items in the image
        """


st.set_page_config(page_title="Health Management Application")

st.header("Health Management Application")
input = st.text_input("Input Prompt" , key='input')
uploaded_file = st.file_uploader("Choose an image of the food....",type=['jpg','png','jpeg'])
image =''


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)

submit=st.button("tell me about the your task")


if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_responce(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)