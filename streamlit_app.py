import streamlit as st
import requests
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- COLE A CHAVE NOVA AQUI ---
API_KEY = "AIzaSyCS_ZFNjJVsi0HBYmgsYscGzZcufSwEORY"

# A URL MAIS ATUALIZADA DO GOOGLE (Versão 1.5 Flash Latest)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("Sua pergunta:")

if arquivo_pdf and pergunta:
    with st.spinner("Lendo e analisando..."):
        try:
            reader = PdfReader(arquivo_pdf)
            texto = "\n".join([p.extract_text() for p in reader.pages[:15]])
            
            payload = {
                "contents": [{"parts": [{"text": f"Contexto: {texto[:20000]}\n\nPergunta: {pergunta}"}]}]
            }
            
            # Chamada direta com tratamento de erro detalhado
            response = requests.post(URL, json=payload)
            
            if response.status_code == 200:
                st.markdown("### 🤖 Resposta:")
                st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error(f"Erro {response.status_code}: O Google recusou a conexão.")
                st.info("DICA: Verifique se você colou a chave nova corretamente no código.")
        except Exception as e:
            st.error(f"Erro técnico: {e}")
