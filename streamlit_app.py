import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. Configuração Visual
st.set_page_config(page_title="Analista de Discurso IA", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# 2. Configuração da API (AQUI ESTÁ O SEGREDO)
# Substitua pela sua chave MAIS RECENTE do AI Studio
API_KEY = "AIzaSyAyyPLimH1lXBQ6pexOlu_xLGiFAEna-uc"

genai.configure(api_key=API_KEY)

# 3. Interface de Usuário
arquivo_pdf = st.file_uploader("Escolha o PDF (Eni Orlandi)", type="pdf")
pergunta = st.text_input("O que deseja saber sobre o texto?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando o livro..."):
        try:
            # Lendo o PDF
            reader = PdfReader(arquivo_pdf)
            texto_completo = ""
            for i in range(min(len(reader.pages), 20)):
                page_text = reader.pages[i].extract_text()
                if page_text:
                    texto_completo += page_text + "\n"
            
            # CHAMADA OFICIAL (O modelo 'gemini-1.5-flash' é o mais estável hoje)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Criando o prompt
            prompt_final = f"Baseado no texto abaixo, responda: {pergunta}\n\nTEXTO:\n{texto_completo[:30000]}"
            
            # Gerando a resposta
            response = model.generate_content(prompt_final)
            
            st.markdown("---")
            st.subheader("🤖 Análise da IA:")
            st.write(response.text)
            
        except Exception as e:
            # Se der erro de "model not found", tentamos o modelo antigo automaticamente
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response_alt = model_alt.generate_content(prompt_final)
                st.write(response_alt.text)
            except:
                st.error(f"Erro técnico: {e}")
                st.info("Verifique se a API Key no código é a mesma do seu AI Studio.")

st.divider()
st.caption("Desenvolvido para análise acadêmica via Google Gemini.")
