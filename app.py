import streamlit as st
import pdfplumber
from nn import create_sum


def read_text_file(file):
    return file.read().decode("utf-8")


def read_pdf_file(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

st.session_state.show_button = False

st.title("Загрузка текстового или PDF файла")

uploaded_file = st.file_uploader("Выберите файл", type=["txt", "pdf"])
content = ""
summary = ""
if uploaded_file is not None:
    p = False
    if uploaded_file.type == "text/plain":
        p = True
        content = read_text_file(uploaded_file)
#        st.subheader("Содержимое текстового файла:")
#        st.text(content)
    elif uploaded_file.type == "application/pdf":
        p = True
        content = read_pdf_file(uploaded_file)
#        st.subheader("Содержимое PDF файла:")
#        st.text(content)
    else:
        st.error("Неподдерживаемый формат файла. Пожалуйста, загрузите текстовый или PDF файл.")
    
    if p:
        if st.button("summarize"):
            if summary == "":
                summary = create_sum(content)
            st.text(summary)


