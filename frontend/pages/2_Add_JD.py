import streamlit as st
from utils import api_client

st.title("📝 Add Job Description")

role = st.text_input("Job Role / Title", placeholder="e.g. Senior Backend Engineer")
jd_text = st.text_area("Job Description Text", height=300, placeholder="Paste the full JD here...")

if st.button("Save JD"):
    if role and jd_text:
        with st.spinner("Saving..."):
            result = api_client.create_jd(role, jd_text)
            
        if result:
            st.success(f"JD Created! ID: {result['jd_id']}")
        else:
            st.error("Failed to save JD.")
    else:
        st.warning("Please fill in both fields.")
