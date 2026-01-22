from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job_description import JobDescription
from app.schemas.job_description import JDCreate, JDResponse

router = APIRouter(prefix="/jds", tags=["Job Descriptions"])

@router.post("/create", response_model=dict)
def create_jd(jd: JDCreate, db: Session = Depends(get_db)):
    db_jd = JobDescription(role=jd.role, jd_text=jd.jd_text)
    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)
    return {"jd_id": db_jd.id}

@router.get("/{jd_id}", response_model=JDResponse)
def get_jd(jd_id: int, db: Session = Depends(get_db)):
    db_jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not db_jd:
        raise HTTPException(status_code=404, detail="Job Description not found")
    return db_jd
