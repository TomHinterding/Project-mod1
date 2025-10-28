import streamlit as st
import query as q

st.set_page_config(page_title="Raw Data", layout="wide")
st.header("Raw Voting Data")

df = q.raw_readable()
st.dataframe(df, use_container_width=True, height=900)
