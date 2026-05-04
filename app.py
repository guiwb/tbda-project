import streamlit as st
import pandas as pd
import plotly.express as px
from services.mongo import list_all

st.set_page_config(layout="wide", page_title="Internet em Pelotas")


def ultimas_mensuracoes(df):
    last_date = df["mensuracao"].max()
    return df[df["mensuracao"] == last_date]


@st.cache_data
def load_data():
    df = list_all()
    df["mensuracao"] = pd.to_datetime(df["mensuracao"])
    return df


df = load_data()

st.sidebar.title("Navegação")

page = st.sidebar.radio(
    "-- Selecione a página --",
    ["📊 Visão geral", "🏢 Provedores", "⚡ Velocidade", "🧪 Tecnologia"]
)

st.sidebar.title("Filtros")

top_empresas = ultimas_mensuracoes(df).groupby(
    "empresa")["qt"].sum().nlargest(5).index.tolist()

empresas = st.sidebar.multiselect(
    "Provedor",
    options=df["empresa"].unique(),
    default=top_empresas
)

tecnologias = st.sidebar.multiselect(
    "Tecnologia",
    options=df["tecnologia"].unique(),
    default=df["tecnologia"].unique()
)

df_filtered = df[
    (df["empresa"].isin(empresas)) &
    (df["tecnologia"].isin(tecnologias))
]

if page == "📊 Visão geral":
    st.title("📊 Visão geral do mercado")

    total = int(ultimas_mensuracoes(df_filtered)["qt"].sum())
    top_empresa = ultimas_mensuracoes(df_filtered).groupby("empresa")[
        "qt"].sum().idxmax()

    col1, col2 = st.columns(2)
    col1.metric("Total de assinantes", total)
    col2.metric("Provedor líder", top_empresa)

    st.markdown("### Evolução no total de assinantes")

    evolucao = df_filtered.groupby("mensuracao")["qt"].sum().reset_index()

    fig = px.line(evolucao, x="mensuracao", y="qt", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Market share")

    share = ultimas_mensuracoes(df_filtered).groupby("empresa")[
        "qt"].sum().reset_index()
    fig2 = px.pie(share, names="empresa", values="qt")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "🏢 Provedores":
    st.title("🏢 Análise de provedores")

    ranking = ultimas_mensuracoes(df_filtered).groupby(
        "empresa")["qt"].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(ranking, x="empresa", y="qt", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Evolução de assinantes por provedor")

    evolucao = df_filtered.groupby(["mensuracao", "empresa"])[
        "qt"].sum().reset_index()

    fig2 = px.line(evolucao, x="mensuracao", y="qt", color="empresa")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "⚡ Velocidade":
    st.title("⚡ Distribuição de velocidade")

    bins = [0, 50, 100, 300, 600, 1000, 10000]
    labels = ["0-50", "50-100", "100-300", "300-600", "600-1000", "1000+"]

    df_filtered["faixa_vel"] = pd.cut(
        df_filtered["velocidade"],
        bins=bins,
        labels=labels
    )

    vel_time = df_filtered.groupby(
        ["mensuracao", "faixa_vel"]
    )["qt"].sum().reset_index()

    fig = px.line(
        vel_time,
        x="mensuracao",
        y="qt",
        color="faixa_vel",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "🧪 Tecnologia":
    st.title("🧪 Tecnologias de acesso")

    tec = ultimas_mensuracoes(df_filtered).groupby(
        "tecnologia")["qt"].sum().reset_index()

    fig = px.bar(tec, x="tecnologia", y="qt", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Evolução no uso das tecnologias")

    tec_time = df_filtered.groupby(
        ["mensuracao", "tecnologia"]
    )["qt"].sum().reset_index()

    fig = px.line(
        tec_time,
        x="mensuracao",
        y="qt",
        color="tecnologia",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)
