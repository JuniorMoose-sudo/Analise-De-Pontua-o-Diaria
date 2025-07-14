import streamlit as st

def display_metrics(df, comparison_df=None):
    """Exibe métricas resumidas com comparação quando disponível"""
    total_pontos = df['ponto'].sum()
    total_tecnicos = df['Responsável'].nunique()
    total_servicos = len(df)
    media_diaria = df.groupby('data')['ponto'].sum().mean()
    
    # Calcular comparações se disponível
    delta_pontos = delta_tecnicos = delta_servicos = delta_media = None
    
    if comparison_df is not None:
        comp_pontos = comparison_df['ponto'].sum()
        comp_tecnicos = comparison_df['Responsável'].nunique()
        comp_servicos = len(comparison_df)
        comp_media = comparison_df.groupby('data')['ponto'].sum().mean()
        
        delta_pontos = ((total_pontos - comp_pontos) / comp_pontos) * 100 if comp_pontos > 0 else 0
        delta_tecnicos = total_tecnicos - comp_tecnicos
        delta_servicos = ((total_servicos - comp_servicos) / comp_servicos) * 100 if comp_servicos > 0 else 0
        delta_media = ((media_diaria - comp_media) / comp_media) * 100 if comp_media > 0 else 0
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total de Pontos", 
                 f"{total_pontos:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."),
                 f"{delta_pontos:+.1f}%" if delta_pontos is not None else None)
    with cols[1]:
        st.metric("Técnicos Envolvidos", 
                 total_tecnicos,
                 f"{delta_tecnicos:+.0f}" if delta_tecnicos is not None else None)
    with cols[2]:
        st.metric("Total de Serviços", 
                 total_servicos,
                 f"{delta_servicos:+.1f}%" if delta_servicos is not None else None)
    with cols[3]:
        st.metric("Média Diária", 
                 f"{media_diaria:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."),
                 f"{delta_media:+.1f}%" if delta_media is not None else None)
