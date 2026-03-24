import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso IA", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- SUA CHAVE API ---
API_KEY = "AIzaSyAzj_xPuSAY7kLJQf5ej6qhF3_zs0XGRzQ"

# A URL QUE NÃO DÁ 404 (Versão 1 Direta)
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando o livro..."):
        try:
            # 1. Extração Simples (15 páginas)
            reader = PdfReader(arquivo_pdf)
            texto = ""
            for i in range(min(len(reader.pages), 15)):
                texto += reader.pages[i].extract_text() + "\n"
            
            # 2. Pacote de dados para o Google
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Responda à pergunta baseando-se no texto abaixo:\n\nTEXTO:\n{texto[:20000]}\n\nPERGUNTA: {pergunta}"
                    }]
                }]
            }
            
            # 3. Envio Manual (Sem usar a biblioteca genai que dá erro)
            response = requests.post(URL, json=payload, headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                res_json = response.json()
                # Exibindo a resposta
                st.markdown("---")
                st.subheader("🤖 Resposta:")
                st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
            else:
                # Se o Flash der 404, tentamos o Pro na mesma URL
                URL_PRO = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
                response_pro = requests.post(URL_PRO, json=payload)
                
                if response_pro.status_code == 200:
                    st.write(response_pro.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Erro {response.status_code}: O Google ainda não liberou o modelo para sua chave.")
                    st.info("Tente gerar uma chave em 'Create API Key in NEW PROJECT' no AI Studio.")

        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Conexão Direta v1 - Estável")
