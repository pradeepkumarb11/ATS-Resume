from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    score = Column(Float)
    rank_position = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job_description = relationship("app.models.job_description.JobDescription")
    resume = relationship("app.models.resume.Resume")
