# 🌐 Tradutor e Conversor de Texto para Voz

Esta aplicação web desenvolvida com Streamlit permite traduzir textos para diferentes idiomas e convertê-los em arquivos de áudio. O usuário pode inserir texto em português, traduzi-lo para um dos idiomas disponíveis e gerar arquivos de áudio tanto do texto original quanto do texto traduzido.

## 🚀 Funcionalidades

- Tradução de texto para 10 idiomas diferentes
- Conversão de texto para voz (Text-to-Speech)
- Ajuste de velocidade da fala
- Player de áudio integrado
- Download dos arquivos de áudio gerados
- Interface amigável e responsiva

## 🛠️ Requisitos

Para executar esta aplicação, você precisará das seguintes bibliotecas Python:

- streamlit
- gtts (Google Text-to-Speech)
- pydub
- base64
- googletrans
- os (biblioteca padrão)

## 📦 Instalação

```bash
pip install streamlit gtts pydub googletrans==4.0.0-rc1
```

Nota: A versão específica do googletrans é necessária para evitar problemas de compatibilidade.

## 🔧 Como executar

```bash
streamlit run app.py
```

Substitua `app.py` pelo nome do arquivo que contém o código.

## 👨‍💻 Como usar

1. Digite ou cole seu texto em português na caixa da esquerda
2. Selecione o idioma de destino no menu lateral
3. Ajuste a velocidade da fala usando o controle deslizante
4. Clique em "Traduzir" para converter o texto para o idioma selecionado
5. Verifique e edite a tradução se necessário
6. Escolha:
   - "Áudio em Português" para gerar áudio do texto original
   - "Gerar Áudio Traduzido" para criar áudio no idioma selecionado
7. Ouça o resultado e faça o download se desejar

## 🌍 Idiomas suportados

- Português
- Inglês
- Espanhol
- Francês
- Italiano
- Alemão
- Japonês
- Russo
- Chinês (Simplificado)

## 📝 Exemplos de uso

A aplicação inclui exemplos de textos que podem ser usados para testar:
- Mensagem motivacional
- Lembrete de reunião
- Instrução técnica

## ⚠️ Observações

- A pasta "temp" será criada para armazenar os arquivos de áudio temporários
- Para textos muito longos, a tradução pode levar alguns segundos
- O texto de entrada é considerado como português por padrão
