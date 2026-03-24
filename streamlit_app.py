import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- COLOQUE SUA CHAVE AQUI ---
API_KEY = "AIzaSyDlmVy73h2AwVorUWpvebB8-G2KYiL7xHY"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Limpando texto e consultando o Gemini..."):
        try:
            # 1. Extração Limpa
            reader = PdfReader(arquivo_pdf)
            texto_sujo = ""
            # Vamos pegar apenas as 15 primeiras páginas para garantir que o 400 suma
            for page in reader.pages[:15]:
                texto_sujo += page.extract_text() + " "
            
            # Limpeza de caracteres que causam erro 400
            texto_limpo = " ".join(texto_sujo.split()) # Remove quebras de linha duplas e espaços malucos
            
            # 2. Montagem do JSON (Payload)
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Responda de forma acadêmica.\n\nCONTEXTO:\n{texto_limpo[:30000]}\n\nPERGUNTA: {pergunta}"
                    }]
                }]
            }
            
            # 3. Chamada v1 Estável
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                res_json = response.json()
                st.markdown("### 🤖 Resposta:")
                st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error(f"Erro do Google: {response.status_code}. Detalhe: {response.text}")

        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Versão 'Vácuo' - Limpeza de Caracteres Ativada")
