import streamlit as st

st.title("🛡️ PROCESS SAFETY MANAGEMENT DIGITAL VISION WALL")

st.header("PSM DASHBOARD")

st.success("PSM Dashboard is running successfully.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("PSM Health", "—")

with col2:
    st.metric("Departments", "—")

with col3:
    st.metric("PSM Pillars", "14")