import streamlit as st
import pandas as pd
import json

# -------------------------
# Load Data
# -------------------------

@st.cache_data
def load_data():
    opps = pd.read_csv("opportunities.csv", dtype=str).fillna("")
    with open("guidance.json", "r") as f:
        guidance = json.load(f)
    return opps, guidance

opps, guidance = load_data()

# -------------------------
# App Title
# -------------------------

st.title("Reliably Informing Opportunities Tool (RIOT)")

# -------------------------
# Input
# -------------------------

opp_id = st.text_input("Enter Salesforce Opportunity ID")

if opp_id:

    match = opps[opps["Id"] == opp_id]

    if match.empty:
        st.error("Opportunity not found.")
    else:
        opp = match.iloc[0]

        # Layout
        col1, col2 = st.columns([2, 1])

        # -------------------------
        # Left Column
        # -------------------------
        with col1:

            st.subheader("Stage Specific Guidance")
            st.info(
                guidance["stage_guidance"].get(
                    opp["StageName"],
                    "No guidance available."
                )
            )

            st.subheader("Vertical Specific Guidance")
            st.info(
                guidance["vertical_guidance"].get(
                    opp["Vertical"],
                    "No guidance available."
                )
            )

            st.subheader("Competitor Specific Guidance")
            st.info(
                guidance["competitor_guidance"].get(
                    opp["Competitor"],
                    "No guidance available."
                )
            )

        # -------------------------
        # Right Column
        # -------------------------
        with col2:

            st.subheader("Similar Opportunities")

            similar = opps[
                (opps["Vertical"] == opp["Vertical"]) &
                (opps["StageName"] == opp["StageName"]) &
                (opps["Id"] != opp_id)
            ]

            st.write(similar.head(5)[["Id", "StageName", "Vertical"]])

            st.subheader("ICPs")

            icps = guidance["icps"].get(opp["Vertical"], [])
            for icp in icps:
                st.write("•", icp)
