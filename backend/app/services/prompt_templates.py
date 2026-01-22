import json

def build_rewrite_bullets_prompt(resume_text: str, jd_text: str, missing_skills: list[str], target_role: str) -> list[dict]:
    """
    Builds a prompt for rewriting resume bullets to match a job description.
    """
    system_prompt = (
        "You are an expert ATS Resume Optimizer. Your task is to rewrite resume bullet points "
        "to differ to the provided Job Description (JD) while strictly adhering to the facts.\n"
        "STRICT RULE: Do NOT invent fake experience or facts not present in the original resume. "
        "Only enhance the phrasing, emphasize relevant skills, and quantify achievements where possible."
    )
    
    missing_skills_str = ', '.join(missing_skills) if missing_skills else "None specific"

    user_prompt = f"""
    Target Role: {target_role}
    
    Job Description:
    {jd_text}
    
    Current Resume Content:
    {resume_text}
    
    Missing Skills to Incorporate (only if supported by resume context):
    {missing_skills_str}
    
    INSTRUCTIONS:
    1. Rewrite the bullet points to be impact-driven and results-oriented.
    2. Use strong action verbs.
    3. Incorporate ATS keywords from the JD and missing skills list NATURALLY.
    4. Provide suggestions for quantification if exact numbers are missing (e.g., [increased by X%]).
    
    OUTPUT FORMAT:
    Return a VALID JSON object with the following structure:
    {{
      "rewritten_bullets": [
        {{
          "original": "original bullet text",
          "rewritten": "optimized bullet text",
          "reasoning": "brief explanation of changes"
        }}
      ]
    }}
    Ensure the output is raw JSON, no markdown formatting.
    """
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def build_summary_prompt(resume_text: str, jd_text: str, target_role: str) -> list[dict]:
    """
    Builds a prompt for creating a professional profile summary.
    """
    system_prompt = (
        "You are an expert Career Coach. Your task is to write a compelling 3-4 line professional summary "
        "tailored to a specific target role and job description.\n"
        "STRICT RULE: Do NOT invent fake experience."
    )
    
    user_prompt = f"""
    Target Role: {target_role}
    
    Job Description:
    {jd_text}
    
    Resume Content:
    {resume_text}
    
    INSTRUCTIONS:
    1. Write a professional summary (3-4 lines max).
    2. Highlight years of experience, key achievements, and top skills relevant to the JD.
    3. Integrate high-value keywords from the JD.
    
    OUTPUT FORMAT:
    Return a VALID JSON object:
    {{
      "summary": "The generated summary text..."
    }}
    Ensure the output is raw JSON, no markdown formatting.
    """
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def build_full_resume_prompt(resume_text: str, jd_text: str, target_role: str, candidate_name: str) -> list[dict]:
    """
    Builds a prompt for generating a full ATS-optimized resume in plain text.
    """
    system_prompt = (
        "You are an AI Resume Builder. Your task is to rewrite a resume into a standard, clean, "
        "ATS-friendly PLAIN TEXT format. \n"
        "STRICT RULE: Do NOT invent fake experience. If information is missing, omit it."
    )
    
    user_prompt = f"""
    Candidate Name: {candidate_name}
    Target Role: {target_role}
    
    Job Description:
    {jd_text}
    
    Original Resume:
    {resume_text}
    
    INSTRUCTIONS:
    1. Output MUST be in plain text. NO Markdown. NO JSON.
    2. Follow this EXACT structure and ordering:
       - Header (Name, Phone, Email, LinkedIn, Location)
       - PROFESSIONAL SUMMARY
       - SKILLS
       - EXPERIENCE (or INTERNSHIPS if applicable)
       - PROJECTS
       - EDUCATION
       - CERTIFICATIONS
       - ADDITIONAL INFORMATION (optional)
    3. Use UPPERCASE for section headings.
    4. Use a separator line exactly like this between sections:
       ------------------------------------------------------------
    5. Use valid bullet points (•) for details.
    6. Optimize the content (Summary, Bullets) to match the JD keywords naturally.
    
    OUTPUT TEMPLATE:
    [NAME]
    [Phone] | [Email] | [Location] | [LinkedIn]
    
    PROFESSIONAL SUMMARY
    ------------------------------------------------------------
    [Optimized summary text...]
    
    SKILLS
    ------------------------------------------------------------
    [Skill 1], [Skill 2], [Skill 3]...
    
    EXPERIENCE
    ------------------------------------------------------------
    [ROLE TITLE] | [COMPANY] | [DATES]
    • [Optimized bullet 1]
    • [Optimized bullet 2]
    
    [ROLE TITLE 2]...
    
    (Continue for all sections)
    """
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
