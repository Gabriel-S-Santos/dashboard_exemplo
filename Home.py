import streamlit as st
import pandas as pd
import plotly.express as px
import os

vendas = pd.read_csv('data/Relatorio_Abril_Nomes.csv', delimiter=';')

df = vendas.copy()

st.set_page_config(
    page_title="Comitê diário",
    page_icon="📊",
    layout="wide"  # Pode ser 'wide' ou 'centered'
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    html, body, [class*="css"], .stApp, .stMarkdown, .stMetric, .stText, h1, h2, h3, h4, h5, h6, p, div {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #000080;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Bem-vindo ao nosso comitê!")

st.write("""

""")

st.success("Selecione uma página no menu à esquerda para começar.")
df['DIA DO FATURAMENTO'] = pd.to_datetime(df['DIA DO FATURAMENTO'], format='%d/%m/%Y')

st.subheader("Faturamento Diário Total")
faturamento_diario = df.groupby('DIA DO FATURAMENTO')['VALOR TOTAL'].sum().reset_index()
fig = px.line(faturamento_diario, x='DIA DO FATURAMENTO', y='VALOR TOTAL', markers=True, title="Faturamento por Dia")
fig.update_layout(xaxis_title="Data", yaxis_title="Faturamento (R$)")
st.plotly_chart(fig, use_container_width=True)


faturamento_consultor = df.groupby('CONSULTOR')['VALOR TOTAL'].sum().reset_index()
fig2 = px.bar(faturamento_consultor, x='CONSULTOR', y='VALOR TOTAL', title="Faturamento por Consultor")
fig2.update_layout(yaxis_title="Faturamento (R$)", showlegend=False)
st.plotly_chart(fig2, use_container_width=True)