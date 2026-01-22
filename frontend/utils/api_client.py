import requests
import os
from typing import Optional, Dict, Any

# Load from env or default
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def get_resumes():
    try:
        resp = requests.get(f"{BACKEND_URL}/resumes/")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def upload_resume(file_obj):
    try:
        files = {"file": (file_obj.name, file_obj, file_obj.type)}
        resp = requests.post(f"{BACKEND_URL}/resumes/upload", files=files)
        return resp.json() if resp.status_code == 200 else None
    except Exception as e:
        print(e)
        return None

def create_jd(role: str, jd_text: str):
    try:
        payload = {"role": role, "jd_text": jd_text}
        resp = requests.post(f"{BACKEND_URL}/jds/create", json=payload)
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def get_jd(jd_id: int):
    try:
        resp = requests.get(f"{BACKEND_URL}/jds/{jd_id}")
        return resp.json() if resp.status_code == 200 else None
    except:
        return None

def run_analysis(resume_id: int, jd_id: int, use_llm: bool = False):
    try:
        payload = {
            "resume_id": resume_id,
            "jd_id": jd_id,
            "use_llm": use_llm
        }
        resp = requests.post(f"{BACKEND_URL}/analysis/run", json=payload)
        return resp.json() if resp.status_code == 200 else {"detail": resp.text}
    except Exception as e:
        return {"detail": str(e)}

def rank_candidates(jd_id: int, resume_ids: list):
    try:
        # Expected body format: {"resume_ids": [1, 2]} for Body(embed=True)
        resp = requests.post(f"{BACKEND_URL}/rank/jd/{jd_id}", json={"resume_ids": resume_ids})
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def get_report_pdf(analysis_id: int):
    try:
        resp = requests.get(f"{BACKEND_URL}/reports/{analysis_id}/pdf")
        return resp.content if resp.status_code == 200 else None
    except:
        return None

def get_resume_pdf(analysis_id: int):
    try:
        resp = requests.get(f"{BACKEND_URL}/reports/resume/{analysis_id}/pdf")
        return resp.content if resp.status_code == 200 else None
    except:
        return None

def get_resume_text(analysis_id: int):
    try:
        resp = requests.get(f"{BACKEND_URL}/reports/resume/{analysis_id}/text")
        return resp.content if resp.status_code == 200 else None
    except:
        return None
