"""
MIT License

Copyright (c) 2026 Desenvolvedor Python Sênior

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

# Função com cache para evitar excesso de requisições (limite do Google Translator)
@st.cache_data(show_spinner=False)
def traduzir_texto(texto: str) -> str:
    return GoogleTranslator(source='auto', target='en').translate(texto)

def main():
    # Título explicando a versão offline
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        "Este aplicativo utiliza bibliotecas tradicionais de Processamento de Linguagem "
        "Natural (**TextBlob** e **deep-translator**) rodando totalmente localmente, **sem dependência de APIs externas** "
        "como OpenAI ou Google Cloud."
    )
    
    st.markdown("---")

    # Área de texto para entrada do usuário
    user_input = st.text_area(
        "Digite seu texto abaixo (pode ser em português ou inglês):",
        placeholder="Ex: Eu estou extremamente feliz com este resultado!",
        height=150
    )

    # Botão 'Analisar'
    if st.button("Analisar Sentimento", type="primary"):
        if not user_input.strip():
            st.warning("Por favor, digite algum texto antes de analisar.")
        else:
            with st.spinner("Analisando sentimento..."):
                try:
                    # Tradução otimizada com cache
                    translated_text = traduzir_texto(user_input)
                    
                    # Análise de polaridade com TextBlob
                    analysis = TextBlob(translated_text)
                    polarity = analysis.sentiment.polarity  # Valor entre -1.0 e 1.0

                    # Classificação baseada na polaridade
                    if polarity > 0.1:
                        st.success(f"**Sentimento: Positivo** (Polaridade: {polarity:.2f})")
                    elif polarity < -0.1:
                        st.error(f"**Sentimento: Negativo** (Polaridade: {polarity:.2f})")
                    else:
                        st.warning(f"**Sentimento: Neutro** (Polaridade: {polarity:.2f})")

                    # Informação complementar opcional para transparência técnica
                    with st.expander("Ver detalhes técnicos da análise"):
                        st.write(f"**Texto Original:** {user_input}")
                        st.write(f"**Texto Traduzido (para o TextBlob):** {translated_text}")
                        st.write(f"**Polaridade Bruta:** {polarity}")
                        st.write(f"**Subjetividade:** {analysis.sentiment.subjectivity}")

                except Exception as e:
                    st.error(
                        "Ocorreu um limite temporário de requisições no tradutor gratuito. "
                        "Por favor, aguarda alguns segundos e tenta novamente.\n\n"
                        f"Detalhe técnico: {e}"
                    )

if __name__ == "__main__":
    main()
