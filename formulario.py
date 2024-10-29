import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente
load_dotenv()

# Configurar a API do Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Criar o modelo de conversa
model = genai.GenerativeModel('gemini-pro')

st.title("Chatbot para Geração de Vídeo Marketing")

# Dados iniciais do vídeo
with st.form("DadosIniciais"):
    campanha = st.selectbox("Selecione o tipo de campanha", ("Engajamento", "Venda/Cadastro"))
    conteudo = st.selectbox("Selecione o tipo de conteúdo", ("Depoimentos", "Storytelling", "Educativo"))
    estadoCliente = st.selectbox("Selecione a condição do cliente", ("Caótico", "Apertado", "Escravo do Negócio", "Iniciante"))
    duracaoVideo = st.text_input("Duração do vídeo")
    assunto = st.text_area("Assunto do vídeo")

    submitted = st.form_submit_button("Gerar Roteiro")
    if submitted:
        prompt = (
            f"Preciso criar um script para um vídeo onde o assunto será {assunto} "
            f"voltado para uma campanha de {campanha} do tipo {conteudo} "
            f"para clientes em que o estado do cliente é {estadoCliente}. "
            f"O script será lido e deve ter duração de {duracaoVideo}. "
            f"O conteúdo gerado, será usado para criação de um vídeo marketing, onde uma pessoa irá fazer a leitura do conteúdo."
        )
        response = model.generate_content(prompt)
        st.session_state.texto_gerado = response.text
        st.write("Conteúdo gerado:")
        texto_antigo = response.text
        st.text_area("Conteúdo Gerado:", value=texto_antigo, height=200)

# Interface de chat para ajustes do texto gerado
st.subheader("Ajuste o Texto Gerado")
if 'novo_texto' not in st.session_state:
    st.session_state.novo_texto = ""

novo_texto = st.text_area("Novo Texto:", value=st.session_state.novo_texto, height=200)

if st.button("Solicitar Ajuste"):
    # Envia o novo texto como prompt para a LLM gerar o ajuste
    ajuste_prompt = f"Ajuste o seguinte texto {st.session_state.texto_gerado} conforme modificações solicitadas em {novo_texto}"
    response = model.generate_content(ajuste_prompt)
    st.session_state.texto_gerado = response.text
    
    st.write("Texto ajustado:")
    st.text_area("Texto Gerado:", value=st.session_state.texto_gerado, height=200)
