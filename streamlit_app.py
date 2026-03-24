import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista Acadêmico", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- SUA CHAVE NOVA AQUI ---
API_KEY = "AIzaSyBUkswqJvINGeeXjWIOr8Kr1RXHG9jtIWg"

def chamar_google_direto(texto, pergunta):
    # A URL EXATA QUE O GOOGLE EXIGE NA VERSÃO V1 (Sem o erro 404)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Responda à pergunta baseando-se no texto abaixo:\n\nTEXTO:\n{texto}\n\nPERGUNTA: {pergunta}"
            }]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    return requests.post(url, headers=headers, json=payload)

arquivo_pdf = st.file_uploader("Suba o PDF", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando..."):
        try:
            reader = PdfReader(arquivo_pdf)
            # Pegando apenas as primeiras 15 páginas para ser instantâneo
            texto_contexto = "\n".join([p.extract_text() for p in reader.pages[:15]])
            
            response = chamar_google_direto(texto_contexto, pergunta)
            
            if response.status_code == 200:
                res_json = response.json()
                st.markdown("### 🤖 Resposta:")
                st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
            else:
                # Se ainda der 404, tentamos o modelo 'gemini-pro' (versão clássica)
                url_alt = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
                res_alt = requests.post(url_alt, headers={'Content-Type': 'application/json'}, json=payload)
                
                if res_alt.status_code == 200:
                    st.write(res_alt.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Erro persistente do Google: {response.status_code}. Verifique se sua chave está ativa no AI Studio.")
        except Exception as e:
            st.error(f"Erro técnico: {e}")
