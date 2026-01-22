from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.analysis import ResumeAnalysis
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.utils.skills import extract_skills
from app.services import ats_engine
import json

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/run", response_model=AnalysisResponse)
def run_analysis(request: AnalysisRequest, db: Session = Depends(get_db)):
    # 1. Fetch Resources
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    jd = db.query(JobDescription).filter(JobDescription.id == request.jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job Description not found")
        
    # 2. Extract Skills
    resume_skills = extract_skills(resume.resume_text or "")
    jd_skills = extract_skills(jd.jd_text or "")
    
    # 3. Compute Scores
    skill_match_score = ats_engine.compute_skill_match(resume_skills, jd_skills)
    similarity_score = ats_engine.compute_similarity_score(resume.resume_text or "", jd.jd_text or "")
    
    resume_exp = ats_engine.extract_years_of_experience(resume.resume_text or "")
    jd_exp = ats_engine.extract_years_of_experience(jd.jd_text or "")
    exp_score = ats_engine.compute_experience_score(resume_exp, jd_exp)
    
    edu_score = ats_engine.compute_education_score(resume.resume_text or "", jd.jd_text or "")
    
    final_score = ats_engine.compute_final_ats_score(
        skill_match_score, similarity_score, exp_score, edu_score
    )
    
    # 4. Detailed Analysis
    resume_skills_set = set(s.lower() for s in resume_skills)
    jd_skills_set = set(s.lower() for s in jd_skills)
    
    matched_skills = list(resume_skills_set.intersection(jd_skills_set))
    missing_skills = list(jd_skills_set - resume_skills_set)
    keyword_suggestions = missing_skills # Simple alias for now
    
    # Rule-based Recommendations
    recommendations = []
    if final_score < 70:
        recommendations.append("Overall score is low. Consider tailoring your resume heavily for this role.")
    if skill_match_score < 50:
        recommendations.append(f"Missing critical skills: {', '.join(missing_skills[:5])}. Add these if you have them.")
    if similarity_score < 40:
        recommendations.append("Contextual similarity is low. Use more keywords from the JD in your summary and experience.")
    if exp_score < 100:
        recommendations.append(f"Experience gap detected. JD mentions {jd_exp} years, found {resume_exp} years.")
        
    # LLM Augmentation
    optimized_bullets = None
    generated_resume_text = None
    
    if request.use_llm:
        from app.services import openrouter_client, prompt_templates
        import json
        
        # 4a. Rewrite Bullets
        try:
            bullet_prompts = prompt_templates.build_rewrite_bullets_prompt(
                resume.resume_text or "",
                jd.jd_text or "",
                missing_skills,
                jd.role or "Target Role"
            )
            bullets_resp = openrouter_client.call_openrouter(bullet_prompts)
            try:
                optimized_bullets = json.loads(bullets_resp)["rewritten_bullets"]
            except:
                # Fallback if valid JSON not found in mocked/raw response
                # We interpret the raw string as a single item or handle error
                pass
        except Exception as e:
            print(f"LLM Error (Bullets): {e}")

        # 4b. Generate Full Optimized Resume
        try:
            resume_prompts = prompt_templates.build_full_resume_prompt(
                resume.resume_text or "",
                jd.jd_text or "",
                jd.role or "Target Role",
                resume.user.name if resume.user else "Candidate"
            )
            resume_resp = openrouter_client.call_openrouter(resume_prompts)
            generated_resume_text = resume_resp # Keep raw string or JSON string
        except Exception as e:
            print(f"LLM Error (Resume): {e}")

    # 5. Store Result
    analysis = ResumeAnalysis(
        resume_id=resume.id,
        jd_id=jd.id,
        ats_score=final_score,
        skill_match_pct=skill_match_score,
        similarity_score_pct=similarity_score,
        experience_score_pct=exp_score,
        education_score_pct=edu_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        keyword_suggestions=keyword_suggestions,
        recommendations=recommendations,
        optimized_bullets=optimized_bullets,
        generated_resume_text=generated_resume_text
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis
