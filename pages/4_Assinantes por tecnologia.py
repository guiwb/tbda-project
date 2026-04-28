import streamlit as st
from services.mongo import list_all

st.title("Assinantes por tecnologia e provedor")

df = list_all()

providers = df["empresa"].dropna().unique().tolist()

selected_providers = st.multiselect(
    "Provedores",
    providers,
    default=[]
)

if selected_providers:
    df_filtered = df[df["empresa"].isin(selected_providers)]
else:
    df_filtered = df.copy()

df_agg = (
    df_filtered
    .groupby(["ano", "tecnologia"])["qt"]
    .sum()
    .reset_index()
)

df_pivot = (
    df_agg
    .pivot(index="ano", columns="tecnologia", values="qt")
    .fillna(0)
    .sort_index()
)

st.area_chart(df_pivot)