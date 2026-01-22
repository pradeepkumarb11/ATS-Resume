from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.ranking import Ranking
from app.services import ranking_engine

router = APIRouter(prefix="/rank", tags=["Ranking"])

@router.post("/jd/{jd_id}")
def rank_candidates(
    jd_id: int, 
    resume_ids: List[int] = Body(embed=True), 
    db: Session = Depends(get_db)
):
    # 1. Fetch JD
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job Description not found")
        
    # 2. Fetch Resumes
    resumes = db.query(Resume).filter(Resume.id.in_(resume_ids)).all()
    if not resumes:
        raise HTTPException(status_code=404, detail="No resumes found")
        
    # 3. Run Ranking Engine
    results = ranking_engine.rank_resumes(jd, resumes)
    
    # 4. Save to DB (Upsert logic or cleaner replace)
    # Ideally checking if ranking exists and updating, or creating new.
    # For simplicity, we'll create new records. In prod, use ON CONFLICT DO UPDATE.
    
    # Clear old rankings for this JD/Resume combo if needed? 
    # Let's just append for history or update if we implement unique constraints.
    # Assuming user wants latest snapshot.
    
    saved_rankings = []
    for res in results:
        # Check if exists
        existing = db.query(Ranking).filter(
            Ranking.jd_id == jd.id, 
            Ranking.resume_id == res["resume_id"]
        ).first()
        
        if existing:
            existing.score = res["ats_score"]
            existing.rank_position = res["rank_position"]
        else:
            new_ranking = Ranking(
                jd_id=jd.id,
                resume_id=res["resume_id"],
                score=res["ats_score"],
                rank_position=res["rank_position"]
            )
            db.add(new_ranking)
            
    db.commit()
    
    return results
