from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"))
    
    ats_score = Column(Float)
    skill_match_pct = Column(Float)
    similarity_score_pct = Column(Float)
    experience_score_pct = Column(Float)
    education_score_pct = Column(Float)
    
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    keyword_suggestions = Column(JSON)
    recommendations = Column(JSON)
    optimized_bullets = Column(JSON)
    generated_resume_text = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resume = relationship("app.models.resume.Resume")
    job_description = relationship("app.models.job_description.JobDescription")
