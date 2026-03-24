import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Configuração da página
st.set_page_config(page_title="Analista de Discurso", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# Chave do Gemini
# Forçando a versão 1 (estável) da API
genai.configure(api_key="AIzaSyCBYDclNRVBWB9LzkFq0JLqtYn7mKafxJQ")

# Criando o modelo com a configuração de transporte correta
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
)
# Interface
arquivo = st.file_uploader("Suba o PDF do livro", type="pdf")
pergunta = st.text_input("O que você quer saber sobre o texto?")

if arquivo and pergunta:
    with st.spinner("Lendo e analisando..."):
        try:
            reader = PdfReader(arquivo)
            texto = ""
            for page in reader.pages[:40]: # Lendo as primeiras 40 páginas
                texto += page.extract_text() + "\n"
            
            prompt = f"Baseado no texto: {texto}\n\nPergunta: {pergunta}"
            response = model.generate_content(prompt)
            st.markdown("### Resposta:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Erro: {e}")
