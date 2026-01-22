from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    resume_id: int
    jd_id: int
    use_llm: bool = False

class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    jd_id: int
    
    ats_score: float
    skill_match_pct: float
    similarity_score_pct: float
    experience_score_pct: float
    education_score_pct: float
    
    matched_skills: List[str]
    missing_skills: List[str]
    keyword_suggestions: List[str]
    recommendations: List[str]
    
    # LLM additions
    optimized_bullets: Optional[List[Dict[str, str]]] = None
    generated_resume_text: Optional[str] = None
    
    created_at: datetime

    class Config:
        from_attributes = True
