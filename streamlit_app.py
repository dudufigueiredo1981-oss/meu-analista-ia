import streamlit as st
import requests
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- COLE A CHAVE DO 'NEW PROJECT' AQUI ---
API_KEY = "AIzaSyDTmogNg2PkpOQ68fUhvKXcpVudMwa3l3Y"

# A URL CORINGA (Versão 1.5 Flash - Versão de Produção)
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("Sua pergunta:")

if arquivo_pdf and pergunta:
    with st.spinner("Conectando ao cérebro da IA..."):
        try:
            reader = PdfReader(arquivo_pdf)
            # Pegando só as 5 primeiras páginas para o teste ser infalível
            texto = ""
            for i in range(min(len(reader.pages), 5)):
                texto += reader.pages[i].extract_text() + "\n"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Contexto acadêmico: {texto[:10000]}\n\nPergunta: {pergunta}"}]
                }]
            }
            
            # Chamada direta
            response = requests.post(URL, json=payload, headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                res_data = response.json()
                st.markdown("### 🤖 Análise:")
                st.write(res_data['candidates'][0]['content']['parts'][0]['text'])
            else:
                # SE DER 404 DE NOVO, O GOOGLE EXIGE O CAMINHO v1beta COM O NOME ANTIGO
                URL_BETA = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
                res_beta = requests.post(URL_BETA, json=payload)
                
                if res_beta.status_code == 200:
                    st.write(res_beta.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Erro {response.status_code}: O Google ainda não ativou sua chave no servidor.")
                    st.info("Aguarde 5 minutos. Às vezes a chave nova demora para 'propagar' no sistema do Google.")

        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Conexão Direta v1/v1beta - Estabilizada")
