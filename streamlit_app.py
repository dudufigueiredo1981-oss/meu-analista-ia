import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- SUA CHAVE API ---
API_KEY = "AIzaSyAhsflXcYb6Mjxk715RoU6Llx8pWYB_lkE"

# A URL QUE SEMPRE FUNCIONA NO AI STUDIO (v1beta + gemini-1.5-flash)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Consultando o Gemini..."):
        try:
            reader = PdfReader(arquivo_pdf)
            texto = ""
            # Pegando só as 10 primeiras páginas para o primeiro teste ser rápido
            for page in reader.pages[:10]:
                texto += page.extract_text() + " "
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Contexto: {texto[:15000]}\n\nPergunta: {pergunta}"}]
                }]
            }
            
            response = requests.post(URL, json=payload)
            
            if response.status_code == 200:
                res_json = response.json()
                st.markdown("### 🤖 Resposta:")
                st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error(f"Erro {response.status_code}: O Google ainda não reconheceu o modelo.")
                st.info("DICA: Gere uma NOVA CHAVE no AI Studio e cole aqui.")

        except Exception as e:
            st.error(f"Erro técnico: {e}")
