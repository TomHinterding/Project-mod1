import streamlit as st
import query as q
st.set_page_config(
        page_title="Check Voting Patterns",
        layout="wide",
)

#selectable features for the multiselect / selectionbox box. Key is whatis saved when selecting, Value is what is shown to the user
feature_options = {
        "handicapped-infants" : "handicapped infants",
        "water-project-cost-sharing" : "water project cost sharing",
        "adoption-of-the-budget-resolution" : "adoption of the budget resolution",
        "physician-fee-freeze" : "physician fee freeze",
        "el-salvador-aid" : "el salvador aid",
        "religious-groups-in-schools" : "religious groups in schools",
        "anti-satellite-test-ban" : "anti satellite test ban",
        "aid-to-nicaraguan-contras" : "aid to nicaraguan contras",
        "mx-missile" : "mx missile",
        "immigration" : "immigration",
        "synfuels-corporation-cutback" : "synfuels corporation cutback",
        "education-spending" : "education spending",
        "superfund-right-to-sue" : "superfund right to sue",
        "crime" : "crime",
        "duty-free-exports" : "duty free exports",
        "export-administration-act-south-africa" : "export administration act south africa"
        }

st.header("Check Voting Patterns")
st.write("Select an issue to show voting statistics")
st.divider()

#creates a the selection session state variable that way we can update the selection directly
if "selection" not in st.session_state:
    st.session_state.selection = "handicapped-infants"

#adjusts size of multiselect
col1, col2 = st.columns([3,10])
with col1:
        #if you want to change multiselect to a normal selection box, you just also need to change q.querySelectedfeatures function to query feature.
        #might be needed if there is no way to neatly display the data of multiple features in a diagramm.
        st.session_state.selection = st.multiselect("Select Your Issue:",list(feature_options), format_func=lambda x: feature_options[x], placeholder="Select an option...", default=st.session_state.selection)
st.divider()

if len(st.session_state.selection) != 0:
        selection_text = f"You Picked: "
        for feature in st.session_state.selection:
                selection_text += f"\n- {feature_options[f"{feature}"]}"
        #picked container
        with st.container(border=True):
               st.write(selection_text)

        #Table container
        with st.container(border=True):
                q = q.querySelectedfeatures(st.session_state.selection)
                st.dataframe(q)

        st.divider()
        #Diagram container
        with st.container(border=True):
                st.write("Todo: Display Graph")
