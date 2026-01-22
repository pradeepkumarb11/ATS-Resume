from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.resume import Resume
from pydantic import BaseModel
import PyPDF2
import docx
import io

router = APIRouter(prefix="/resumes", tags=["Resumes"])

class ResumeResponse(BaseModel):
    id: int
    filename: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    content = await file.read()
    filename = file.filename
    text_content = ""
    
    # Simple extraction logic
    try:
        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
        elif filename.endswith(".docx"):
            doc = docx.Document(io.BytesIO(content))
            for para in doc.paragraphs:
                text_content += para.text + "\n"
        else:
            # Assume text or ignore
            text_content = content.decode("utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")
    
    # Clean text
    text_content = text_content.strip()
    
    db_resume = Resume(
        filename=filename,
        file_path="memory", # Not saving to disk for now
        resume_text=text_content
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return ResumeResponse(
        id=db_resume.id, 
        filename=db_resume.filename, 
        created_at=str(db_resume.created_at)
    )

@router.get("/", response_model=list[ResumeResponse])
def get_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).order_by(Resume.created_at.desc()).all()
    # Manual map or let Pydantic handle it
    return [
        ResumeResponse(id=r.id, filename=r.filename, created_at=str(r.created_at)) 
        for r in resumes
    ]
