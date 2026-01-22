import csv
import os
import re

SKILLS_CSV_PATH = "sample_data/skills_master.csv"

def load_skills() -> set[str]:
    skills = set()
    if not os.path.exists(SKILLS_CSV_PATH):
        # Fallback empty or basic list if file missing
        return {"python", "java", "sql"}
    
    with open(SKILLS_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            for item in row:
                cleaned = item.strip().lower()
                if cleaned:
                    skills.add(cleaned)
    return skills

MASTER_SKILLS = load_skills()

SYNONYM_MAP = {
    "ml": "machine learning",
    "dl": "deep learning",
    "js": "javascript",
    "ts": "typescript",
    "db": "database",
    "powerbi": "power bi",
    "ai": "artificial intelligence",
    "ds": "data science",
    "de": "data engineering",
    "fe": "frontend",
    "be": "backend",
    "fs": "fullstack",
    "cv": "computer vision",
    "nlp": "natural language processing",
    "dda": "data analysis",
    "bi": "business intelligence"
}

def normalize_text(text: str) -> str:
    """Basic text normalization."""
    # Remove special chars but keep some that might be part of skills like C++, C#, .NET
    # For simplicity, we'll replace non-alphanumeric (except +, #, .) with space
    text = text.lower()
    text = re.sub(r'[^a-z0-9+#.]', ' ', text)
    return text

def extract_skills(text: str) -> list[str]:
    """
    Extracts skills from text using the master list and synonym mapping.
    Matches primarily by checking if the skill token(s) exist in the text.
    Processing:
    1. Normalize text
    2. Check for exact matches of multi-word skills first (simple heuristic)
    3. Check for single word skills
    4. Handle synonyms
    """
    normalized_text = normalize_text(text)
    tokens = set(normalized_text.split())
    
    found_skills = set()

    # 1. Check for synonyms in the tokens
    for token in list(tokens):
        if token in SYNONYM_MAP:
            expanded = SYNONYM_MAP[token]
            # Add the expanded term to tokens for matching (optional) or just add directly
            # Here we will check if the expanded term is in our master list
            if expanded in MASTER_SKILLS:
                found_skills.add(expanded)

    # 2. Check for skills in text
    # This is a naive O(N*M) approach, effective for reasonable skill list sizes
    # Ideally we'd use Aho-Corasick or a Trie for large scale
    
    for skill in MASTER_SKILLS:
        # We need to be careful about substrings. e.g. "go" matches "good".
        # Safe approach: regex match with word boundaries
        
        # Escape special characters for regex (like c++, c#)
        escaped_skill = re.escape(skill)
        
        # Look for whole word match
        pattern = r'(?:^|\s)' + escaped_skill + r'(?:$|\s)'
        if re.search(pattern, normalized_text):
            found_skills.add(skill)
            
    return list(found_skills)
