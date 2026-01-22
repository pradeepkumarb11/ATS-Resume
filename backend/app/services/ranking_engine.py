from typing import List, Dict, Any
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.utils.skills import extract_skills
from app.services import ats_engine

def rank_resumes(jd: JobDescription, resumes: List[Resume]) -> List[Dict[str, Any]]:
    """
    Computes ATS scores for a list of resumes against a JD and returns them ranked.
    """
    ranked_results = []
    
    jd_skills = extract_skills(jd.jd_text or "")
    jd_exp = ats_engine.extract_years_of_experience(jd.jd_text or "")
    
    for resume in resumes:
        resume_text = resume.resume_text or ""
        resume_skills = extract_skills(resume_text)
        
        # specific extraction for this resume
        resume_exp = ats_engine.extract_years_of_experience(resume_text)
        
        # Compute scores
        skill_match_score = ats_engine.compute_skill_match(resume_skills, jd_skills)
        similarity_score = ats_engine.compute_similarity_score(resume_text, jd.jd_text or "")
        exp_score = ats_engine.compute_experience_score(resume_exp, jd_exp)
        edu_score = ats_engine.compute_education_score(resume_text, jd.jd_text or "")
        
        final_score = ats_engine.compute_final_ats_score(
            skill_match_score, similarity_score, exp_score, edu_score
        )
        
        # Helpers for response
        resume_skills_set = set(s.lower() for s in resume_skills)
        jd_skills_set = set(s.lower() for s in jd_skills)
        
        matched_skills = list(resume_skills_set.intersection(jd_skills_set))
        missing_skills = list(jd_skills_set - resume_skills_set)
        
        ranked_results.append({
            "resume_id": resume.id,
            "filename": resume.filename,
            "ats_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "years_exp": resume_exp
        })
        
    # Sort by ATS Score descending
    ranked_results.sort(key=lambda x: x["ats_score"], reverse=True)
    
    # Add rank position
    for i, res in enumerate(ranked_results):
        res["rank_position"] = i + 1
        
    return ranked_results
