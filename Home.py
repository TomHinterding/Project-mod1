import streamlit as st
import pandas as pd
import os

st.set_page_config(
        page_title="Raw Data",
)

filepath = os.path.join("data/", "table/", "dataset_56_vote.csv")
Raw_Data = pd.read_csv(filepath)

st.dataframe(Raw_Data, height= 10000)