import streamlit as st
import os
import joblib
from sklearn.neighbors import KNeighborsClassifier

model = joblib.load(os.path.join("data/", "model/", "FinalModel.pkl"))
st.set_page_config(
        page_title="Predict Party",
        layout="wide"
)

#['adoption-of-the-budget-resolution', 'physician-fee-freeze', 'anti-satellite-test-ban', 'synfuels-corporation-cutback', 'education-spending']

if "budget" not in st.session_state:
    st.session_state.budget = "abstain"
if "physician" not in st.session_state:
    st.session_state.physician = "abstain"
if "antiSatelite" not in st.session_state:
    st.session_state.ntiSatelite = "abstain"
if "synfuels" not in st.session_state:
    st.session_state.synfuels = "abstain"
if "education" not in st.session_state:
    st.session_state.education = "abstain"

st.header("Predict Party")
st.divider()

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

with col1:
    st.session_state.budget = st.selectbox("budget",["Yes", "abstain", "No"], index=None, placeholder="Select an option...")
with col2:
    st.session_state.physician = st.selectbox("physician",["Yes", "abstain", "No"], index=None, placeholder="Select an option...")
with col3:
    st.session_state.ntiSatelite = st.selectbox("ntiSatelite",["Yes", "abstain", "No"], index=None, placeholder="Select an option...")
with col4:
    st.session_state.synfuels = st.selectbox("synfuels",["Yes", "abstain", "No"], index=None, placeholder="Select an option...")
with col5:
    st.session_state.education = st.selectbox("education",["Yes", "abstain", "No"], index=None, placeholder="Select an option...")

cola, colb = st.columns([10,1])
with colb:
        button = st.button("Predict Party")

st.divider()

if button:
    i=0
    Values = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    for var in st.session_state:
        if var == "abstain":
            Values[0][3*i]=1
        elif var == "No":
            Values[0][3*i + 1] = 1
        else:
            Values[0][3*i +2] = 1
    st.write(model.predict(Values))

