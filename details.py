import streamlit as st
import plotly.express as px

def show_tech_details(df, pontos_tecnico):
    """Mostra detalhes por técnico"""
    st.subheader("🔍 Detalhes por Técnico")
    
    selected_tech = st.selectbox(
        "Selecione um técnico para detalhes",
        options=pontos_tecnico['Responsável'].tolist()
    )
    
    tech_data = df[df['Responsável'] == selected_tech]
    
    if not tech_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**📌 Resumo do Técnico: {selected_tech}**")
            
            total_pontos = tech_data['ponto'].sum()
            total_servicos = len(tech_data)
            dias_trabalhados = tech_data['data'].nunique()
            media_diaria = total_pontos / dias_trabalhados if dias_trabalhados > 0 else 0
            media_servico = total_pontos / total_servicos if total_servicos > 0 else 0
            
            st.metric("Total de Pontos", f"{total_pontos:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.metric("Total de Serviços", total_servicos)
            st.metric("Dias Trabalhados", dias_trabalhados)
            st.metric("Média Diária", f"{media_diaria:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."))
            st.metric("Média por Serviço", f"{media_servico:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        with col2:
            st.markdown("**📈 Evolução Diária**")
            
            tech_daily = tech_data.groupby('data').agg(
                pontos=('ponto', 'sum'),
                servicos=('ponto', 'count')
            ).reset_index()
            
            fig = px.line(
                tech_daily,
                x='data',
                y='pontos',
                markers=True,
                title=f"Desempenho Diário - {selected_tech}",
                hover_data=['servicos']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**🛠 Distribuição por Tipo de Serviço**")
        
        tech_services = tech_data.groupby('Tipo de Serviço').agg(
            pontos=('ponto', 'sum'),
            servicos=('ponto', 'count')
        ).reset_index().sort_values('pontos', ascending=False)
        
        fig = px.bar(
            tech_services,
            x='Tipo de Serviço',
            y='pontos',
            color='servicos',
            title=f"Serviços Realizados - {selected_tech}",
            hover_data=['servicos'],
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
