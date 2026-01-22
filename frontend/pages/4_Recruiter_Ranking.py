import streamlit as st
from utils import api_client

st.title("👥 Recruiter Mode: Ranking")

jd_id = st.number_input("Enter Job Description ID", min_value=1, step=1)
resumes = api_client.get_resumes()

if not resumes:
    st.error("No resumes found in database.")
else:
    options = {r['filename']: r['id'] for r in resumes}
    selected_resumes = st.multiselect("Select Candidates to Rank", list(options.keys()))
    
    if st.button("Rank Candidates"):
        if not selected_resumes:
            st.warning("Select at least one candidate.")
        else:
            resume_ids = [options[name] for name in selected_resumes]
            with st.spinner("Ranking..."):
                results = api_client.rank_candidates(jd_id, resume_ids)
                
            if results:
                st.subheader("🏆 Candidate Rankings")
                
                # Display as dataframe for cleaner sortable view
                # Prepare data
                display_data = []
                for res in results:
                    display_data.append({
                        "Rank": res['rank_position'],
                        "Score": res['ats_score'],
                        "Filename": res['filename'],
                        "Matched Skills": len(res['matched_skills']),
                        "Missing Skills": len(res['missing_skills']),
                        "Years Exp": res['years_exp']
                    })
                
                st.dataframe(display_data)
                
                st.subheader("Detailed Breakdown")
                for res in results:
                    with st.expander(f"#{res['rank_position']} {res['filename']} (Score: {res['ats_score']})"):
                        st.write(f"Matched: {', '.join(res['matched_skills'])}")
                        st.write(f"Missing: {', '.join(res['missing_skills'])}")
            else:
                st.error("Ranking failed or no data returned.")
