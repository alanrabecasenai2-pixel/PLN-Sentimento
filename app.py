import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# O st.set_page_config tem de vir LOGO APÓS os imports!
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

def main():
    st.title("📊 Analisador de Sentimentos Offline")
    st.markdown(
        "Este aplicativo utiliza bibliotecas tradicionais de Processamento de Linguagem "
        "Natural (**TextBlob** e **deep-translator**) rodando totalmente localmente, **sem dependência de APIs externas** "
        "como OpenAI ou Google Cloud."
    )
    
    st.markdown("---")

    user_input = st.text_area(
        "Digite seu texto abaixo (pode ser em português ou inglês):",
        placeholder="Ex: Eu estou extremamente feliz com este resultado!",
        height=150
    )

    if st.button("Analisar Sentimento", type="primary"):
        if not user_input.strip():
            st.warning("Por favor, digite algum texto antes de analisar.")
        else:
            with st.spinner("Analisando sentimento..."):
                try:
                    translated_text = GoogleTranslator(source='auto', target='en').translate(user_input)
                    analysis = TextBlob(translated_text)
                    polarity = analysis.sentiment.polarity

                    if polarity > 0.1:
                        st.success(f"**Sentimento: Positivo** (Polaridade: {polarity:.2f})")
                    elif polarity < -0.1:
                        st.error(f"**Sentimento: Negativo** (Polaridade: {polarity:.2f})")
                    else:
                        st.warning(f"**Sentimento: Neutro** (Polaridade: {polarity:.2f})")

                    with st.expander("Ver detalhes técnicos da análise"):
                        st.write(f"**Texto Original:** {user_input}")
                        st.write(f"**Texto Traduzido (para o TextBlob):** {translated_text}")
                        st.write(f"**Polaridade Bruta:** {polarity}")
                        st.write(f"**Subjetividade:** {analysis.sentiment.subjectivity}")

                except Exception as e:
                    st.error(f"Ocorreu um erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
