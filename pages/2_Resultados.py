import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from main_functions import load_combined_data, plot_lines, footnote  # import helper functions

st.set_page_config(page_title="Resultados", page_icon="📊", layout="wide")

st.title("Resultados da Análise")
combined_df = load_combined_data(st.session_state.uploaded_files_data)

if combined_df.empty:
    st.info("Por favor, carregue arquivos válidos na página 'Upload de Arquivos'.")
else:
    tab1, tab2, tab3, tab4 = st.tabs(["Tensão", "Corrente", "Potência", "Resumo Estatístico"])

    with tab1:
        voltage_cols = [c for c in combined_df.columns if "VRMS(V)" in c and "AVG" in c]
        if voltage_cols:
            st.plotly_chart(plot_lines(combined_df, voltage_cols[:3], "Tensão RMS", "Tensão (V)"), use_container_width=True)

    with tab2:
        current_cols = [c for c in combined_df.columns if "IRMS(A)" in c and "AVG" in c]
        if current_cols:
            st.plotly_chart(plot_lines(combined_df, current_cols[:3], "Corrente RMS", "Corrente (A)"), use_container_width=True)

    with tab3:
        power_cols = [c for c in combined_df.columns if "P(kW)" in c and "AVG" in c]
        if power_cols:
            st.plotly_chart(plot_lines(combined_df, power_cols[:4], "Potência Ativa", "Potência (kW)"), use_container_width=True)

    with tab4:
        col1, col2 = st.columns(2)
        if voltage_cols:
            with col1:
                st.markdown("#### Estatísticas de Tensão (V)")
                st.dataframe(combined_df[voltage_cols[:3]].describe(), use_container_width=True)
        if current_cols:
            with col2:
                st.markdown("#### Estatísticas de Corrente (A)")
                st.dataframe(combined_df[current_cols[:3]].describe(), use_container_width=True)
        if power_cols:
            st.markdown("#### Estatísticas de Potência (kW/kWAr)")
            st.dataframe(combined_df[power_cols[:4]].describe(), use_container_width=True)

footnote("cartoon_me.png", "José ALVES", "2025", "1.0.0", "https://www.jeduapf.github.io")
