import streamlit as st
from main_functions import footnote

st.set_page_config(
    page_title="Bem-vindo",
    page_icon="⚡",
    layout="wide"
)

st.title("Bem-vindo ao Analisador de Dados Elétricos")
st.write("""
Este aplicativo permite:
- Carregar arquivos CSV de analisadores do tipo MAR722 da Megabras 
- Visualizar gráficos e estatísticas resumidas com dados elétricos (tensão, corrente, potência, etc.)
- Baixar imagens dos gráficos gerados

Use o menu à esquerda para acessar:
1. **Upload de Arquivos**  
2. **Resultados**
""")

# Exibe imagem de exemplo do modelo
st.markdown("---")
st.subheader("Exemplo do modelo MAR722")
st.image("modelo.jpeg", caption="Analisador MAR722 - Megabras", use_container_width=True)
    
footnote("cartoon_me.png", "José ALVES", "2025", "1.0.0", "https://www.jeduapf.github.io")