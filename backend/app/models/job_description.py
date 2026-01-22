from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)
    jd_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
