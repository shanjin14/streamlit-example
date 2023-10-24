import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit UI! 👋")

st.sidebar.success("select a module you need here")

st.markdown(
    """
A sample UI for manage flat file upload, reference data management
"""
)