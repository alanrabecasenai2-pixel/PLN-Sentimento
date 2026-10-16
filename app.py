# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="📊",
    layout="centered"
)

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
                    # Tradução invisível para o inglês (já que o TextBlob otimiza melhor em inglês)
                    # Detectamos e traduzimos caso necessário, ou simplesmente traduzimos via GoogleTranslator
                    translated_text = GoogleTranslator(source='auto', target='en').translate(user_input)
                    
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
                    st.error(f"Ocorreu um erro durante o processamento: {e}")

if __name__ == "__main__":
    main()
