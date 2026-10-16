import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import time

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

# Cache otimizado para guardar traduções e evitar chamadas repetidas ao tradutor
@st.cache_data(show_spinner=False)
def traduzir_para_ingles(texto: str) -> str:
    # Pequena pausa para mitigar limite de requisições rápidas do Google Tradutor gratuito
    time.sleep(0.5)
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(texto)

def main():
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        "Este aplicativo utiliza bibliotecas tradicionais de Processamento de Linguagem "
        "Natural (**TextBlob** e **deep-translator**) para analisar o sentimento de textos em português ou inglês."
    )
    
    st.markdown("---")

    # Área de texto para entrada do usuário
    user_input = st.text_area(
        "Digite seu texto abaixo:",
        placeholder="Ex: Eu estou extremamente feliz com este resultado!",
        height=150
    )

    # Botão 'Analisar'
    if st.button("Analisar Sentimento", type="primary"):
        if not user_input.strip():
            st.warning("Por favor, digite algum texto antes de analisar.")
        else:
            with st.spinner("Traduzindo e analisando sentimento..."):
                try:
                    # Passo 1: Tradução invisível para o inglês via deep-translator
                    translated_text = traduzir_para_ingles(user_input)
                    
                    # Passo 2: Análise de polaridade com TextBlob
                    analysis = TextBlob(translated_text)
                    polarity = analysis.sentiment.polarity  # Valor entre -1.0 e 1.0

                    # Passo 3: Classificação baseada na polaridade
                    if polarity > 0.05:
                        st.success(f"**Sentimento: Positivo** (Polaridade: {polarity:.2f})")
                    elif polarity < -0.05:
                        st.error(f"**Sentimento: Negativo** (Polaridade: {polarity:.2f})")
                    else:
                        st.warning(f"**Sentimento: Neutro** (Polaridade: {polarity:.2f})")

                    # Informação complementar para transparência técnica
                    with st.expander("Ver detalhes técnicos da análise"):
                        st.write(f"**Texto Original:** {user_input}")
                        st.write(f"**Texto Traduzido (para o TextBlob):** {translated_text}")
                        st.write(f"**Polaridade Bruta:** {polarity}")
                        st.write(f"**Subjetividade:** {analysis.sentiment.subjectivity}")

                except Exception as e:
                    st.error(
                        "Ocorreu um limite temporário de requisições no serviço de tradução gratuito do Google. "
                        "Isto acontece ocasionalmente em servidores cloud públicos. "
                        "Por favor, aguarde alguns segundos e tente novamente.\n\n"
                        f"**Detalhe técnico:** {e}"
                    )

if __name__ == "__main__":
    main()
