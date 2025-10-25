import streamlit as st

st.set_page_config(
        page_title="Check Voting Patterns",
        layout="wide",
)

st.header("Check Voting Patterns")
st.write("Select an issue to show voting statistics")
st.divider()

if "selection" not in st.session_state:
    st.session_state.selection = "handicapped-infants"

col1, col2 = st.columns([3,10])
with col1:
        st.session_state.selection = st.selectbox("Select Your Issue:",
                ['handicapped infants',
                'water project cost sharing',
                'adoption of the-budget resolution',
                'physician fee freeze',
                'el salvador aid',
                'religious groups in schools',
                'anti satellite test ban',
                'aid to nicaraguan contras',
                'mx missile',
                'immigration',
                'synfuels corporation cutback',
                'education spending',
                'superfund right to sue',
                'crime',
                'duty free exports',
                'export administration act south africa'])

st.divider()

with st.container(border=True):
        st.write("You Picked: ", st.session_state.selection)
        st.write("Todo: Display Table")

st.divider()

with st.container(border=True):
        st.write("You Picked: ", st.session_state.selection)
        st.write("Todo: Display Graph")
