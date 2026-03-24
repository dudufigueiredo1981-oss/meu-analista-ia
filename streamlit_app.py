import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- COLOQUE A SUA CHAVE NOVA DO GOOGLE AI STUDIO AQUI ---
API_KEY = "AIzaSyBUkswqJvINGeeXjWIOr8Kr1RXHG9jtIWg"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber sobre o texto?")

if arquivo_pdf and pergunta:
    with st.spinner("Lendo e analisando o documento..."):
        try:
            # 1. Extração do texto (Primeiras 20 páginas para evitar lentidão)
            reader = PdfReader(arquivo_pdf)
            texto_extraido = ""
            for page in reader.pages[:20]:
                content = page.extract_text()
                if content:
                    texto_extraido += content + "\n"
            
            # 2. Definição do Pacote de Dados (O famoso 'payload')
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Contexto acadêmico:\n{texto_extraido}\n\nPergunta: {pergunta}"
                    }]
                }]
            }
            headers = {'Content-Type': 'application/json'}

            # 3. Tentativa 1: Modelo Gemini 1.5 Flash (Mais rápido)
            url_flash = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            response = requests.post(url_flash, headers=headers, json=payload)

            # 4. Verificação e Tentativa 2 (Se a 1 falhar)
            if response.status_code == 200:
                resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.markdown("### 🤖 Resposta:")
                st.write(resultado)
            else:
                # Tenta o modelo Gemini Pro caso o Flash dê erro 404
                url_pro = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
                response_pro = requests.post(url_pro, headers=headers, json=payload)
                
                if response_pro.status_code == 200:
                    resultado = response_pro.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown("### 🤖 Resposta (via Gemini Pro):")
                    st.write(resultado)
                else:
                    st.error(f"Erro do Google: {response_pro.status_code}. Verifique se sua chave API está correta.")

        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Versão Corrigida - Conexão Direta v1")
