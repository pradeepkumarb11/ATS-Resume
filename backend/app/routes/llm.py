from fastapi import APIRouter, HTTPException, Body
from app.schemas.llm import RewriteBulletsRequest, GenerateSummaryRequest, GenerateResumeRequest
from app.services import openrouter_client, prompt_templates
import json

router = APIRouter(prefix="/llm", tags=["LLM Tools"])

@router.post("/rewrite_bullets")
def rewrite_bullets(request: RewriteBulletsRequest):
    prompts = prompt_templates.build_rewrite_bullets_prompt(
        request.resume_text, 
        request.jd_text, 
        request.missing_skills, 
        request.target_role
    )
    response_text = openrouter_client.call_openrouter(prompts)
    try:
        # Attempt to parse as JSON if the prompt requested JSON
        return json.loads(response_text)
    except:
        return {"content": response_text}

@router.post("/generate_summary")
def generate_summary(request: GenerateSummaryRequest):
    prompts = prompt_templates.build_summary_prompt(
        request.resume_text, 
        request.jd_text, 
        request.target_role
    )
    response_text = openrouter_client.call_openrouter(prompts)
    try:
        return json.loads(response_text)
    except:
        return {"summary": response_text}

@router.post("/generate_resume")
def generate_resume(request: GenerateResumeRequest):
    prompts = prompt_templates.build_full_resume_prompt(
        request.resume_text, 
        request.jd_text, 
        request.target_role,
        request.candidate_name
    )
    response_text = openrouter_client.call_openrouter(prompts)
    try:
        return json.loads(response_text)
    except:
        return {"content": response_text}
