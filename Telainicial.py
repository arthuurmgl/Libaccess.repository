import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
import speech_recognition as sr
import os
import tempfile
import cv2
import numpy as np
import base64
from gtts import gTTS 
from io import BytesIO



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
    background-color: linear-gradient(135deg, #0890BB 0%, #FC9900 100%);
}}


.main .block-container {{
    background-color: linear-gradient(135deg, #0890BB 0%, #FC9900 100%);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
</style>
"""

# Estilo CSS personalizado para o botão e biografia
st.markdown("""
<style>
    .biography {
        background-color: ##308C6A;
        padding: 20px;
        border-radius: 10px;
        margin-top: 10px;
        border-left: 5px solid #4e8cff;
    }
</style>
""", unsafe_allow_html=True)


# Botão expansível para a biografia
with st.expander("📖 Sobre o LibAccess - Objetivo do Projeto", expanded=False):
    st.markdown("""
    <div class="biography">
        <h3 style='color:#2c3e50;'>LibAccess - Democratizando o Acesso ao Conhecimento</h3>
        
         LibAccess é uma plataforma inovadora desenvolvida com o objetivo de: 
        
                🔓 Facilitar o acesso aberto a conteúdos acadêmicos e científicos 
                📚 Criar uma biblioteca digital colaborativa de recursos educacionais
                🌍 Promover a democratização do conhecimento em múltiplos idiomas
                🤝 Conectar pesquisadores, estudantes e entusiastas do aprendizado
        
        
        Nossa missão é remover barreiras ao conhecimento, utilizando tecnologia de ponta para:
        
        
                🧠 Organizar informações complexas de maneira acessível
                ⚡ Oferecer ferramentas de busca e análise inteligente
                📊 Visualizar dados acadêmicos de forma intuitiva
        
                
    </div>
    """, unsafe_allow_html=True)

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

# --- FUNÇÕES PRINCIPAIS ---

#Processar pdf
def processar_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        st.session_state.pdf_path = tmp.name
    
    texto = ""
    with open(st.session_state.pdf_path, "rb") as arq:
        leitor = PdfReader(arq)
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
    
    st.session_state.extracted_text = texto.strip()
    return texto

def texto_para_voz(texto, lang='pt'):
    try:
        tts = gTTS(text=texto, lang=lang, slow=False)
        
        # Salva em buffer de memória
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Reproduz no navegador
        st.audio(audio_buffer, format='audio/mp3')
        
        # Salva em arquivo temporário (opcional)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tts.save(tmp_audio.name)
            return tmp_audio.name
    
    except Exception as e:
        st.error(f"Erro na conversão para voz: {str(e)}")  
        return None

    if audio_file:
        with open(audio_file, "rb") as f:
         st.download_button("Baixar Audio", f, file_name="audio_libaccess.mp3") 

def exibir_libras(texto):
    LIBRAS_DIR = "C:/Users/thuur/Desktop/Projeto Libaccess/images_libras"
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
### Audio para libras
def audio_para_texto():
    #Captura áudio do microfone e converte para texto.
    r = sr.Recognizer()
    try:
        with sr.Microphone() as fonte:
            st.info("Fale agora... (gravando por 5 segundos)")
            audio = r.listen(fonte, timeout=5, phrase_time_limit=5)
            try:
                texto = r.recognize_google(audio, language="pt-BR")
                return texto.upper()  # Padroniza para maiúsculas
            except sr.UnknownValueError:
                st.error("Não foi possível entender o áudio")
                return None
            except sr.RequestError as e:
                st.error(f"Erro na API: {str(e)}")
                return None
    except Exception as e:
        st.error(f"Erro no microfone: {str(e)}")
        return None

def exibir_libras(texto):
    LIBRAS_DIR = "C:/Users/thuur/Desktop/Projeto Libaccess/imagens_libras2"
    
    # Verifica se a pasta existe
    if not os.path.exists(LIBRAS_DIR):
        st.error(f"Pasta não encontrada: {LIBRAS_DIR}")
        return
    
    # Filtra apenas letras (A-Z)
    texto = texto.upper()
    letras = [c for c in texto if c.isalpha()]
    
    if not letras:
        st.warning("Nenhuma letra válida encontrada")
        return
    
    # Exibe as imagens encontradas
    st.subheader("Sinais em LIBRAS")
    cols = st.columns(6)  # 6 colunas por linha
    
    for i, letra in enumerate(letras):
        img_path = os.path.join(LIBRAS_DIR, f"{letra}.png")
        
        with cols[i % 6]:
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    st.image(img, caption=letra, width=100)
                except Exception as e:
                    st.error(f"Erro ao abrir {letra}.png: {str(e)}")
            else:
                st.error(f"Arquivo não encontrado: {letra}.png")


# --- INTERFACE PRINCIPAL ---
# Inicialização de estado
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

#Área de tabs
tab1, tab2, tab3 = st.tabs([" PDF para LIBRAS", " Áudio para LIBRAS", " Reconhecimento"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
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

    st.markdown('</div>', unsafe_allow_html=True)


with tab2:    
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Botão de gravação
    if st.button("Iniciar Gravação 🎤", key="btn_gravar"):
        with st.spinner("Gravando... (5 segundos)"):
            texto = audio_para_texto()
            if texto:
                st.session_state['texto_audio'] = texto
    
    # Exibe o texto reconhecido (se existir)
    if 'texto_audio' in st.session_state:
        st.text_area("Texto Reconhecido", st.session_state.texto_audio, key="texto_reconhecido")
        
        # Botões de ação (só aparecem depois da gravação)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Exibir em LIBRAS 🤟", key="btn_libras"):
                st.session_state['mostrar_libras'] = True
        
        with col2:
            if st.button("Ouvir Áudio 🔊", key="btn_voz"):
                texto_para_voz(st.session_state.texto_audio)
    
    # Exibe as LIBRAS (se solicitado)
    if st.session_state.get('mostrar_libras', False) and 'texto_audio' in st.session_state:
        exibir_libras(st.session_state.texto_audio)
        st.session_state['mostrar_libras'] = False  

    
    st.markdown('</div>', unsafe_allow_html=True)

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