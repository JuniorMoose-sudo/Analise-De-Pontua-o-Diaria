import streamlit as st

# Tabela de Pontuação
PESOS = {
    # ATIVAÇÃO
    "BOT - FIBRA ATIVAÇÃO": 2,
    "OPERAÇÕES - FIBRA ATIVAÇÃO (INSTALAÇÃO)": 2,
    "OPERAÇÕES - REVISITA - INSTALAÇÃO FIBRA": 2,
    "OPERAÇÕES - REVISITA DE ATIVAÇÃO AGENDADA": 2,

    # TROCA DE ENDEREÇO
    "OPERAÇÕES - TROCA DE ENDEREÇO": 2,
    "OPERAÇÕES - REVISITA - TROCA DE ENDEREÇO": 2,
    "OPERAÇÕES - RECOLHIMENTO/TROCA DE ENDEREÇO": 0.84,
    
    # CORRETIVA
    "OPERAÇÕES - PROBLEMA RECORRENTE": 1.14,
    "OPERAÇÕES - AÇÕES PREVENTIVAS": 1.14,
    "OPERAÇÕES - SERVIÇOS ADICIONAIS": 1.14,
    "OPERAÇÕES - DIFICULDADES DE ACESSO": 1.14,

    # CORRETIVA REVISITA
    "OPERAÇÕES - REVISITA SERVIÇOS ADICIONAIS": 1.14,
    "OPERAÇÕES - REVISITA AÇÕES PREVENTIVAS": 1.14,
    "OPERAÇÕES - REVISITA DIFICULDADES DE ACESSO": 1.14,
    "OPERAÇÕES - REVISITA PROBLEMA RECORRENTE": 1.14,

    # SEM ACESO
    "OPERAÇÕES - SEM ACESSO": 1.14,
    "OPERAÇÕES - RÁDIO SEM ACESSO": 1.14,
    
    # SEM ACESO REVISITA
    "OPERAÇÕES - SEM ACESSO REVISITA": 1.14,
    "OPERAÇÕES - RÁDIO SEM ACESSO REVISITA": 1.14,

    # RECOLHIMENTO
    "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO": 0.84,
    "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO AGENDADO": 0.84,
    "ESTOQUE - REVISITA DE RECOLHIMENTO EM COMODATO": 0.84
}

# Categorias de serviços para agrupamento
CATEGORIAS = {
    "ATIVAÇÃO": ["BOT - FIBRA ATIVAÇÃO", "OPERAÇÕES - FIBRA ATIVAÇÃO (INSTALAÇÃO)", 
                "OPERAÇÕES - REVISITA - INSTALAÇÃO FIBRA", "OPERAÇÕES - REVISITA DE ATIVAÇÃO AGENDADA"],
    
    "TROCA DE ENDEREÇO": ["OPERAÇÕES - TROCA DE ENDEREÇO", "OPERAÇÕES - REVISITA - TROCA DE ENDEREÇO",
                         "OPERAÇÕES - RECOLHIMENTO/TROCA DE ENDEREÇO"],
    
    "CORRETIVA": ["OPERAÇÕES - PROBLEMA RECORRENTE", "OPERAÇÕES - AÇÕES PREVENTIVAS",
                 "OPERAÇÕES - SERVIÇOS ADICIONAIS", "OPERAÇÕES - DIFICULDADES DE ACESSO",
                 "OPERAÇÕES - REVISITA SERVIÇOS ADICIONAIS", "OPERAÇÕES - REVISITA AÇÕES PREVENTIVAS",
                 "OPERAÇÕES - REVISITA DIFICULDADES DE ACESSO", "OPERAÇÕES - REVISITA PROBLEMA RECORRENTE"],
    
    "SEM ACESSO": ["OPERAÇÕES - SEM ACESSO", "OPERAÇÕES - RÁDIO SEM ACESSO",
                  "OPERAÇÕES - SEM ACESSO REVISITA", "OPERAÇÕES - RÁDIO SEM ACESSO REVISITA"],
    
    "RECOLHIMENTO": ["ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO", 
                    "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO AGENDADO",
                    "ESTOQUE - REVISITA DE RECOLHIMENTO EM COMODATO"]
}

# Estilos e formatações
def apply_custom_styles():
    st.markdown("""
        <style>
            .main {background-color: #f8f9fa;}
            .stDataFrame {width: 100%;}
            .css-1v0mbdj {margin: 0 auto;}
            .stPlotlyChart {border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
            .stAlert {border-radius: 10px;}
            .st-bb {background-color: white;}
            .st-at {background-color: #f0f2f6;}
            header {background-color: white !important;}
            .metric-container {padding: 15px; border-radius: 10px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
            .metric-title {font-size: 14px; color: #555;}
            .metric-value {font-size: 24px; font-weight: bold; color: #1a73e8;}
            .metric-delta {font-size: 12px;}
            .section-title {border-bottom: 2px solid #1a73e8; padding-bottom: 5px; margin-top: 20px !important;}
            .filter-box {background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;}
        </style>
    """, unsafe_allow_html=True)