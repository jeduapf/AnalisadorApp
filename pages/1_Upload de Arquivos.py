import streamlit as st
import pandas as pd
import io
from main_functions import process_uploaded_file, validate_csv, footnote # import helper functions

st.set_page_config(page_title="Upload de Arquivos", page_icon="📁", layout="wide")

# Inicializar session_state
if 'uploaded_files_data' not in st.session_state:
    st.session_state.uploaded_files_data = {}

st.title("Upload de Arquivos CSV")
uploaded_files = st.file_uploader(
    "Carregue seus arquivos CSV",
    type=['csv'],
    accept_multiple_files=True,
)

if st.session_state.uploaded_files_data or uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.uploaded_files_data:
            st.session_state.uploaded_files_data[uploaded_file.name] = process_uploaded_file(uploaded_file)

    # Resumo no sidebar com texto normal
    st.sidebar.subheader("Resumo dos Dados")
    valid_files = [f for f in st.session_state.uploaded_files_data.values() if f['valid']]
    if valid_files:
        all_start_dates = [f['start_date'] for f in valid_files if f['start_date']]
        all_end_dates = [f['end_date'] for f in valid_files if f['end_date']]
        total_size = sum(f['size'] for f in valid_files)

        if all_start_dates and all_end_dates:
            st.sidebar.write("---")
            st.sidebar.write("Data Inicial:")
            st.sidebar.write(min(all_start_dates).strftime("%d/%m/%Y %H:%M:%S"))

            st.sidebar.write("Data Final:")
            st.sidebar.write(max(all_end_dates).strftime("%d/%m/%Y %H:%M:%S"))
            st.sidebar.write("---")
            
        st.sidebar.write("Total de Registros:", f"{total_size:,}")
        st.sidebar.write("Arquivos Válidos:", len(valid_files))
        st.sidebar.write("---")
    else:
        st.sidebar.info("Nenhum arquivo válido carregado ainda")

    st.markdown("---")
    st.subheader("Status dos Arquivos")
    for filename, file_info in st.session_state.uploaded_files_data.items():
        with st.expander(f"{'✅' if file_info['valid'] else '❌'} {filename}", expanded=not file_info['valid']):
            if file_info['valid']:
                st.success("Arquivo válido e pronto para análise!")
            else:
                for error in file_info['errors']:
                    st.error(f"❌ {error}")
            for warning in file_info['warnings']:
                st.warning(f"⚠️ {warning}")

    if st.button("Limpar Todos os Arquivos"):
        st.session_state.uploaded_files_data = {}
        st.rerun()
else:
    st.info("Por favor, carregue um ou mais arquivos CSV para começar a análise")

footnote("cartoon_me.png", "José ALVES", "2025", "1.0.0", "https://www.jeduapf.github.io")
