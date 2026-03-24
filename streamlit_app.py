import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso IA", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- SUA CHAVE API ---
API_KEY = "AIzaSyAyyPLimH1lXBQ6pexOlu_xLGiFAEna-uc"

try:
    genai.configure(api_key=API_KEY)
    # USANDO O MODELO 1.0 PRO (O mais estável contra erro 404)
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    st.error(f"Erro na configuração: {e}")

arquivo_pdf = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que deseja saber?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando com o modelo estável..."):
        try:
            reader = PdfReader(arquivo_pdf)
            texto = ""
            for page in reader.pages[:15]:
                texto += page.extract_text() + "\n"
            
            # Gerando a resposta
            response = model.generate_content(f"Baseado no texto: {texto[:20000]}\n\nPergunta: {pergunta}")
            
            st.markdown("---")
            st.subheader("🤖 Resposta:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Erro: {e}")
            st.info("DICA: Vá no AI Studio e gere uma chave nova clicando em 'Create API key in NEW project'.")

st.divider()
st.caption("Versão Estável 1.0 Pro - Anti-404")
