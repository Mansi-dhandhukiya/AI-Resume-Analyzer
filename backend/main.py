
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, field_validator

from backend.parser import parse_resume
from backend.skills import extract_skills
from backend.matcher import analyze_resume

import tempfile
import os


# Create FastAPI application
app = FastAPI(
    title="AI Resume Analyzer",
    description="Analyze resume against job description",
    version="1.0.0"
)


# Home API
@app.get("/")
def home():

    return {
        "message": "AI Resume Analyzer API is running successfully!"
    }


# Upload Resume API
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Check PDF extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="PDF file must be smaller than 5 MB."
        )

    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file."
        )

    temp_path = None

    try:

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        # Extract resume text
        resume_text = parse_resume(temp_path)

        # Extract skills
        skills = extract_skills(resume_text)

        return {
            "filename": file.filename,
            "resume_text": resume_text,
            "skills": skills
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to process the resume."
        )

    finally:

        # Delete temporary PDF
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# Request body for analysis
class AnalyzeRequest(BaseModel):

    resume_text: str = Field(min_length=1)
    jd_text: str = Field(min_length=1)
    @field_validator("resume_text", "jd_text")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Text cannot be empty or contain only spaces")
        return value


# Resume Analysis API
@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:

        # Extract skills from resume
        resume_skills = extract_skills(
            request.resume_text
        )

        # Extract skills from job description
        jd_skills = extract_skills(
            request.jd_text
        )

        # Compare resume and job description
        result = analyze_resume(
            request.resume_text,
            request.jd_text,
            resume_skills,
            jd_skills
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
