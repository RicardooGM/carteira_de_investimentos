import streamlit as st
import pandas as pd

from core.returns import annualized_return
from core.risk import volatility, correlation_matrix

st.title("📊 Retornos & Risco")

# -----------------------------
# Verificação de dados
# -----------------------------
prices = st.session_state.get("prices")
returns = st.session_state.get("returns")

if prices is None or returns is None:
    st.warning("Carregue os dados na página 📥 Importação de Dados")
    st.stop()

# -----------------------------
# Configurações
# -----------------------------
st.sidebar.subheader("Configurações")

periods = st.sidebar.selectbox(
    "Frequência",
    options=[252, 52, 12],
    format_func=lambda x: "Diário" if x == 252 else "Semanal" if x == 52 else "Mensal"
)

# -----------------------------
# Métricas
# -----------------------------
ret_annual = annualized_return(returns, periods)
vol_annual = volatility(returns, periods)

metrics = pd.DataFrame({
    "Retorno Anualizado": ret_annual,
    "Volatilidade": vol_annual
})

st.subheader("📈 Métricas por Ativo")

st.dataframe(
    metrics.style.format({
        "Retorno Anualizado": "{:.2%}",
        "Volatilidade": "{:.2%}"
    }),
    use_container_width=True
)

# -----------------------------
# Correlação
# -----------------------------
st.subheader("🔗 Correlação entre Ativos")

corr = correlation_matrix(returns)

st.dataframe(
    corr.style
        .background_gradient(cmap="RdYlGn", vmin=-1, vmax=1)
        .format("{:.2f}"),
    use_container_width=True
)
