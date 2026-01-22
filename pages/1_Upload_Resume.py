import streamlit as st
from utils import api_client

st.title("📤 Upload Resume")

uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    if st.button("Upload & Process"):
        with st.spinner("Uploading and extracting text..."):
            result = api_client.upload_resume(uploaded_file)
            
        if result:
            st.success(f"Resume uploaded successfully! ID: {result['id']}")
            st.json(result)
        else:
            st.error("Failed to upload resume. Please check backend connection.")

st.subheader("Recent Uploads")
resumes = api_client.get_resumes()
if resumes:
    st.table(resumes)
else:
    st.info("No resumes found.")
