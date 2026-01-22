# AI Resume Checker & Optimizer

A comprehensive AI-powered Application Tracking System (ATS) simulator and Resume Optimizer. This tool helps candidates tailor their resumes to specific Job Descriptions (JDs) and helps recruiters rank candidates efficiently.

## 🚀 Features

### Core Functionality
- **ATS Scoring Engine**: intelligent rule-based scoring of resumes against JDs (Skills, Experience, Similarity, Education).
- **Resume Parsing**: Supports PDF and DOCX formats.
- **Skill Extraction**: Extracts technical skills using a comprehensive master list and regex patterns.
- **Job Description Management**: Store and analyze against multiple JDs.

### AI & LLM Integration (OpenRouter)
- **Bullet Rewriting**: Context-aware rewriting of experience bullets to match JD keywords.
- **Summary Generation**: AI-generated professional summaries tailored to the target role.
- **Full Resume Generation**: Generates a complete, optimized resume draft in **Plain Text ATS Standard Format** (replaces JSON).

### Reporting
- **PDF Reports**: Download detailed analysis reports with scores and recommendations.
- **PDF Resumes**: Download the AI-optimized resume as a clean PDF.
- **Text Resumes**: Download the AI-optimized resume as a `.txt` file.

### Frontend
- **Streamlit UI**: Clean, interactive interface for all user roles (Candidate & Recruiter).
- **Interactive Dashboards**: Gauge charts for scores, side-by-side skill comparison.

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL (Production) / SQLite (Dev)
- **Frontend**: Streamlit
- **AI/LLM**: OpenRouter API (Access to Deepseek, Gemma, Llama, etc.)
- **PDF Processing**: PyPDF2, ReportLab

---

## ⚙️ Configuration

### Environment Variables (.env)
Create a `.env` file in the `backend/` directory:

```env
# Database (SQLite for local, Postgres for prod)
DATABASE_URL=sqlite:///./sql_app.db

# LLM Configuration (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=google/gemma-2-9b-it  # or deepseek/deepseek-chat

# Application URLs
APP_URL=http://localhost:8501
```

---

## 🚀 Running Locally

### 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
*Server runs at `http://localhost:8000`*

### 2. Frontend (Streamlit)

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```
*App runs at `http://localhost:8501`*

---

## ☁️ Deployment Guide

### Backend: Render.com + Neon.tech (PostgreSQL)

1. **Database**: Create a project on [Neon.tech](https://neon.tech) and get the Postgres Connection String.
2. **Hosting**: Create a Web Service on [Render](https://render.com).
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Env Vars**: Set `DATABASE_URL` (from Neon), `OPENROUTER_API_KEY`, etc.

### Frontend: Streamlit Community Cloud

1. **Deploy**: Connect your GitHub repo to [Streamlit Cloud](https://share.streamlit.io).
2. **Main File**: `frontend/streamlit_app.py`
3. **Secrets**: Add `BACKEND_URL` in the app's "Secrets" settings:
   ```toml
   BACKEND_URL = "https://your-render-backend.onrender.com"
   ```

---

## 📂 Project Structure

```
p:/Projects/ATS Resume/
├── backend/
│   ├── app/
│   │   ├── main.py          # App entry point
│   │   ├── routes/          # API Endpoints (jds, ranking, analysis, llm)
│   │   ├── services/        # Business Logic (ats_engine, openrouter)
│   │   ├── models/          # DB Models
│   │   └── utils/           # Helpers (skills extraction)
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py     # Main UI
│   ├── pages/               # Sub-pages (Upload, Report, Ranking)
│   ├── utils/               # API Client
│   └── requirements.txt
└── README.md
```
