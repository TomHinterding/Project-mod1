import streamlit as st
import query as q
import pandas as pd
import altair as alt

st.set_page_config(
        page_title="Check Voting Patterns",
        layout="wide",
)

#selectable features for the multiselect / selectionbox box. Key is whatis saved when selecting, Value is what is shown to the user
feature_options = q.feature_options()

st.header("Check Voting Patterns")
st.write("Select an issue to show voting statistics")
st.divider()

#creates a the selection session state variable that way we can update the selection directly
if "selection" not in st.session_state:
    st.session_state["selection"] = []

#adjusts size of multiselect
col1, col2 = st.columns([3,10])
with col1:
        #if you want to change multiselect to a normal selection box, you just also need to change q.querySelectedfeatures function to query feature.
        #might be needed if there is no way to neatly display the data of multiple features in a diagramm.
        st.session_state["selection"] = st.multiselect("Select Your Issue:",list(feature_options), format_func=lambda x: feature_options[x], placeholder="Select an option...")
st.divider()

if len(st.session_state["selection"]) != 0:
        selection_text = f"You Picked: "
        for feature in st.session_state["selection"]:
                selection_text += f"\n- {feature_options[feature]}"
        #picked container
        with st.container(border=True):
               st.write(selection_text)

        tab1, tab2 = st.tabs(["Table", "Graph"])
        #Table container
        with tab1:
                with st.container(border=True):
                        results = q.querySelectedfeatures(st.session_state["selection"])
                        pretty = results.copy()
                        pretty["feature"] = pretty["feature"].map(feature_options)
                        pretty = pretty.rename(columns={
                        "feature": "Issue",
                        "Party": "Party",
                        "?count": "Unknown",
                        "ncount": "No",
                        "ycount": "Yes",
                        "?%": "Unknown (%)",
                        "n%": "No (%)",
                        "y%": "Yes (%)"
                        })
                        cols = ["Party","Issue","Yes","Unknown","No","Yes (%)","Unknown (%)","No (%)"]
                        st.dataframe(pretty[cols], use_container_width=True, height=500)

        #Diagram container
        with tab2:
                with st.container(border=True):
                        results = q.querySelectedfeatures(st.session_state["selection"])

                        feature_label_map = feature_options
                        vote_count_map = {"ycount": "Yes", "?count": "Unknown", "ncount": "No"}
                        vote_pct_map   = {"y%": "Yes",   "?%": "Unknown",   "n%": "No"}
                        order = ["Yes", "Unknown", "No"]

                        plot = results.copy()
                        plot["Issue"] = plot["feature"].map(feature_label_map)

                        issue_labels = [feature_label_map[k] for k in st.session_state["selection"]]
                        issue_to_show = issue_labels[0] if len(issue_labels) == 1 else st.selectbox("Issue to graph", issue_labels, index=0)

                        sub = plot[plot["Issue"] == issue_to_show].copy()

                        counts_long = (
                        sub[["Party","Issue","ycount","?count","ncount"]]
                        .melt(id_vars=["Party","Issue"], var_name="VoteKey", value_name="Count")
                        .replace({"VoteKey": vote_count_map})
                        .rename(columns={"VoteKey": "Vote"})
                        )

                        pcts_long = (
                        sub[["Party","Issue","y%","?%","n%"]]
                        .melt(id_vars=["Party","Issue"], var_name="PctKey", value_name="Percent")
                        .replace({"PctKey": vote_pct_map})
                        .rename(columns={"PctKey": "Vote"})
                        )

                        data = counts_long.merge(pcts_long, on=["Party","Issue","Vote"], how="inner")
                        data["Count"] = pd.to_numeric(data["Count"], errors="coerce").fillna(0)
                        data["Percent"] = pd.to_numeric(data["Percent"], errors="coerce").fillna(0.0)
                        data["Percent_fmt"] = data["Percent"].map(lambda x: f"{x:.1f}%")
                        data["Vote"] = pd.Categorical(data["Vote"], categories=order, ordered=True)

                        chart = (
                        alt.Chart(data)
                        .mark_bar()
                        .encode(
                                x=alt.X("Party:N", title="Party"),
                                xOffset=alt.XOffset("Vote:N", sort=order),
                                y=alt.Y("Count:Q", title="Number of votes"),
                                color=alt.Color("Vote:N", scale=alt.Scale(domain=order), title="Vote"),
                                tooltip=[
                                alt.Tooltip("Party:N"),
                                alt.Tooltip("Vote:N"),
                                alt.Tooltip("Count:Q"),
                                alt.Tooltip("Percent:Q", format=".1f")
                                ]
                        )
                        .properties(title=issue_to_show, height=380)
                        )

                        labels = (
                        alt.Chart(data)
                        .mark_text(dy=-6, baseline="bottom")
                        .encode(
                                x="Party:N",
                                xOffset=alt.XOffset("Vote:N", sort=order),
                                y="Count:Q",
                                text="Percent_fmt:N"
                        )
                        )

                        st.altair_chart(chart + labels, use_container_width=True)