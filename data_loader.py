import pandas as pd
from config import PESOS, SERVICE_TO_CATEGORY
import streamlit as st


@st.cache_data(ttl=3600)
def load_data(uploaded_file):
    """Carrega e processa os dados do arquivo Excel"""
    try:
        # Optimization 1: Read only necessary columns
        required_columns = ['Responsável', 'Tipo de Serviço', 'Localidade', 'Data/Hora Encerramento']

        # We can't use usecols directly if we need to check for missing columns gracefully first with all columns
        # But if we assume the file structure is correct or rely on read_excel raising error if cols missing (which it doesn't always if usecols is passed, it might just raise ValueError)
        # However, to be safe and fast, let's try reading only headers first? No, that's two reads.
        # Let's try reading with usecols. If a column is missing, read_excel might raise ValueError.

        try:
             df = pd.read_excel(uploaded_file, usecols=required_columns)
        except ValueError as e:
             # Fallback or error handling if columns are missing
             # But let's stick to the previous logic of checking after read, but we can't do that if we use usecols.
             # Actually, if we use usecols and a col is missing, it raises ValueError: "Usecols do not match columns, columns expected but not found: ..."
             # So we can catch that and show the error.
             st.error(f"Erro ao ler colunas: {str(e)}")
             return None

        # Processamento dos dados
        df = df.dropna(subset=['Responsável', 'Tipo de Serviço'])

        # Map weights
        df['ponto'] = df['Tipo de Serviço'].map(PESOS)
        df = df.dropna(subset=['ponto'])

        # Optimization 2: Optimize date parsing
        # Parse once to datetime
        temp_dates = pd.to_datetime(df['Data/Hora Encerramento'], errors='coerce')

        # Assign date (date object)
        df['data'] = temp_dates.dt.date
        df = df.dropna(subset=['data'])

        # Re-align temp_dates after dropna.
        # Actually, simpler to dropna on 'data' then re-calculate or just calculate all before dropping.
        # Let's calculate all derived columns from temp_dates before dropping?
        # But if date is NaT, then derived cols are also NaT/NaN.
        # So:

        # Filter temp_dates using the same index if we dropped rows?
        # We dropped rows based on 'ponto' earlier.
        # So temp_dates aligns with df.

        # Let's redo:
        # 1. Parse dates
        # 2. Drop NaT
        # 3. Calculate derived

        # We need to make sure we don't have alignment issues.
        df['temp_datetime'] = pd.to_datetime(df['Data/Hora Encerramento'], errors='coerce')
        df = df.dropna(subset=['temp_datetime'])

        df['data'] = df['temp_datetime'].dt.date
        df['dia_semana'] = df['temp_datetime'].dt.day_name()
        df['semana'] = df['temp_datetime'].dt.isocalendar().week
        df['mes'] = df['temp_datetime'].dt.month_name()

        # Remove temp column
        df = df.drop(columns=['temp_datetime'])

        # Optimization 3: Map service category using hash map (O(1))
        # Use map instead of apply
        df['categoria'] = df['Tipo de Serviço'].map(SERVICE_TO_CATEGORY).fillna('OUTROS')

        return df

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")
        return None
