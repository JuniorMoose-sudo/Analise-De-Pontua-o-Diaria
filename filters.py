import streamlit as st

def create_filters(df):
    """Cria os filtros interativos"""
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de data
    min_date = df['data'].min()
    max_date = df['data'].max()
    date_range = st.sidebar.date_input(
        "Período de análise",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtro de técnicos
    all_techs = sorted(df['Responsável'].unique())
    selected_techs = st.sidebar.multiselect(
        "Selecione os técnicos",
        options=all_techs,
        default=all_techs,
        help="Selecione um ou mais técnicos para análise"
    )
    
    # Filtro de categorias
    all_categories = sorted(df['categoria'].unique())
    selected_categories = st.sidebar.multiselect(
        "Selecione as categorias",
        options=all_categories,
        default=all_categories,
        help="Filtre por tipo de serviço"
    )
    
    # Filtro de localidades
    all_localities = sorted(df['Localidade'].unique())
    selected_localities = st.sidebar.multiselect(
        "Selecione as localidades",
        options=all_localities,
        default=all_localities,
        help="Filtre por bairro/região"
    )
    
    # Aplicar filtros
    filtered_df = df[
        (df['data'].between(date_range[0], date_range[1])) &
        (df['Responsável'].isin(selected_techs)) &
        (df['categoria'].isin(selected_categories)) &
        (df['Localidade'].isin(selected_localities))
    ]
    
    # Mostrar resumo dos filtros
    st.sidebar.markdown(f"""
        **Resumo dos Filtros:**
        - Período: {date_range[0].strftime('%d/%m/%Y')} a {date_range[1].strftime('%d/%m/%Y')}
        - Técnicos selecionados: {len(selected_techs)} de {len(all_techs)}
        - Categorias selecionadas: {len(selected_categories)} de {len(all_categories)}
        - Localidades selecionadas: {len(selected_localities)} de {len(all_localities)}
    """)
    
    return filtered_df