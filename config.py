import streamlit as st

# Tabela de Pontuação
PESOS = {
    # ATIVAÇÃO
    "BOT - FIBRA ATIVAÇÃO": 2.30,
    "OPERAÇÕES - FIBRA ATIVAÇÃO (INSTALAÇÃO)": 2.30,
    "OPERAÇÕES - REVISITA - INSTALAÇÃO FIBRA": 2.30,
    "OPERAÇÕES - REVISITA DE ATIVAÇÃO AGENDADA": 2.30,
    "OPERAÇÕES - ATIVAÇÃO FIBRA (CORPORATIVO/GOVERNO)": 2.30,

    # TROCA DE ENDEREÇO
    "OPERAÇÕES - TROCA DE ENDEREÇO": 2.30,
    "OPERAÇÕES - REVISITA - TROCA DE ENDEREÇO": 2.30,
    "OPERAÇÕES - RECOLHIMENTO/TROCA DE ENDEREÇO": 0.96,

    # CORRETIVA
    "OPERAÇÕES - PROBLEMA RECORRENTE": 1.31,
    "OPERAÇÕES - AÇÕES PREVENTIVAS": 1.31,
    "OPERAÇÕES - AÇÕES PREVENTIVAS/CRÍTICO": 1.31,
    "OPERAÇÕES - SERVIÇOS ADICIONAIS": 1.31,
    "OPERAÇÕES - DIFICULDADES DE ACESSO": 1.31,
    "OPERAÇÕES - ANÁLISE TÉCNICA": 1.31,
    "OPERAÇÕES - PASSAGEM DE CABO": 1.31,
    "OPERAÇÕES - TROCA DE EQUIPAMENTO": 1.31,
    "OPERAÇÕES - PROBLEMA NO EQUIPAMENTO": 1.31,
    "OPERAÇÕES - PROBLEMA NO CONECTOR": 1.31,
    "OPERAÇÕES - PROBLEMA NA REDE INTERNA": 1.31,
    "OPERAÇÕES - PROBLEMA COM PÁGINAS/APP ESPECÍFICOS": 1.31,
    "OPERAÇÕES - EQUIPAMENTO DESATUALIZADO": 1.31,
    "OPERAÇÕES - EQUIPAMENTO TRAVADO": 1.31,
    "OPERAÇÕES - SINAL ALTO": 1.31,
    "OPERAÇÕES - DNS": 1.31,
    "OPERAÇÕES - ORIGEM REDES": 1.31,
    "OPERAÇÕES - INTERFERÊNCIA": 1.31,
    "OPERAÇÕES - ONU DESPROVISIONADA": 1.31,
    "OPERAÇÕES - CABO ROMPIDO": 1.31,

    # CORRETIVA REVISITA
    "OPERAÇÕES - REVISITA SERVIÇOS ADICIONAIS": 1.31,
    "OPERAÇÕES - REVISITA AÇÕES PREVENTIVAS": 1.31,
    "OPERAÇÕES - REVISITA DIFICULDADES DE ACESSO": 1.31,
    "OPERAÇÕES - REVISITA PROBLEMA RECORRENTE": 1.31,

    # SEM ACESSO
    "OPERAÇÕES - SEM ACESSO": 1.31,
    "OPERAÇÕES - RÁDIO SEM ACESSO": 1.31,

    # SEM ACESSO REVISITA
    "OPERAÇÕES - SEM ACESSO REVISITA": 1.31,
    "OPERAÇÕES - RÁDIO SEM ACESSO REVISITA": 1.31,

    # RECOLHIMENTO
    "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO": 0.96,
    "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO AGENDADO": 0.96,
    "ESTOQUE - REVISITA DE RECOLHIMENTO EM COMODATO": 0.96,
    "ESTOQUE - EQUIPAMENTO RECOLHIDO": 0.96,
    "ESTOQUE - EQUIPAMENTO NÃO RECOLHIDO": 0.96,
    "ESTOQUE - RECOLHIMENTO AGENDADO": 0.96,
    "ESTOQUE- CLIENTE AUSENTE": 0.96
}

