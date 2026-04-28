import streamlit as st
from services.mongo import list_by_date, get_available_dates
import pandas as pd

st.title("Assinantes por data")

available_dates = get_available_dates()

date_map = {
    pd.to_datetime(d).strftime("%d/%m/%Y"): d
    for d in available_dates
}

selected_label = st.selectbox("Selecione a data", list(date_map.keys()))
date = date_map[selected_label]

if date:
    df = list_by_date(date)
    st.dataframe(df)