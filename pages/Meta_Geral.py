import streamlit as st
import pandas as pd
import plotly.express as px
import os

pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

caminho_vendas = os.path.join(pasta_raiz, 'data', 'Relatorio_Abril_Nomes.csv')
caminho_metas = os.path.join(pasta_raiz, 'data', 'Empresas_Faturamento_Meta.csv')

st.set_page_config(
    page_title="Comitê - Meta Geral",
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

st.title("Nossa Meta Geral até agora!")
df_metas = metas.copy()
df_metas = df_metas.drop(columns=["FATURAMENTO ANTERIOR"], errors='ignore')
df_metas['META ESTABELECIDA'] = df_metas['META ESTABELECIDA'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
total_vendas = vendas.groupby('NOME DA EMPRESA')['VALOR TOTAL'].sum()
df_metas['REALIZADO ATUAL'] = df_metas['NOME DA EMPRESA'].map(total_vendas)
df_metas['REALIZADO ATUAL'] = df_metas['REALIZADO ATUAL'].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
# Remove o 'R$' e transforma em float
df_metas['META ESTABELECIDA_NUM'] = df_metas['META ESTABELECIDA'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True).astype(float)
df_metas['REALIZADO ATUAL_NUM'] = df_metas['REALIZADO ATUAL'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True).astype(float)

# Calcula o percentual
df_metas['% DA META'] = (df_metas['REALIZADO ATUAL_NUM'] / df_metas['META ESTABELECIDA_NUM']) * 100

st.subheader("Meta Geral - Consolidado")

# Soma total das metas e do realizado
meta_total = df_metas['META ESTABELECIDA_NUM'].sum()
realizado_total = df_metas['REALIZADO ATUAL_NUM'].sum()
percentual_total = (realizado_total / meta_total) * 100

# Exibe Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Meta Total", f"R$ {meta_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col2.metric("Realizado Total", f"R$ {realizado_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col3.metric("% da Meta Realizada", f"{percentual_total:.2f}%")

# Barra de Progresso Geral
st.progress(min(percentual_total, 100) / 100)

# Gráfico de Barras
df_total = pd.DataFrame({
    'Categoria': ['Meta Total', 'Realizado'],
    'Valor': [meta_total, realizado_total]
})

fig_total = px.bar(df_total, x='Categoria', y='Valor', color='Categoria',
                   text_auto='.2s', color_discrete_sequence=["#1f77b4", "#2ca02c"],
                   title="Comparativo de Meta x Realizado - Geral")

fig_total.update_layout(yaxis_title="Faturamento (R$)")
st.plotly_chart(fig_total, use_container_width=True)

st.subheader("Progresso de Cada Empresa")

for index, row in df_metas.iterrows():
    st.write(f"**{row['NOME DA EMPRESA']}** - {row['% DA META']:.2f}% concluído")
    progresso = min(row['% DA META'], 100) / 100  # Limita a barra em 100%
    st.progress(progresso)


st.caption("Dashboard gerado com dados fictícios")
