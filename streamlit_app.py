import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# 1. Tente com o Gemini Pro (O mais compatível)
API_KEY = "AIzaSyBUkswqJvINGeeXjWIOr8Kr1RXHG9jtIWg"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Suba o PDF", type="pdf")
pergunta = st.text_input("Sua pergunta:")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando..."):
        try:
            reader = PdfReader(arquivo_pdf)
            texto = ""
            for i in range(min(len(reader.pages), 20)):
                texto += reader.pages[i].extract_text() + "\n"
            
            payload = {
                "contents": [{"parts": [{"text": f"Contexto: {texto}\n\nPergunta: {pergunta}"}]}]
            }

            response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            
            if response.status_code == 200:
                st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                # Se o gemini-pro falhar, tentamos uma última vez com o flash (mas no v1)
                st.error(f"Erro: O Google não encontrou o modelo. Tente novamente em instantes.")
        except Exception as e:
            st.error(f"Erro técnico: {e}")
