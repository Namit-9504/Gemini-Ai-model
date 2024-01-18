from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image 
import google.generativeai as  genai


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_responce(input,pdf_content,prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    responce = model.generate_content([input,pdf_content[0],prompt])
    return responce.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    ## Converting pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]


        ## Convert to bytes 

        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format="JPEG")
        image_byte_arr=image_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode() # encode to base64   
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")


## Streamlit App

st.set_page_config(page_title=("ATS Resume Expert"))
st.header("ATS Tracking System")
input_text = st.text_area("Job Description:",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDf)......",type=["pdf"])

if uploaded_file is not None:
    st.write("File Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improve My Skills")

submit3 = st.button("What are the KeyWords that Are Missing?")

submit4 = st.button("Percentage match ")

input_prompt1 = """
You are an experienced HR With Tech Experience in the field  of any one job role from Data Science , Full Stack Web Development,
Big Data Engineering, DEVOPS , Data Analyst. Your task is to improve review the provied resume against the job 
descrition for this profiles. 
Please Share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weakness of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """ 
You are an experienced HR With Tech Experience in the field  of any one job role from Data Science , Full Stack Web Development,
Big Data Engineering, DEVOPS , Data Analyst. 
Your Task is to provide Seek comprehensive advice and actionable strategies on skill development. 
Discuss methodologies, online courses, and practical approaches that individuals can employ to enhance their
skills across diverse domains. Provide insights into effective learning techniques and resources to facilitate 
continuous personal and professional growth.
"""

input_prompt3 = """
You are an experienced HR With Tech Experience in the field  of any one job role from Data Science , Full Stack Web Development,
Big Data Engineering, DEVOPS , Data Analyst..
Your Task is to provide missing information in the resume related to provided job description
Identify and elaborate on the missing keywords in the given context. 
Discuss the importance of these keywords and how their inclusion can enhance the understanding, relevance, 
and searchability of the content. Provide specific examples and insights into effective keyword selection 
strategies for improved communication and discoverability.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of  any one job role Data Science,Full Stack Web Development,
Big Data Engineering, DEVOPS , Data Analytics. and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        responce = get_gemini_responce(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(responce)
    else: 
        st.write("Please Upload The Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        responce = get_gemini_responce(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(responce)
    else: 
        st.write("Please Upload The Resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        responce = get_gemini_responce(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(responce)
    else: 
        st.write("Please Upload The Resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        responce = get_gemini_responce(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(responce)
    else: 
        st.write("Please Upload The Resume")
