import google.generativeai as genai
import streamlit as st
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_responce(input):
    model = genai.GenerativeModel("gemini-pro")
    responce = model.generate_content(input)
    return responce.text

def input_pdf_info(uploaded_file):
    if uploaded_file is not None:
        reader=pdf.PdfReader(uploaded_file)
        page = reader.pages[0]
        info=page.extract_text()
        return info
    else: 
        raise FileNotFoundError("No File Uploaded ")
    

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}
Give Output In a Proper formate show the percentage match in bold make the response easy to read
in the output dont show the provided job description
"""

## streamlit app
st.set_page_config(page_title="ATS Resume EXpert")
st.title("Third Year Mini Project")
st.title("Application Tracking System") 
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_info(uploaded_file)
        response=get_gemini_responce(input_prompt)
        st.subheader(response)