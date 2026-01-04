import streamlit as st
from data.data_loader import load_prices

st.title("📥 Importação de Dados")

tickers = st.text_input(
    "Ativos (separados por vírgula)",
    "PETR4.SA, VALE3.SA, ITUB4.SA"
)

col1, col2 = st.columns(2)

with col1:
    start = st.date_input("Data inicial")

with col2:
    end = st.date_input("Data final")

if st.button("Carregar dados"):
    prices = load_prices(
        [t.strip() for t in tickers.split(",")],
        start,
        end
    )

    st.session_state["prices"] = prices
    st.success("Dados carregados com sucesso!")

if "prices" in st.session_state:
    st.subheader("Prévia dos dados")
    st.dataframe(st.session_state["prices"].head())

