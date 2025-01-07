import streamlit as st
import pdfplumber

def read_text_file(file):
    return file.read().decode("utf-8")

def read_pdf_file(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

st.title("Загрузка текстового или PDF файла")

uploaded_file = st.file_uploader("Выберите файл", type=["txt", "pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        # Если файл текстовый
        content = read_text_file(uploaded_file)
        st.subheader("Содержимое текстового файла:")
    elif uploaded_file.type == "application/pdf":
        # Если файл PDF
        content = read_pdf_file(uploaded_file)
        st.subheader("Содержимое PDF файла:")
    else:
        st.error("Неподдерживаемый формат файла. Пожалуйста, загрузите текстовый или PDF файл.")