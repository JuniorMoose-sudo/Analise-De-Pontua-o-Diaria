import streamlit as st
from datetime import datetime, timedelta
from config import apply_custom_styles
from data_loader import load_data
from filters import create_filters
from metrics import display_metrics
from charts import (
    plot_tecnicos_chart, plot_daily_evolution,
    plot_category_analysis, plot_time_analysis,
    plot_locality_analysis
)
from details import show_tech_details
from auth import check_authentication, login_form, logout_button

def main():
    st.set_page_config(layout="wide", page_title="Painel de Produtividade", page_icon="📊")

    if not check_authentication():
        login_form()
        return

    apply_custom_styles()

    with st.sidebar:
        logout_button()

    st.title("📊 Dashboard de Produtividade por Técnico")
    uploaded_file = st.file_uploader("Envie a planilha Excel", type=["xlsx", "xls"])

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            filtered_df = create_filters(df)
            comparison_df = filtered_df[filtered_df['data'] < filtered_df['data'].max() - timedelta(days=7)]

            display_metrics(filtered_df, comparison_df)
            pontos_tecnico = plot_tecnicos_chart(filtered_df)
            show_tech_details(filtered_df, pontos_tecnico)
            plot_category_analysis(filtered_df)
            plot_daily_evolution(filtered_df)
            plot_time_analysis(filtered_df)
            plot_locality_analysis(filtered_df)
            st.caption(f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()
