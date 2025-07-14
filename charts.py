import plotly.express as px
import numpy as np
import streamlit as st

def plot_tecnicos_chart(df):
    """Gráfico de pontos por técnico com informações adicionais"""
    pontos_tecnico = df.groupby('Responsável').agg(
        pontos=('ponto', 'sum'),
        servicos=('ponto', 'count'),
        media_por_servico=('ponto', 'mean'),
        dias_trabalhados=('data', 'nunique')
    ).reset_index().sort_values('pontos', ascending=False)
    
    pontos_tecnico['pontos_por_dia'] = pontos_tecnico['pontos'] / pontos_tecnico['dias_trabalhados']
    
    # Gráfico principal
    fig = px.bar(
        pontos_tecnico, 
        x='Responsável', 
        y='pontos', 
        title="Pontos por Técnico",
        text_auto='.1f',
        color='pontos_por_dia',
        color_continuous_scale='Blues',
        hover_data={
            'Responsável': True,
            'pontos': ':.1f',
            'servicos': True,
            'media_por_servico': ':.2f',
            'dias_trabalhados': True,
            'pontos_por_dia': ':.1f'
        }
    )

    fig.update_layout(
        xaxis_title="Técnico",
        yaxis_title="Pontuação Total",
        hovermode="x unified",
        coloraxis_colorbar=dict(title="Pts/dia")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    return pontos_tecnico

def plot_daily_evolution(df):
    """Gráfico de evolução diária com tendência"""
    pontos_diarios = df.groupby('data').agg(
        pontos=('ponto', 'sum'),
        servicos=('ponto', 'count'),
        tecnicos=('Responsável', 'nunique')
    ).reset_index()
    
    pontos_diarios['media_por_tecnico'] = pontos_diarios['pontos'] / pontos_diarios['tecnicos']
    pontos_diarios['media_por_servico'] = pontos_diarios['pontos'] / pontos_diarios['servicos']
    
    if len(pontos_diarios) > 1:
        fig = px.line(
            pontos_diarios, 
            x='data', 
            y='pontos', 
            markers=True, 
            title="Evolução Diária",
            line_shape='spline',
            hover_data={
                'data': ':%d/%m/%Y',
                'pontos': ':.1f',
                'servicos': True,
                'tecnicos': True,
                'media_por_tecnico': ':.1f',
                'media_por_servico': ':.2f'
            }
        )

        # Adicionar linha de tendência
        z = np.polyfit(range(len(pontos_diarios)), pontos_diarios['pontos'], 1)
        p = np.poly1d(z)
        fig.add_scatter(
            x=pontos_diarios['data'], 
            y=p(pontos_diarios.index), 
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Tendência'
        )

        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Pontuação Total",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("A planilha contém apenas um dia de dados — sem comparação temporal possível.")

def plot_category_analysis(df):
    """Análise por categoria de serviço"""
    st.subheader("📊 Análise por Categoria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por categoria
        cat_dist = df.groupby('categoria').agg(
            pontos=('ponto', 'sum'),
            servicos=('ponto', 'count')
        ).reset_index().sort_values('pontos', ascending=False)
        
        fig = px.pie(
            cat_dist,
            names='categoria',
            values='pontos',
            title='Distribuição de Pontos por Categoria',
            hover_data=['servicos']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pontuação média por categoria
        cat_avg = df.groupby('categoria')['ponto'].mean().reset_index().sort_values('ponto', ascending=False)
        
        fig = px.bar(
            cat_avg,
            x='categoria',
            y='ponto',
            title='Pontuação Média por Serviço',
            text_auto='.2f',
            color='ponto',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

def plot_time_analysis(df):
    """Análise temporal por dia da semana e semana do mês"""
    st.subheader("⏰ Análise Temporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Por dia da semana
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_map = {day: i for i, day in enumerate(weekday_order)}
        
        weekday_data = df.copy()
        weekday_data['dia_semana_num'] = weekday_data['dia_semana'].map(weekday_map)
        weekday_data = weekday_data.sort_values('dia_semana_num')
        
        weekday_stats = weekday_data.groupby('dia_semana').agg(
            pontos=('ponto', 'sum'),
            servicos=('ponto', 'count'),
            tecnicos=('Responsável', 'nunique')
        ).reset_index()
        
        weekday_stats['pontos_por_tecnico'] = weekday_stats['pontos'] / weekday_stats['tecnicos']
        
        fig = px.bar(
            weekday_stats,
            x='dia_semana',
            y='pontos',
            title='Produtividade por Dia da Semana',
            text_auto='.1f',
            color='pontos_por_tecnico',
            color_continuous_scale='Purples',
            hover_data={
                'servicos': True,
                'tecnicos': True,
                'pontos_por_tecnico': ':.1f'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Por semana do mês
        week_stats = df.groupby('semana').agg(
            pontos=('ponto', 'sum'),
            servicos=('ponto', 'count'),
            tecnicos=('Responsável', 'nunique')
        ).reset_index()
        
        week_stats['pontos_por_tecnico'] = week_stats['pontos'] / week_stats['tecnicos']
        
        fig = px.line(
            week_stats,
            x='semana',
            y='pontos',
            title='Produtividade por Semana do Mês',
            markers=True,
            hover_data={
                'servicos': True,
                'tecnicos': True,
                'pontos_por_tecnico': ':.1f'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

def plot_locality_analysis(df):
    """Análise por localidade"""
    st.subheader("📍 Análise por Localidade")
    
    locality_stats = df.groupby('Localidade').agg(
        pontos=('ponto', 'sum'),
        servicos=('ponto', 'count'),
        tecnicos=('Responsável', 'nunique')
    ).reset_index().sort_values('pontos', ascending=False)
    
    locality_stats['pontos_por_servico'] = locality_stats['pontos'] / locality_stats['servicos']
    
    fig = px.scatter(
        locality_stats,
        x='servicos',
        y='pontos',
        size='tecnicos',
        color='pontos_por_servico',
        hover_name='Localidade',
        title='Relação Serviços x Pontos por Localidade',
        labels={
            'servicos': 'Total de Serviços',
            'pontos': 'Total de Pontos',
            'tecnicos': 'Técnicos',
            'pontos_por_servico': 'Pontos/Serviço'
        },
        color_continuous_scale='Viridis'
    )
    
    st.plotly_chart(fig, use_container_width=True)
