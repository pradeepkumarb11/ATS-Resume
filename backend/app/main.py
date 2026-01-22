from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routes import jds, analysis, ranking, llm, resumes, reports

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Checker & Optimizer")

origins = ["*"]
if settings.APP_URL and settings.APP_URL != "http://localhost:8501":
    origins.append(settings.APP_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows localhost and production frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jds.router)
app.include_router(resumes.router)
app.include_router(analysis.router)
app.include_router(ranking.router)
app.include_router(llm.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"message": "ATS Resume Backend Running"}
