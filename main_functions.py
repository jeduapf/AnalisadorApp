import pandas as pd
import plotly.graph_objects as go
import io
import streamlit as st
import base64

# ------------------------------
# Funções auxiliares
# ------------------------------

def validate_csv(df, filename):
    """Valida se o CSV tem as colunas necessárias"""
    errors, warnings = [], []

    if df.empty:
        errors.append("O arquivo está vazio")
        return False, errors, warnings

    df.columns = df.columns.str.strip()

    time_col = None
    for col in df.columns:
        if 'TIME' in col.upper():
            time_col = col
            break

    if time_col is None:
        errors.append("Coluna 'TIME' não encontrada")
    else:
        try:
            pd.to_datetime(df[time_col])
        except:
            errors.append("Coluna 'TIME' não está em formato de data/hora válido")

    vrms_cols = [col for col in df.columns if 'VRMS' in col.upper()]
    irms_cols = [col for col in df.columns if 'IRMS' in col.upper()]
    power_cols = [col for col in df.columns if 'P(KW)' in col.upper()]

    if not vrms_cols:
        warnings.append("Nenhuma coluna de tensão (VRMS) encontrada")
    if not irms_cols:
        warnings.append("Nenhuma coluna de corrente (IRMS) encontrada")
    if not power_cols:
        warnings.append("Nenhuma coluna de potência (P) encontrada")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) == 0:
        errors.append("Nenhuma coluna numérica encontrada")

    return len(errors) == 0, errors, warnings

@st.cache_data
def process_uploaded_file(uploaded_file):
    """Processa e valida um arquivo CSV"""
    try:
        df = None
        delimiters = ['\t', ',', ';']
        for delimiter in delimiters:
            try:
                uploaded_file.seek(0)
                df_temp = pd.read_csv(uploaded_file, delimiter=delimiter)
                if len(df_temp.columns) > 1:
                    df = df_temp
                    break
            except:
                continue
        if df is None:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)

        df.columns = df.columns.str.strip()
        is_valid, errors, warnings = validate_csv(df, uploaded_file.name)

        result = {
            'name': uploaded_file.name,
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'data_bytes': None,
            'start_date': None,
            'end_date': None,
            'size': len(df) if not df.empty else 0
        }

        if is_valid:
            time_col = next((col for col in df.columns if 'TIME' in col.upper()), None)
            if time_col:
                try:
                    df[time_col] = pd.to_datetime(df[time_col])
                    result['start_date'] = df[time_col].min()
                    result['end_date'] = df[time_col].max()
                except:
                    pass
            # salvar em bytes parquet para session_state
            buf = io.BytesIO()
            df.to_parquet(buf, index=False)
            result["data_bytes"] = buf.getvalue()

        return result
    except Exception as e:
        return {
            'name': uploaded_file.name,
            'valid': False,
            'errors': [f"Erro ao ler arquivo: {str(e)}"],
            'warnings': [],
            'data_bytes': None,
            'start_date': None,
            'end_date': None,
            'size': 0
        }

@st.cache_data
def load_combined_data(files_data):
    """Combina os DataFrames salvos em session_state"""
    all_data = []
    for file_info in files_data.values():
        if file_info["valid"] and file_info["data_bytes"]:
            df = pd.read_parquet(io.BytesIO(file_info["data_bytes"]))
            df["source_file"] = file_info["name"]
            if "TIME" not in df.columns:
                time_col = next((col for col in df.columns if 'TIME' in col.upper()), None)
                if time_col:
                    df = df.rename(columns={time_col: "TIME"})
            all_data.append(df)
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df["TIME"] = pd.to_datetime(combined_df["TIME"])
        return combined_df.sort_values("TIME")
    return pd.DataFrame()

@st.cache_data
def plot_lines(df, cols, title, ytitle):
    """Cria gráfico de linhas Plotly"""
    fig = go.Figure()
    for col in cols:
        fig.add_trace(go.Scatter(
            x=df['TIME'], y=df[col],
            name=col, mode='lines'
        ))
    fig.update_layout(
        title=title,
        xaxis_title="Data/Hora",
        yaxis_title=ytitle,
        hovermode='x unified',
        height=500
    )
    return fig

def footnote(img_path, name, year, version, link):
    """Adiciona um rodapé estiloso com imagem e texto"""
    import base64
    import streamlit as st

    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()

    st.markdown("---")
    st.markdown(f"""
    <style>
    .footer-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
        padding: 10px 20px;
        border-radius: 12px;
        transition: box-shadow 0.3s ease, transform 0.3s ease, background-color 0.3s ease;
        font-family: 'Comic Sans MS', 'Cursive', sans-serif;
        background-color: transparent;
    }}

    .footer-container:hover {{
        background-color: #FFFFFF; /* white background on hover */
        box-shadow: -8px 0 20px rgba(0,0,0,0.3);
        transform: translateX(-2px);
    }}

    .footer-container a {{
        text-decoration: none;
    }}

    .footer-text {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        font-size: 1rem;
        color: #333333; /* always dark gray text */
        font-weight: bold;
    }}
    </style>

    <div class="footer-container">
        <a href="{link}" target="_blank">
            <img src="data:image/png;base64,{b64}" width="150" style="border-radius:50%;">
        </a>
        <div class="footer-text">
            <span>{name}</span>
            <span>{year}</span>
            <span>v{version}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
