import streamlit as st
import os
import joblib
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

model = joblib.load(os.path.join("data/", "model/", "FinalModel.pkl"))
st.set_page_config(
        page_title="Predict Party",
        layout="wide"
)

#['adoption-of-the-budget-resolution', 'physician-fee-freeze', 'anti-satellite-test-ban', 'synfuels-corporation-cutback', 'education-spending']
voting_options = {
    "y" : "Yes",
    "?" : "abstain",
    "n" : "No"
}
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
    st.session_state.budget = st.selectbox("budget",list(voting_options), format_func=lambda x: voting_options[x], index=None, placeholder="Select an option...")
with col2:
    st.session_state.physician = st.selectbox("physician",list(voting_options), format_func=lambda x: voting_options[x], index=None, placeholder="Select an option...")
with col3:
    st.session_state.ntiSatelite = st.selectbox("ntiSatelite",list(voting_options), format_func=lambda x: voting_options[x], index=None, placeholder="Select an option...")
with col4:
    st.session_state.synfuels = st.selectbox("synfuels",list(voting_options), format_func=lambda x: voting_options[x], index=None, placeholder="Select an option...")
with col5:
    st.session_state.education = st.selectbox("education",list(voting_options), format_func=lambda x: voting_options[x], index=None, placeholder="Select an option...")

cola, colb = st.columns([10,1])
with colb:
        button = st.button("Predict Party")

st.divider()

if button:
	Values = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
	features = ['adoption-of-the-budget-resolution_', 'physician-fee-freeze_', 'anti-satellite-test-ban_', 'synfuels-corporation-cutback_', 'education-spending_']
	to_predict = pd.DataFrame({})
	for col in features:
		to_predict[f"{col}?"] = [0]
		to_predict[f"{col}n"] = [0]
		to_predict[f"{col}y"] = [0]
	to_predict[f"adoption-of-the-budget-resolution_{st.session_state.budget}"] = [1]
	to_predict[f"physician-fee-freeze_{st.session_state.physician}"] = [1]
	to_predict[f"anti-satellite-test-ban_{st.session_state.ntiSatelite}"] = [1]
	to_predict[f"synfuels-corporation-cutback_{st.session_state.synfuels}"] = [1]
	to_predict[f"education-spending_{st.session_state.education}"] = [1]
	prediction = model.predict(to_predict)
	st.write(prediction)