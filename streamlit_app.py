import streamlit as st
import requests
import json
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso IA", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- SUA CHAVE API (A QUE VOCÊ CRIOU NO AI STUDIO) ---
API_KEY = "AIzaSyDTmogNg2PkpOQ68fUhvKXcpVudMwa3l3Y"

# A URL MAIS RESILIENTE DO GOOGLE (Versão 1.5 Flash - Caminho de Produção)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Escolha o livro (PDF)", type="pdf")
pergunta = st.text_input("O que deseja saber sobre o texto?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando com a URL de Contingência..."):
        try:
            # 1. Extração de texto (Apenas 5 páginas para garantir que não trave)
            reader = PdfReader(arquivo_pdf)
            texto_extraido = ""
            for page in reader.pages[:5]:
                content = page.extract_text()
                if content:
                    texto_extraido += content + " "
            
            # 2. Limpeza Radical (Remove caracteres que bugam a API)
            texto_limpo = " ".join(texto_extraido.split())
            
            # 3. Montagem do Pedido
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Responda à pergunta baseando-se no texto:\n\nTEXTO: {texto_limpo[:10000]}\n\nPERGUNTA: {pergunta}"
                    }]
                }]
            }
            
            # 4. Envio Direto (Usando o método POST puro)
            response = requests.post(URL, json=payload, headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                res_data = response.json()
                st.markdown("---")
                st.subheader("🤖 Resposta:")
                st.write(res_data['candidates'][0]['content']['parts'][0]['text'])
            else:
                # SE DER 404 AQUI, É PORQUE A CHAVE ESTÁ INVÁLIDA
                st.error(f"Erro do Google ({response.status_code}): O modelo não foi encontrado na sua conta.")
                st.info("Dudu, se der 404 agora, crie uma chave em outro Gmail. Às vezes o Google bloqueia um e-mail específico.")

        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Versão de Emergência - Analista de Discurso")
