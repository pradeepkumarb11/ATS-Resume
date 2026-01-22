import streamlit as st

st.set_page_config(
    page_title="AI Resume Checker & Optimizer",
    page_icon="🚀",
    layout="wide"
)

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
