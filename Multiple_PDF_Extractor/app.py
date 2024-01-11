import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv() ## To see the environment variables i.e. variables in .env file
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_pdf_text(pdf_docs): # In This function we read the pdf and extract the all text 
    text="" # Extracted text is Stored in this variable
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000) # pdf will be divided into 10000 chunks or tokens and overlapping chunks are 1000
    chunks=text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks): # This function assigns a vector to words in a pdf file
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")#Embedding technique
    vector_store=FAISS.from_texts(text_chunks,embedding=embeddings)## Performing embedding on the pdf
    vector_store.save_local("faiss_index") # Storing Vectors in file faiss_index


def get_connversational_chain():
    prompt_template ="""
    Answers the question as detailed as possible from the provided Context , make sure to provide all the details,
    if the answer is not in provided context just say, "Answer is not in provided context", Don't provide the Wrong answers
    Context:\n{context}?\n
    Question:\n{question}\n

    Answer:"""

    model=ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)

    prompt=PromptTemplate(template=prompt_template,input_variables=["context", "question"])
    chain=load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain


def user_input(user_question):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index",embeddings) # here it reads the faiss_index file using embedding technique
    docs=new_db.similarity_search(user_question)

    chain = get_connversational_chain()

    response = chain(
        {"input_documents":docs,"question":user_question},
        return_only_outputs=True)
    print(response)
    st.write("Reply:",response["output_text"])

def main():
    st.set_page_config("Chat With Multiple PDF")
    st.header("Chat With Multiple PDF with Gemini 💁🏼‍♂️")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit button & Process",accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing....."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks=get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("DONE")


if __name__ == "__main__":
    main()