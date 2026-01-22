import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_skill_match(resume_skills: list[str], jd_skills: list[str]) -> float:
    """
    Computes percentage of JD skills present in resume.
    """
    if not jd_skills:
        return 100.0 if not resume_skills else 0.0 # Edge case: no skills required
    
    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in jd_skills)
    
    matches = resume_set.intersection(jd_set)
    
    # Avoid division by zero
    if len(jd_set) == 0:
        return 0.0
        
    score = (len(matches) / len(jd_set)) * 100
    return round(score, 2)

def compute_similarity_score(resume_text: str, jd_text: str) -> float:
    """
    Computes cosine similarity between resume and JD using TF-IDF.
    """
    if not resume_text or not jd_text:
        return 0.0
    
    documents = [resume_text, jd_text]
    try:
        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(documents)
        similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return round(similarity * 100, 2)
    except Exception as e:
        print(f"Error computing similarity: {e}")
        return 0.0

def extract_years_of_experience(text: str) -> float:
    """
    Extracts maximum years of experience mentioned in text using regex.
    This is a heuristic approach.
    """
    # Patterns like "5 years", "5+ years", "10 yrs"
    # We look for digits followed by year keywords
    pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if not matches:
        return 0.0
    
    # Convert matches to integers and take the maximum found
    # This assumes the resume mentions total experience explicitly or we take the max of segment durations
    # For a simple heuristic, max single mention is often "Over 10 years experience"
    try:
        years = [float(m) for m in matches]
        return max(years)
    except:
        return 0.0

def compute_experience_score(resume_years: float, jd_years: float) -> float:
    """
    Computes score based on experience match.
    If resume_years >= jd_years, score is 100.
    Else, proportional.
    """
    if jd_years <= 0:
        return 100.0
    
    if resume_years >= jd_years:
        return 100.0
    
    score = (resume_years / jd_years) * 100
    return round(score, 2)

def compute_education_score(resume_text: str, jd_text: str) -> float:
    """
    Heuristic scoring for education based on degree keywords.
    """
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    
    degrees = {
        "phd": 3,
        "doctorate": 3,
        "master": 2,
        "ms ": 2, # space to avoid partial word match like 'systems' match 'ms'... tricky. 
                  # Better: "m.s." or regex. Keeping simple for now.
        "m.s.": 2,
        "mba": 2,
        "bachelor": 1,
        "bs ": 1,
        "b.s.": 1,
        "b.tech": 1
    }
    
    # Find highest degree in JD
    jd_level = 0
    for deg, level in degrees.items():
        if deg in jd_lower:
            jd_level = max(jd_level, level)
            
    # Find highest degree in Resume
    resume_level = 0
    for deg, level in degrees.items():
        if deg in resume_lower:
            resume_level = max(resume_level, level)
            
    if jd_level == 0:
        return 100.0 # No specific education requirement found
        
    if resume_level >= jd_level:
        return 100.0
        
    # Partial credit
    return round((resume_level / jd_level) * 100, 2)

def compute_final_ats_score(
    skill_match: float,
    similarity: float,
    experience_score: float,
    education_score: float
) -> float:
    """
    Computes weighted ATS score.
    Weights:
    - Skill Match: 50%
    - Similarity: 25%
    - Experience: 15%
    - Education: 10%
    """
    weighted_score = (
        (skill_match * 0.50) +
        (similarity * 0.25) +
        (experience_score * 0.15) +
        (education_score * 0.10)
    )
    return round(weighted_score, 2)
