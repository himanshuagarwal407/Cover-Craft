# CoverCraft

Part of the **JobPilot** project series — a multi-agent job search assistant.

## What this does
Takes a resume, a job description, and a few style preferences, and generates:
- A tailored cover letter
- Rewritten resume bullet points aligned to the job description

## Status
🚧 In development — Project 3 of 5 in the JobPilot series.

## Approach
This version uses **style-guided prompting** rather than RAG over personal writing samples — the user selects preferences (tone, length, confidence level) which shape the generation prompt directly. A RAG-based version using real writing samples for authentic voice-matching is a planned future enhancement once sample data is available.

## Tech Stack
- **Backend:** Python, FastAPI
- **LLM:** Google Gemini API
- **Frontend:** Gradio
- **Parsing:** pdfplumber / python-docx (reused from ResumeFitCheck)

## Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # add your Gemini API key
uvicorn main:app --reload
```

### Frontend
```bash
python app.py
```

## Environment Variables
See `.env.example` for required keys.

## Part of JobPilot
This is one of five standalone sub-projects that combine into the final **JobPilot** multi-agent system:
1. ResumeFitCheck — resume/JD scoring
2. JobScout — job search & recommendations
3. **CoverCraft** (this repo) — AI cover letter writer
4. ApplyTrack — application tracker
5. JobPilot — final orchestration of all agents
