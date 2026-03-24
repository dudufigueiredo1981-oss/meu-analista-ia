import streamlit as st
import requests
import json
from pypdf import PdfReader

# 1. Configuração da Página
st.set_page_config(page_title="Analista de Discurso IA", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# 2. Configuração da API (Caminho Direto v1 - SEM ERRO 404)
API_KEY = "AIzaSyCBYDclNRVBWB9LzkFq0JLqtYn7mKafxJQ"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# 3. Interface
arquivo_pdf = st.file_uploader("Escolha o livro (PDF)", type="pdf")
pergunta = st.text_input("O que deseja saber sobre este texto?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando o livro..."):
        try:
            # Lendo o PDF de forma simples
            reader = PdfReader(arquivo_pdf)
            texto_contexto = ""
            for i in range(min(len(reader.pages), 30)): # Primeiras 30 páginas
                texto_contexto += reader.pages[i].extract_text() + "\n"
            
            # Montando o pacote para o Google (JSON)
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Responda à pergunta baseando-se no texto abaixo:\n\nPERGUNTA: {pergunta}\n\nTEXTO:\n{texto_contexto}"
                    }]
                }]
            }

            # Enviando direto (Método REST)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(URL, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                res_json = response.json()
                resposta_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                st.markdown("### 🤖 Análise:")
                st.write(resposta_ia)
            else:
                st.error(f"Erro do Google ({response.status_code}): {response.text}")

        except Exception as e:
            st.error(f"Erro de processamento: {e}")

st.divider()
st.caption("Versão com Conexão Direta v1 - Estável")
            