# Categorias de serviços para agrupamento - ATUALIZADA
CATEGORIAS = {
    "ATIVAÇÃO": [
        "BOT - FIBRA ATIVAÇÃO",
        "OPERAÇÕES - FIBRA ATIVAÇÃO (INSTALAÇÃO)",
        "OPERAÇÕES - REVISITA - INSTALAÇÃO FIBRA",
        "OPERAÇÕES - REVISITA DE ATIVAÇÃO AGENDADA",
        "OPERAÇÕES - ATIVAÇÃO FIBRA (CORPORATIVO/GOVERNO)"
    ],

    "TROCA DE ENDEREÇO": [
        "OPERAÇÕES - TROCA DE ENDEREÇO",
        "OPERAÇÕES - REVISITA - TROCA DE ENDEREÇO",
        "OPERAÇÕES - RECOLHIMENTO/TROCA DE ENDEREÇO"
    ],

    "CORRETIVA": [
        "OPERAÇÕES - PROBLEMA RECORRENTE",
        "OPERAÇÕES - AÇÕES PREVENTIVAS",
        "OPERAÇÕES - AÇÕES PREVENTIVAS/CRÍTICO",
        "OPERAÇÕES - SERVIÇOS ADICIONAIS",
        "OPERAÇÕES - DIFICULDADES DE ACESSO",
        "OPERAÇÕES - REVISITA SERVIÇOS ADICIONAIS",
        "OPERAÇÕES - REVISITA AÇÕES PREVENTIVAS",
        "OPERAÇÕES - REVISITA DIFICULDADES DE ACESSO",
        "OPERAÇÕES - REVISITA PROBLEMA RECORRENTE",
        "OPERAÇÕES - ANÁLISE TÉCNICA",
        "OPERAÇÕES - PASSAGEM DE CABO",
        "OPERAÇÕES - TROCA DE EQUIPAMENTO",
        "OPERAÇÕES - PROBLEMA NO EQUIPAMENTO",
        "OPERAÇÕES - PROBLEMA NO CONECTOR",
        "OPERAÇÕES - PROBLEMA NA REDE INTERNA",
        "OPERAÇÕES - PROBLEMA COM PÁGINAS/APP ESPECÍFICOS",
        "OPERAÇÕES - EQUIPAMENTO DESATUALIZADO",
        "OPERAÇÕES - EQUIPAMENTO TRAVADO",
        "OPERAÇÕES - SINAL ALTO",
        "OPERAÇÕES - DNS",
        "OPERAÇÕES - ORIGEM REDES",
        "OPERAÇÕES - INTERFERÊNCIA",
        "OPERAÇÕES - ONU DESPROVISIONADA",
        "OPERAÇÕES - CABO ROMPIDO"
    ],

    "SEM ACESSO": [
        "OPERAÇÕES - SEM ACESSO",
        "OPERAÇÕES - RÁDIO SEM ACESSO",
        "OPERAÇÕES - SEM ACESSO REVISITA",
        "OPERAÇÕES - RÁDIO SEM ACESSO REVISITA"
    ],

    "RECOLHIMENTO": [
        "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO",
        "ESTOQUE - RECOLHIMENTO DE EQUIPAMENTO COMODATO AGENDADO",
        "ESTOQUE - REVISITA DE RECOLHIMENTO EM COMODATO",
        "ESTOQUE - EQUIPAMENTO RECOLHIDO",
        "ESTOQUE - EQUIPAMENTO NÃO RECOLHIDO",
        "ESTOQUE - RECOLHIMENTO AGENDADO",
        "ESTOQUE- CLIENTE AUSENTE"
    ]
}

# Flatten CATEGORIAS for O(1) lookup
SERVICE_TO_CATEGORY = {}
for category, services in CATEGORIAS.items():
    for service in services:
        SERVICE_TO_CATEGORY[service] = category

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
