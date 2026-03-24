import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista Acadêmico", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- COLOQUE A CHAVE QUE VOCÊ ACABOU DE CRIAR AQUI ---
API_KEY = "AIzaSyBUkswqJvINGeeXjWIOr8Kr1RXHG9jtIWg"

def chamar_google(texto, pergunta, modelo):
    url = f"https://generativelanguage.googleapis.com/v1/models/{modelo}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Contexto: {texto}\n\nPergunta: {pergunta}"}]}]}
    headers = {'Content-Type': 'application/json'}
    return requests.post(url, headers=headers, data=json.dumps(payload))

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando com a chave nova..."):
        try:
            reader = PdfReader(arquivo_pdf)
            texto = "\n".join([p.extract_text() for p in reader.pages[:30]])
            
            # Tenta o modelo Flash primeiro
            res = chamar_google(texto, pergunta, "gemini-1.5-flash")
            
            # Se der erro, tenta o Pro
            if res.status_code != 200:
                res = chamar_google(texto, pergunta, "gemini-pro")
            
            if res.status_code == 200:
                st.write(res.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error(f"Erro: A chave nova ainda não ativou ou o modelo está instável. Código: {res.status_code}")
        except Exception as e:
            st.error(f"Erro técnico: {e}")
