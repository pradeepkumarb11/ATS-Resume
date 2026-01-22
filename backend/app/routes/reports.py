from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.analysis import ResumeAnalysis
from app.models.resume import Resume
from app.models.job_description import JobDescription
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import json

router = APIRouter(prefix="/reports", tags=["Reports"])

def draw_header(c, title):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, title)
    c.line(50, 745, 550, 745)

@router.get("/{analysis_id}/pdf")
def generate_report_pdf(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    jd = analysis.job_description
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle(f"ATS Report - {analysis_id}")
    
    # Header
    draw_header(c, "ATS Analysis Report")
    
    # Details
    c.setFont("Helvetica", 12)
    y = 720
    c.drawString(50, y, f"Role: {jd.role if jd else 'Unknown'}")
    y -= 20
    c.drawString(50, y, f"Date: {analysis.created_at.strftime('%Y-%m-%d %H:%M')}")
    y -= 40
    
    # Scores
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Overall ATS Score: {analysis.ats_score}%")
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Skill Match: {analysis.skill_match_pct}% | Similarity: {analysis.similarity_score_pct}%")
    y -= 15
    c.drawString(50, y, f"Experience: {analysis.experience_score_pct}% | Education: {analysis.education_score_pct}%")
    y -= 30
    
    # Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Matched Skills:")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(50, y, ", ".join(analysis.matched_skills))
    y -= 30
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.red)
    c.drawString(50, y, "Missing Skills:")
    c.setFillColor(colors.black)
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(50, y, ", ".join(analysis.missing_skills))
    y -= 30
    
    # Recommendations
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Recommendations:")
    y -= 15
    c.setFont("Helvetica", 10)
    for rec in analysis.recommendations:
        c.drawString(60, y, f"- {rec}")
        y -= 15
        
    # Rewritten Bullets (if any)
    if analysis.optimized_bullets:
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Optimized Bullets Suggestions:")
        y -= 15
        c.setFont("Helvetica", 9)
        bullets = analysis.optimized_bullets
        if isinstance(bullets, str):
             try: bullets = json.loads(bullets)
             except: bullets = []
             
        for item in bullets:
            if y < 100: # New page if running out of space
                c.showPage()
                y = 750
            if isinstance(item, dict):
                c.drawString(60, y, f"Original: {item.get('original', '')[:90]}...")
                y -= 12
                c.drawString(60, y, f"Better:   {item.get('rewritten', '')[:90]}...")
                y -= 20

    c.save()
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=report_{analysis_id}.pdf"})

@router.get("/resume/{analysis_id}/pdf")
def generate_resume_pdf(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.id == analysis_id).first()
    if not analysis or not analysis.generated_resume_text:
        raise HTTPException(status_code=404, detail="Generated resume not found")

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle(f"Optimized Resume - {analysis_id}")
    
    text_content = analysis.generated_resume_text
    
    # 1. Check if it happens to be JSON (old data compatibility), convert to string if so
    if isinstance(text_content, str):
        try:
            # If it parses as JSON, it might be old data. We'll just dump it as string for now
            # or try to format it. But prioritizing new text format.
            parsed = json.loads(text_content)
            if isinstance(parsed, dict):
                text_content = json.dumps(parsed, indent=2) # Fallback
        except:
            pass # It is just text, good.

    # 2. Draw Text Logic
    text_object = c.beginText(40, 750)
    text_object.setFont("Courier", 10) # Fixed width is safe for layout
    
    lines = text_content.split('\n')
    for line in lines:
        # Simple pagination
        if text_object.getY() < 40:
            c.drawText(text_object)
            c.showPage()
            text_object = c.beginText(40, 750)
            text_object.setFont("Courier", 10)
        
        # Check for our separators to bold or handle nicely? 
        # For now, just print line by line.
        text_object.textLine(line)
        
    c.drawText(text_object)
    c.save()
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=resume_{analysis_id}.pdf"})

@router.get("/resume/{analysis_id}/text")
def generate_resume_text(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.id == analysis_id).first()
    if not analysis or not analysis.generated_resume_text:
        raise HTTPException(status_code=404, detail="Generated resume not found")

    content = analysis.generated_resume_text
    
    # If JSON formatted string, try to clean it up slightly or just return as is (user wants text)
    # But mostly we expect plain text now from the Prompt.
    
    return Response(content=str(content), media_type="text/plain", headers={"Content-Disposition": f"attachment; filename=resume_{analysis_id}.txt"})
