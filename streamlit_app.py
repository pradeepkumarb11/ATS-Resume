import streamlit as st

st.set_page_config(
    page_title="AI Resume Checker & Optimizer",
    page_icon="🚀",
    layout="wide"
)

# --- Start Backend (Unified Deployment) ---
import subprocess
import time
import requests
import os
import sys

# Function to check if backend is running
def is_backend_running(url="http://localhost:8000"):
    try:
        requests.get(f"{url}/")
        return True
    except requests.exceptions.ConnectionError:
        return False

# Start backend if not running
if not is_backend_running():
    with st.spinner("Starting Backend Server... (This may take a minute)"):
        # We run uvicorn from the 'backend' directory so relative imports in backend/app work correctly
        # We use a non-blocking subprocess
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd="backend",  # Important: Run from backend directory
            stdout=subprocess.DEVNULL, # Suppress stdout to keep streamlit clean
            stderr=subprocess.DEVNULL,
        )
        # Wait a few seconds for it to start
        time.sleep(5)
        
        # Retry check
        retries = 10
        while retries > 0:
            if is_backend_running():
                st.success("Backend started successfully!")
                break
            time.sleep(2)
            retries -= 1
        else:
            st.error("Failed to start backend. Please check logs.")
# ------------------------------------------

st.title("🚀 AI Resume Checker & Optimizer")

st.markdown("""
### Welcome to the AI-Powered ATS System

This tool helps candidates optimize their resumes and recruiters screen candidates efficiently.

#### Features:
- **📊 ATS Scoring Engine**: Intelligent analysis of skills, experience, and context.
- **🤖 LLM Integration**: Auto-rewrite bullets, generate summaries, and full resume drafts (OpenRouter/Deepseek).
- **📝 Job Description Match**: Tailored analysis against specific JDs.
- **🏆 Recruiter Mode**: Batch ranking of candidates.

#### How to use:
1. **Upload Resume**: Go to the Upload page to add your resume (PDF/DOCX).
2. **Add JD**: Input the target Job Description.
3. **ATS Report**: Select a resume and JD to get a detailed analysis.
4. **Recruiter Mode**: Rank multiple candidates against a JD.
""")

st.sidebar.success("Select a page above.")
