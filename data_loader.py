import pandas as pd
from config import PESOS, CATEGORIAS
import streamlit as st


def load_data(uploaded_file):
    """Carrega e processa os dados do arquivo Excel"""
    try:
        df = pd.read_excel(uploaded_file)
        
        # Verifica colunas necessárias
        required_columns = ['Responsável', 'Tipo de Serviço', 'Localidade', 'Data/Hora Encerramento']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            st.error(f"Colunas obrigatórias não encontradas: {', '.join(missing_cols)}")
            return None
        
        # Processamento dos dados
        df = df[required_columns].copy()
        df = df.dropna(subset=['Responsável', 'Tipo de Serviço'])
        df['ponto'] = df['Tipo de Serviço'].map(PESOS)
        df = df.dropna(subset=['ponto'])
        
        # Processa datas
        df['data'] = pd.to_datetime(df['Data/Hora Encerramento'], errors='coerce').dt.date
        df = df.dropna(subset=['data'])
        
        # Adiciona colunas auxiliares
        df['dia_semana'] = pd.to_datetime(df['data']).dt.day_name()
        df['semana'] = pd.to_datetime(df['data']).dt.isocalendar().week
        df['mes'] = pd.to_datetime(df['data']).dt.month_name()
        
        # Mapeia categoria de serviço
        df['categoria'] = df['Tipo de Serviço'].apply(
            lambda x: next((k for k, v in CATEGORIAS.items() if x in v), 'OUTROS')
        )
        
        return df
    
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")
        return None