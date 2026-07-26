from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import shutil
import os
import json

from resume_parser import extract_resume_text, normalize_text
from jd_handler import validate_jd
from models import StylePreference, ResumeFitContent
from generator import generate_cover_letter

app = FastAPI(title="CoverCraft API")

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

@app.get("/")
def read_root():
    return {"status": "CoverCraft API is running."}


@app.post("/generate")
def generate(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    tone: str = Form("formal"),
    length: str = Form("brief"),
    confidence: str = Form("assertive"),
):
    _, ext = os.path.splitext(resume.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type '{ext}'. Please upload a .pdf or .docx file.")

    temp_path = f"temp_{resume.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    try:
        raw_text = extract_resume_text(temp_path)

        if not raw_text or not raw_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the resume. It may be a scanned/image-based file.")

        resume_text = normalize_text(raw_text)

        try:
            cleaned_jd = validate_jd(jd_text)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        try:
            style = StylePreference(tone=tone, length=length, confidence=confidence)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid style preferences: {e}")

        try:
            result = generate_cover_letter(resume_text, cleaned_jd, style)
        except (RuntimeError, ValueError) as e:
            raise HTTPException(status_code=502, detail=f"Generation failed: {e}")

    finally:
        os.remove(temp_path)

    return result