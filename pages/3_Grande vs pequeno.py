import streamlit as st
from services.mongo import list_all

st.title("Grande vs pequeno (%)")

df = list_all()

min_speed, max_speed = st.slider(
    "Faixa de velocidade Mbps",
    int(df["velocidade"].min()),
    int(df["velocidade"].max()),
    (int(df["velocidade"].min()), int(df["velocidade"].max()))
)

filtered_df = df[
    (df["velocidade"] >= min_speed) &
    (df["velocidade"] <= max_speed) &
    (df["porte"].isin([2, 3]))
]

# Agrupa os dados por ano e porte e soma a quantidade, por exemplo:

# Antes:
# ano	porte	qt
# 2020	2	100
# 2020	2	50
# 2020	3	30

# Depois:

# ano	porte	qt
# 2020	2	150
# 2020	3	30
df_agg = (
    filtered_df
    .groupby(["ano", "porte"])["qt"]
    .sum()
    .reset_index()
)

# Transforma linhas em colunas (pivot)
# Antes:

# ano	porte	qt
# 2020	2	150
# 2020	3	30

# Depois:

# ano	2	3
# 2020	150	30
df_pivot = (
    df_agg
    .pivot(index="ano", columns="porte", values="qt")
    .reindex(columns=[2, 3], fill_value=0).fillna(0)
)

# Renomeia as colunas 2 e 3 para grande e pequeno, para ficar mais legível
df_pivot = df_pivot.rename(columns={
    2: "grande",
    3: "pequeno"
})

df_pivot["total"] = df_pivot["grande"] + df_pivot["pequeno"]

df_pivot["% grande"] = ((df_pivot["grande"] / df_pivot["total"]) * 100).round(2)
df_pivot["% pequeno"] = ((df_pivot["pequeno"] / df_pivot["total"]) * 100).round(2)

st.dataframe(df_pivot.reset_index())