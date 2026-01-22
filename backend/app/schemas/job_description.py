from pydantic import BaseModel
from datetime import datetime

class JDBase(BaseModel):
    role: str
    jd_text: str

class JDCreate(JDBase):
    pass

class JDResponse(JDBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
