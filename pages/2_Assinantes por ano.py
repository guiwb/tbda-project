import streamlit as st
from services.mongo import list_all

st.title("Assinantes por ano")

df = list_all()
options = ["Todos"] + df["empresa"].dropna().unique().tolist()

select_provider = st.selectbox("Provedor", options)

if select_provider != "Todos":
    df_filtered = df[df["empresa"] == select_provider]
else:
    df_filtered = df.copy()

df_agg = (
    df_filtered
    .groupby("ano", as_index=False)["qt"]
    .sum()
    .sort_values("ano")
)

st.line_chart(df_agg.set_index("ano")["qt"])