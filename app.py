import streamlit as st  # Importa a biblioteca Streamlit para criar interfaces web interativas
import os  # Importa o módulo os para interagir com o sistema operacional (criar diretórios, etc.)
from gtts import gTTS  # Importa Google Text-to-Speech para converter texto em fala
from pydub import AudioSegment  # Importa o módulo para manipulação de arquivos de áudio
import base64  # Importa o módulo para codificação/decodificação em base64 (usado para criar links de download)
from googletrans import Translator  # Importa o módulo para tradução de textos

# Configuração da página Streamlit
st.set_page_config(
    page_title="Tradutor e Conversor de Texto para Voz",  # Define o título da página
    page_icon="🔊",  # Define o ícone da página
    layout="wide"  # Define o layout como "wide" para usar toda a largura da tela
)

# Inicializa o tradutor do Google
translator = Translator()

# Função para traduzir texto
def translate_text(text, target_language):
    """
    Traduz o texto para o idioma de destino.
    
    Parâmetros:
    - text: Texto a ser traduzido
    - target_language: Código do idioma de destino (ex: 'en', 'es', 'fr')
    
    Retorno:
    - Texto traduzido
    """
    try:
        # Tenta fazer a tradução usando o Google Translator
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        # Em caso de erro, exibe a mensagem e retorna o texto original
        st.error(f"Erro na tradução: {e}")
        return text

# Função para converter texto em voz
def text_to_speech(text, language, speed=1.0):
    """
    Converte texto em arquivo de áudio.
    
    Parâmetros:
    - text: Texto a ser convertido
    - language: Código do idioma (ex: 'pt', 'en')
    - speed: Velocidade da fala (1.0 é velocidade normal)
    
    Retorno:
    - Caminho para o arquivo de áudio gerado
    """
    # Criar diretório temporário se não existir
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Gerar o arquivo de áudio usando Google TTS
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = "temp/audio_converted.mp3"
    tts.save(audio_file)
    
    # Ajustar a velocidade do áudio se necessário
    if speed != 1.0:
        audio = AudioSegment.from_mp3(audio_file)
        # Ajustar velocidade (valores menores que 1.0 aumentam a velocidade)
        audio_speed_adjusted = audio.speedup(playback_speed=speed)
        audio_speed_adjusted.export(audio_file, format="mp3")
    
    # Retornar o caminho do arquivo para download
    return audio_file

# Função para criar link de download
def get_binary_file_downloader_html(bin_file, file_label='Arquivo'):
    """
    Cria um link HTML para download do arquivo de áudio.
    
    Parâmetros:
    - bin_file: Caminho para o arquivo binário
    - file_label: Rótulo para o link de download
    
    Retorno:
    - HTML com link de download
    """
    with open(bin_file, 'rb') as f:
        data = f.read()  # Lê o arquivo binário
    bin_str = base64.b64encode(data).decode()  # Codifica o arquivo em base64
    # Cria um link HTML com o arquivo codificado em base64
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Baixar {file_label}</a>'
    return href

# Título e descrição da aplicação
st.title("🌐 Tradutor e Conversor de Texto para Voz")
st.subheader("Traduza e transforme seu texto em áudio em diferentes idiomas!")

# Painel lateral para configurações
st.sidebar.header("Configurações")

# Dicionário com idiomas suportados e seus códigos
idiomas = {
    "Português": "pt",
    "Inglês": "en",
    "Espanhol": "es",
    "Francês": "fr",
    "Italiano": "it",
    "Alemão": "de",
    "Japonês": "ja",
    "Russo": "ru",
    "Chinês (Simplificado)": "zh-cn"
}

# Seleção de idioma usando caixa de seleção no sidebar
idioma_selecionado = st.sidebar.selectbox("Traduzir e converter para:", list(idiomas.keys()))

# Controle deslizante para ajustar a velocidade da fala
velocidade = st.sidebar.slider("Velocidade da fala:", min_value=0.5, max_value=1.5, value=1.0, step=0.1)

# Checkbox para pular tradução e usar texto original
pular_traducao = st.sidebar.checkbox("Pular tradução (usar texto original)", False)

