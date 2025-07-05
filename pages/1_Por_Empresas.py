import streamlit as st
import pandas as pd
import plotly.express as px
import os

pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

caminho_vendas = os.path.join(pasta_raiz, 'data', 'Relatorio_Abril_Nomes.csv')
caminho_metas = os.path.join(pasta_raiz, 'data', 'Empresas_Faturamento_Meta.csv')

st.set_page_config(
    page_title="Comitê - Por Empresa",
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

vendas = pd.read_csv(caminho_vendas, delimiter=';')
metas = pd.read_csv(caminho_metas, delimiter=';')


df = vendas.copy()


df['DIA DO FATURAMENTO'] = pd.to_datetime(df['DIA DO FATURAMENTO'], format='%d/%m/%Y')
data_maxima = df['DIA DO FATURAMENTO'].max()
st.title("RESULTADOS GERAIS") 

empresas = df['NOME DA EMPRESA'].unique()
empresa_selecionada = st.sidebar.selectbox("Selecione a empresa:", empresas)

st.subheader(f"Venda Diária pela {empresa_selecionada}")
venda_diaria_empresa = df[df['NOME DA EMPRESA'] == empresa_selecionada]
vendas_hoje = venda_diaria_empresa[venda_diaria_empresa['DIA DO FATURAMENTO'] == data_maxima]['VALOR TOTAL'].sum()
st.metric(label=f"Faturamento de Hoje!", value=f"R$ {vendas_hoje:,.2f}")

st.subheader(f"Resultado do dia:")
venda_diaria = venda_diaria_empresa.groupby('DIA DO FATURAMENTO')['VALOR TOTAL'].sum().reset_index()
fig = px.line(venda_diaria, x='DIA DO FATURAMENTO', y='VALOR TOTAL', markers=True, title="Venda por dia")
st.plotly_chart(fig, use_container_width=True)


st.subheader(f"Vendas dos Últimos 7 Dias - {empresa_selecionada}")
ultimos_7_dias = venda_diaria_empresa[venda_diaria_empresa['DIA DO FATURAMENTO'] >= (data_maxima - pd.Timedelta(days=6))]
vendas_7dias = ultimos_7_dias.groupby('DIA DO FATURAMENTO')['VALOR TOTAL'].sum().reset_index()

fig3 = px.bar(vendas_7dias, x='DIA DO FATURAMENTO', y='VALOR TOTAL', color_discrete_sequence=["#1f77b4"],
              title="Faturamento dos Últimos 7 Dias")
fig3.update_layout(xaxis_title="Data", yaxis_title="Faturamento (R$)")
st.plotly_chart(fig3, use_container_width=True)



st.subheader(f"Acompanhamento de Meta - {empresa_selecionada}")
df_empresa = df[df['NOME DA EMPRESA'] == empresa_selecionada]
faturamento_ate_hoje = df_empresa['VALOR TOTAL'].sum()
meta = metas[metas['NOME DA EMPRESA'] == empresa_selecionada]['META ESTABELECIDA'].values[0]

percentual_meta = (faturamento_ate_hoje / meta) * 100

st.metric(label="Faturamento Até Agora", value=f"R$ {faturamento_ate_hoje:,.2f}")
st.metric(label="Meta Estabelecida", value=f"R$ {meta:,.2f}")
st.metric(label="% da Meta Concluída", value=f"{percentual_meta:.2f}%")

st.caption("Dashboard gerado com dados fictícios")
