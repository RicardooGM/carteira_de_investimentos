import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from data_loader import load_prices, compute_returns

st.set_page_config(page_title="Carteira Quant", layout="wide")
st.title("📊 App de Análise de Carteira")

# =========================
# 1️⃣ Importação de dados
# =========================
st.header("📥 Importação de Dados")

tickers = st.text_input(
    "Ativos (separados por vírgula)",
    "PETR4.SA, VALE3.SA, ITUB4.SA"
)

col1, col2 = st.columns(2)

with col1:
    start = st.date_input("Data inicial")

with col2:
    end = st.date_input("Data final")

if start >= end:
    st.error("Data inicial deve ser menor que a final.")
    st.stop()

prices = load_prices(
    [t.strip().upper() for t in tickers.split(",")],
    start,
    end
)
st.subheader("📊 Preços")

col3, col4 = st.columns(2, vertical_alignment="center")

with col3:
        st.line_chart(prices)
with col4:
        st.dataframe(prices)

# =========================
# 2️⃣ Retornos
# =========================
st.header("📈 Retornos")

col5, col6 = st.columns(2, vertical_alignment="center")

with col5:
    st.write("Retorno Simples")

    returns = compute_returns(prices)

    st.line_chart(returns)

with col6:
    st.write("Retorno Acumulado Simples")
    retorno_acumulado =  (1+returns).cumprod()-1
    st.line_chart(retorno_acumulado)

# =========================
# ⚠️ RISCO
# =========================
st.header("⚠️ Retorno e Risco")
def infer_periods_per_year(returns):
    days = (returns.index[-1] - returns.index[0]).days
    years = days / 365.25
    return max(1, int(round(len(returns) / years)))

if returns is None or returns.empty:
    st.info("Selecione os ativos e o período para calcular o risco.")
    st.stop()

# Frequência inferida automaticamente a partir do período selecionado
periods_per_year = infer_periods_per_year(returns)

# Retorno e risco anualizados
ret_annual = returns.mean() * periods_per_year
vol_annual = returns.std() * np.sqrt(periods_per_year)

retorno = (1+returns).prod()-1

risk_metrics = pd.DataFrame({
    "Retorno Médio do Periodo": ret_annual,
    "Retorno Acumulado do Período":retorno,
    "Volatilidade (Risco)": vol_annual
})

st.dataframe(
    risk_metrics.style.format("{:.2%}"),
    use_container_width=True
)

# Transparência metodológica
st.caption(
    f"""
📅 Período analisado: **{start} → {end}**  
📊 Observações totais: **{len(returns)}**  
📐 Frequência implícita: **≈ {periods_per_year} observações/ano**  
⚠️ Risco medido como **desvio-padrão anualizado dos retornos**
"""
)


# =========================
# 4️⃣ Correlação
# =========================

col1, col2 = st.columns(2)

with col1:
    st.header("🔗 Correlação")


    if returns is None or returns.empty:
        st.info("Calcule os retornos para visualizar a correlação.")
        st.stop()

    corr_matrix = returns.corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto"
    )

    fig.update_layout(
        height=450,
        
        
        coloraxis_colorbar=dict(title="Correlação")
    )

    st.plotly_chart(fig, use_container_width=True)

#ADICIONAR O IBOVESPA COMO BENCHMARK PARA OS TOPICOS 