# Informações adicionais no sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**Dicas:**
- O texto de entrada é considerado como português
- Para textos longos, a tradução pode levar alguns segundos
- Verifique a tradução antes de gerar o áudio
- Ajuste a velocidade para obter uma fala mais natural
""")

# Área principal dividida em duas colunas
col1, col2 = st.columns([1, 1])

# Coluna para texto original
with col1:
    st.markdown("### Texto Original (Português)")
    # Área de texto para entrada do usuário, com um exemplo padrão
    texto_usuario = st.text_area("Digite ou cole seu texto em português aqui:", 
                          "Olá a todos! Lembrem-se que teremos nossa reunião semanal amanhã às 10h na sala de conferências. Por favor, tragam seus relatórios atualizados e ideias para o próximo trimestre..",
                          height=200)
    
    # Botões de ação para texto original, organizados em 3 colunas
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        traduzir = st.button("Traduzir", type="primary")  # Botão primário para traduzir
    with col_btn2:
        gerar_audio_original = st.button("Áudio em Português")  # Botão para gerar áudio em português
    with col_btn3:
        limpar = st.button("Limpar Texto")  # Botão para limpar o texto
        if limpar:
            texto_usuario = ""  # Limpa o texto
            st.rerun()  # Reexecuta o app para refletir a mudança

# Coluna para texto traduzido
with col2:
    st.markdown(f"### Texto Traduzido ({idioma_selecionado})")
    
    # Variável para armazenar o texto traduzido usando session_state
    # Isso mantém o valor entre as reexecuções do Streamlit
    if 'texto_traduzido' not in st.session_state:
        st.session_state.texto_traduzido = ""
    
    # Traduzir texto quando o botão for pressionado
    if traduzir and texto_usuario:
        with st.spinner('Traduzindo...'):  # Mostra um spinner durante a tradução
            language_code = idiomas[idioma_selecionado]  # Obtém o código do idioma
            texto_traduzido = translate_text(texto_usuario, language_code)  # Traduz o texto
            st.session_state.texto_traduzido = texto_traduzido  # Armazena na sessão
    
    # Área de texto para mostrar e editar a tradução
    texto_traduzido = st.text_area("Texto traduzido:", 
                            st.session_state.texto_traduzido,
                            height=200)
    
    # Botões para texto traduzido, organizados em 2 colunas
    col_trad1, col_trad2 = st.columns(2)
    with col_trad1:
        gerar_audio_traduzido = st.button("Gerar Áudio Traduzido", type="primary")  # Botão para gerar áudio traduzido
    with col_trad2:
        editar_traducao = st.button("Editar Tradução")  # Botão para editar tradução (funcionalidade não implementada)

# Área de player de áudio e resultados
st.markdown("---")
st.markdown("### 🎧 Player de Áudio")

# Lógica para gerar áudio do texto original em português
if gerar_audio_original and texto_usuario:
    with st.spinner('Gerando áudio em português...'):  # Mostra um spinner durante a geração do áudio
        audio_path = text_to_speech(texto_usuario, "pt", velocidade)  # Gera o áudio
        
        # Exibir player de áudio integrado do Streamlit
        st.audio(audio_path)
        
        # Link para download do áudio
        st.markdown(get_binary_file_downloader_html(audio_path, 'áudio em português'), unsafe_allow_html=True)
        
        # Detalhes do arquivo gerado
        st.info(f"Idioma: Português | Velocidade: {velocidade}x | Caracteres: {len(texto_usuario)}")

# Lógica para gerar áudio do texto traduzido
elif gerar_audio_traduzido and (texto_traduzido or texto_usuario):
    with st.spinner(f'Gerando áudio em {idioma_selecionado}...'):  # Mostra um spinner durante a geração do áudio
        language_code = idiomas[idioma_selecionado]  # Obtém o código do idioma
        
        # Determinar o texto a ser usado (original ou traduzido)
        if pular_traducao:
            texto_final = texto_usuario  # Usa o texto original
            st.warning("Usando texto original sem tradução")  # Avisa o usuário
        else:
            # Se não há tradução ainda, traduza agora
            if not texto_traduzido:
                texto_traduzido = translate_text(texto_usuario, language_code)
            texto_final = texto_traduzido  # Usa o texto traduzido
        
        audio_path = text_to_speech(texto_final, language_code, velocidade)  # Gera o áudio
        
        # Exibir player de áudio
        st.audio(audio_path)
        
        # Link para download
        st.markdown(get_binary_file_downloader_html(audio_path, f'áudio em {idioma_selecionado}'), unsafe_allow_html=True)
        
        # Detalhes do arquivo
        st.info(f"Idioma: {idioma_selecionado} | Velocidade: {velocidade}x | Caracteres: {len(texto_final)}")
else:
    # Mensagem de instruções quando nenhum áudio foi gerado ainda
    st.info("Digite seu texto, traduza-o se desejar, e clique em um dos botões de áudio para criar seu arquivo de voz.")

# Seção expansível com exemplos de texto
with st.expander("Ver exemplos de texto"):
    st.markdown("""
    **Mensagem motivacional:**
    ```
    Boa tarde, time! Que a gente comece este dia com energia e determinação! Cada desafio é uma oportunidade para aprender e crescer. Vamos seguir juntos, com foco e colaboração, buscando sempre a melhoria e a eficiência no nosso trabalho.
    ```
    
    **Lembrete de reunião:**
    ```
    Olá a todos! Lembrem-se que teremos nossa reunião semanal amanhã às 10h na sala de conferências. Por favor, tragam seus relatórios atualizados e ideias para o próximo trimestre.
    ```
    
    **Instrução técnica:**
    ```
    Para acessar o novo sistema, faça login com suas credenciais habituais e navegue até o menu "Configurações". Em seguida, selecione "Preferências do Usuário" e ative a opção "Novo Interface".
    ```
    """)

# Rodapé com instruções de uso
st.markdown("---")
st.markdown("### Como usar:")
st.markdown("""
1. Digite ou cole seu texto em português na caixa da esquerda
2. Clique em "Traduzir" para converter para o idioma selecionado
3. Verifique e edite a tradução se necessário
4. Escolha:
   - "Áudio em Português" para gerar áudio do texto original
   - "Gerar Áudio Traduzido" para criar áudio no idioma selecionado
5. Ouça o resultado e faça o download se desejar
""")

# Comentário sobre limpeza de arquivos temporários
# Limpeza de arquivos temporários (em produção, você pode implementar uma limpeza periódica)
# Esta parte é opcional e pode ser implementada de diferentes formas