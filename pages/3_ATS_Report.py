import streamlit as st
from utils import api_client
import time

st.title("📊 ATS Analysis Report")

# Fetch Data
resumes = api_client.get_resumes()
# Assuming we can get JDs too, or just user input ID. For now let's input ID or Mock List.
# We'll just ask for JD ID since we didn't make a get_jds list endpoint (only create/get).
# Better user experience: Add GET /jds/ route or just simple text input for JD ID.
jd_id = st.number_input("Enter Job Description ID", min_value=1, step=1)

resume_options = {r['filename']: r['id'] for r in resumes}
selected_resume_name = st.selectbox("Select Resume", list(resume_options.keys()) if resumes else [])

use_llm = st.checkbox("Enable LLM (Deepseek) for Optimization", value=False)
st.caption("⚠️ LLM features require a valid OpenRouter API Key in backend.")

if st.button("Run Analysis"):
    if not selected_resume_name or not jd_id:
        st.error("Please select a resume and provide a valid JD ID.")
    else:
        resume_id = resume_options[selected_resume_name]
        
        with st.spinner("Running deep analysis... This may take a few seconds (or more with LLM)."):
            data = api_client.run_analysis(resume_id, jd_id, use_llm)
            
        if "detail" in data:
            st.error(f"Analysis Failed: {data['detail']}")
        else:
            st.success("Analysis Complete!")
            
            # --- Results Display ---
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("ATS Score", f"{data['ats_score']}%")
            col2.metric("Skill Match", f"{data['skill_match_pct']}%")
            col3.metric("Similarity", f"{data['similarity_score_pct']}%")
            col4.metric("Experience Score", f"{data['experience_score_pct']}%")
            
            # Gauge for ATS Score (Simple Progress Bar)
            st.progress(data['ats_score'] / 100)
            
            st.subheader("Skill Analysis")
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"✅ Matched Skills ({len(data['matched_skills'])})")
                st.write(", ".join(data['matched_skills']))
                
            with c2:
                st.warning(f"❌ Missing Skills ({len(data['missing_skills'])})")
                st.write(", ".join(data['missing_skills']))
                
            st.subheader("Recommendations")
            for rec in data['recommendations']:
                st.markdown(f"- {rec}")
                
            if use_llm:
                st.divider()
                st.subheader("🤖 LLM Suggestions")
                
                tab1, tab2, tab3 = st.tabs(["Rewritten Bullets", "Optimized Summary", "Draft Resume"])
                
                with tab1:
                    if data.get('optimized_bullets'):
                        for item in data['optimized_bullets']:
                            st.markdown(f"**Original:** {item.get('original', '')}")
                            st.markdown(f"**Rewritten:** {item.get('rewritten', '')}")
                            st.caption(f"Reasoning: {item.get('reasoning', '')}")
                            st.divider()
                    else:
                        st.info("No rewritten bullets available.")
                        
                with tab2:
                    # Note: We didn't explicitly return summary in analysis response schema separate from generated_resume_text
                    # But if we did partial LLM calls (e.g. just summary) it would appear.
                    # The full resume generation includes summary.
                    st.info("Check the full draft resume for the new summary.")
                    
                with tab3:
                    draft_text = data.get('generated_resume_text')
                    if draft_text:
                        st.text_area("Full ATS Optimized Resume JSON/Text", value=str(draft_text), height=500)
                        st.download_button(
                            "Download JSON Source", 
                            str(draft_text), 
                            file_name=f"optimized_resume_{resume_id}.json"
                        )
                        
                        # PDF Download
                        if "id" in data:
                            pdf_data = api_client.get_resume_pdf(data['id'])
                            if pdf_data:
                                st.download_button(
                                    "📄 Download PDF Resume (ATS Format)",
                                    pdf_data,
                                    file_name=f"optimized_resume_{resume_id}.pdf",
                                    mime="application/pdf"
                                )
                            else:
                                st.warning("Could not generate PDF. Ensure resume data is valid.")
                            
                            # Text Download
                            txt_data = api_client.get_resume_text(data['id'])
                            if txt_data:
                                st.download_button(
                                    "📝 Download Plain Text Resume (ATS Optimized)",
                                    txt_data,
                                    file_name=f"optimized_resume_{resume_id}.txt",
                                    mime="text/plain"
                                )
                    else:
                        st.info("No draft resume generated.")
