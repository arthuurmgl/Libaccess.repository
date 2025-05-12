import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
import pyttsx3
import speech_recognition as sr
import os
import tempfile
import cv2
import numpy as np
import base64

st.set_page_config(
    page_title="LibAccess®",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS E CABEÇALHO

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: rgba(255, 255, 255, 0.9);
            background-blend-mode: lighten;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Cabeçalho personalizado
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">LibAccess<span class="registered">®</span></h1>
        <h2 class="subtitle">MÃOS QUE CONECTAM</h2>
        <div class="divider"></div>
    </div>
""", unsafe_allow_html=True)
############################
# Função para converter imagem para base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    

# Caminho para sua imagem (ajuste o nome do arquivo)
background_path = "C:/Users/thuur/Pictures/Camera Roll/Screenshots/Captura de tela 2025-05-11 033525.png"


# CSS para imagem de fundo
background_css = f"""
<style>
.stApp {{
    background-image: url(data:image/jpg;base64,{img_to_base64(background_path)});
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-blend-mode: overlay;
    background-color: rgba(255,255,255,0.85);
}}

/* Melhora a legibilidade do conteúdo */
.main .block-container {{
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
</style>
"""

# Aplica o CSS
st.markdown(background_css, unsafe_allow_html=True)


# CSS inline
st.markdown("""
    <style>
    .header-container {
        text-align: center;
        margin-bottom: 1.1rem;
        padding: 1.1rem;
        background: linear-gradient(135deg, #2A7F62 0%, #3AA682 100%);
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        color: white;
    }
    .main-title {
        font-size: 1.1rem ;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
        letter-spacing: 1.5px;
    }
    .registered {
        font-size: 1.5rem;
        vertical-align: super;
    }
    .subtitle {
        font-size: 1.8rem !;
        font-style: italic;
        font-weight: 400;
        margin-top: 0 !;
        color: #FFD166;
    }
    .divider {
        height: 4px;
        width: 100px;
        background: #FFD166;
        margin: 1rem auto;
        border-radius: 2px;
    }
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        margin-bottom: 5.5rem;
        border-left: 5px solid #2A7F62;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-title {
        color: #2A7F62;
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #2A7F62 0%, #3AA682 100%);
        color: black;
        border: none;
        border-radius: 8px;
        padding: 5px 28px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(42, 127, 98, 0.4);
    }
    .tab-content {
        min-height: 300px
        font-size: 1.1rem
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
 }
    </style>
""", unsafe_allow_html=True)

import streamlit as st

st.markdown("""
<style>
    /* Estilo para o item não marcado (Inform desenroluyendo) */
    .stCheckbox [data-baseweb="checkbox"]:not([aria-checked="true"]) + label {
        color: #FF5733;  /* Cor laranja/vermelho */
        font-weight: bold;
    }
    
    /* Estilo para o item marcado (Análisis de contacto) */
    .stCheckbox [data-baseweb="checkbox"][aria-checked="true"] + label {
        color: #33FF57;  /* Cor verde */
        font-weight: bold;
    }
</style>
            
""", unsafe_allow_html=True)

# --- FUNÇÕES PRINCIPAIS ---

#Processar pdf
def processar_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        st.session_state.pdf_path = tmp.name
    
    texto = ""
    with open(st.session_state.pdf_path, "rb") as arq:
        leitor = PdfReader(arq)  # Usando PyPDF2 aqui
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
    
    st.session_state.extracted_text = texto.strip()
    return texto

def texto_para_voz(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(texto)
    engine.runAndWait()

def exibir_libras(texto):
    LIBRAS_DIR = "C:/Users/thuur/Desktop/Projeto Libaccess/imagens_libras"
    texto = texto.upper()
    
    if not os.path.exists(LIBRAS_DIR):
        st.error(f"Pasta '{LIBRAS_DIR}' não encontrada!")
        return
    
    caracteres_validos = [c for c in texto if c.isalpha()]
    
    if not caracteres_validos:
        st.warning("Nenhum caractere válido encontrado para exibir em LIBRAS")
        return
    
    st.subheader("Representação em LIBRAS")
    cols_per_row = 6
    for i in range(0, len(caracteres_validos), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(caracteres_validos):
                letra = caracteres_validos[i + j]
                img_path = os.path.join(LIBRAS_DIR, f"{letra}.png")
                
                with cols[j]:
                    if os.path.exists(img_path):
                        try:
                            img = Image.open(img_path)
                            st.image(img, caption=letra, width=100)
                        except:
                            st.error(f"Erro ao carregar {letra}.png")
                    else:
                        st.error(f"Imagem para '{letra}' não encontrada")

def audio_para_texto():
    reconhecedor = sr.Recognizer()
    with st.spinner("Ouvindo... Fale agora (5 segundos)"):
        with sr.Microphone() as fonte:
            try:
                audio = reconhecedor.listen(fonte, timeout=5)
                texto = reconhecedor.recognize_google(audio, language="pt-BR")
                return texto.upper()
            except sr.WaitTimeoutError:
                st.error("Tempo esgotado. Nenhum áudio detectado.")
                return ""
            except sr.UnknownValueError:
                st.error("Não foi possível reconhecer o áudio")
                return ""
            except Exception as e:
                st.error(f"Erro: {str(e)}")
                return ""

# --- INTERFACE PRINCIPAL ---
# Inicialização de estado
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

# Aas principais
tab1, tab2, tab3 = st.tabs(["📚 PDF para LIBRAS", "🎤 Áudio para LIBRAS", "📷 Reconhecimento"])

with tab1:
    st.markdown('<div class="tab-content" style="font-size:70rem;">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Carregue um arquivo PDF", type=["pdf"])
        
    if uploaded_file:
        texto = processar_pdf(uploaded_file)
        
        with st.expander("Visualizar Texto Extraído"):
            st.text(texto)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Converter para Voz 🔊"):
                with st.spinner("Convertendo..."):
                    texto_para_voz(texto)
                st.success("Conversão concluída!")
        with col2:
            if st.button("Exibir em LIBRAS 🤟"):
                exibir_libras(texto)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content" style="font-size:74rem;">', unsafe_allow_html=True)
    if st.button("Iniciar Gravação 🎤"):
        texto = audio_para_texto()
        if texto:
            st.text_area("Texto Reconhecido", texto)
            exibir_libras(texto)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content" style="font-size:74rem;">', unsafe_allow_html=True)
    if st.checkbox("Mostrar demonstração"):
        st.image("https://via.placeholder.com/800x400?text=Webcam+Feed+Preview", use_column_width=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# Rodapé
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1.5rem; background: #2A7F62; color: white; border-radius: 12px;">
        <p style="margin: 0; font-size: 0.9rem;">LibAccess® - Sistema de Acessibilidade | Versão 2.0</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">© 2023 Todos os direitos reservados</p>
    </div>
""", unsafe_allow_html=True)