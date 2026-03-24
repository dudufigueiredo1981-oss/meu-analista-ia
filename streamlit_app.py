import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- SUA CHAVE API ---
API_KEY = "AIzaSyDlmVy73h2AwVorUWpvebB8-G2KYiL7xHY"

# ENDEREÇO UNIVERSAL (O único que não dá 404 no v1)
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Consultando a Base de Dados do Google..."):
        try:
            # 1. Extração Simples
            reader = PdfReader(arquivo_pdf)
            texto_bruto = ""
            for page in reader.pages[:10]: # Apenas 10 páginas para garantir sucesso total
                texto_bruto += page.extract_text() + " "
            
            # 2. Limpeza de Segurança
            texto_limpo = " ".join(texto_bruto.split())
            
            # 3. Formatação do Pedido (Exatamente como o Google quer)
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Baseado no texto: {texto_limpo[:20000]}\n\nPergunta: {pergunta}"
                    }]
                }]
            }
            
            # 4. Envio Direto
            response = requests.post(URL, json=payload)
            
            if response.status_code == 200:
                res_json = response.json()
                # Pegando a resposta dentro da estrutura do Google
                resposta = res_json['candidates'][0]['content']['parts'][0]['text']
                st.markdown("### 🤖 Resposta:")
                st.write(resposta)
            else:
                st.error(f"Erro do Google: {response.status_code}. Tente trocar o modelo para gemini-1.0-pro no link.")
                st.info(f"Detalhe do Servidor: {response.text}")

        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Conexão Estável v1 via Gemini-Pro")
