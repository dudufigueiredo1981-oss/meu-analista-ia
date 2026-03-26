import streamlit as st
import requests
from pypdf import PdfReader

st.set_page_config(page_title="Analista de Discurso IA", page_icon="📚")
st.title("📚 Analista de Discurso IA")

# --- COLE SUA CHAVE DO GROQ AQUI (Começa com gsk_) ---
GROQ_API_KEY = st.secrets["GROQ_KEY"]

arquivo_pdf = st.file_uploader("Escolha o livro (PDF)", type="pdf")
pergunta = st.text_input("O que deseja saber sobre o texto?")

if arquivo_pdf and pergunta:
    with st.spinner("Analisando com Llama 3 (Groq)..."):
        try:
            # 1. Extração de texto (Lendo 15 páginas)
            reader = PdfReader(arquivo_pdf)
            texto_base = ""
            for page in reader.pages[:15]:
                texto_base += page.extract_text() + "\n"
            
            # 2. Chamada para a API do Groq (Rápida e Estável)
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Você é um analista de discurso acadêmico especializado em Eni Orlandi."},
                    {"role": "user", "content": f"Baseado no texto: {texto_base[:25000]}\n\nPergunta: {pergunta}"}
                ]
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                resposta = response.json()['choices'][0]['message']['content']
                st.markdown("---")
                st.subheader("🤖 Análise da IA:")
                st.write(resposta)
            else:
                st.error(f"Erro no Groq: {response.status_code}. Verifique a chave.")
                
        except Exception as e:
            st.error(f"Erro técnico: {e}")

st.divider()
st.caption("Powered by Groq & Llama 3 - Estabilidade Total")
