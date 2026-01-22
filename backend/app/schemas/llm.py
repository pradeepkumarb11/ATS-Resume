from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class LLMRequestBase(BaseModel):
    resume_text: str
    jd_text: str
    target_role: str

class RewriteBulletsRequest(LLMRequestBase):
    missing_skills: List[str] = []

class GenerateSummaryRequest(LLMRequestBase):
    pass

class GenerateResumeRequest(LLMRequestBase):
    candidate_name: str

class LLMResponseBase(BaseModel):
    content: Any # JSON or string
