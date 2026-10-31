# AI Resume Analyzer

An intelligent resume analysis application that compares a candidate's resume with a job description and identifies matching skills, missing skills, and overall relevance.

## Overview

AI Resume Analyzer helps job seekers understand how well their resumes match a particular job description.

Users can upload a PDF resume, enter a job description, and receive an analysis containing:
- Overall resume match score
- Skill match percentage
- Text similarity percentage
- Matched skills
- Missing skills
- Additional skills

## Features

- PDF resume upload
- Automatic text extraction using PDFPlumber
- Skill extraction using spaCy PhraseMatcher
- Resume and job description comparison
- TF-IDF text similarity calculation
- Cosine similarity scoring
- Matched, missing, and additional skill identification
- Interactive Streamlit interface
- FastAPI backend
- Input validation and error handling

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend API |
| Streamlit | Frontend interface |
| spaCy | Skill extraction |
| Scikit-learn | TF-IDF and cosine similarity |
| PDFPlumber | PDF text extraction |
| Pytest | Automated testing |

## Project Structure

```text
AI-Resume-Analyzer/
│
├── backend/
│   ├── main.py
│   ├── parser.py
│   ├── skills.py
│   ├── matcher.py
│   └── skills.json
│
├── frontend/
│   └── ui.py
│
├── tests/
│   ├── test_matcher.py
│   ├── test_skills.py
│   └── test_parser.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 6. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/ui.py
```

## How It Works

1. The user uploads a PDF resume.
2. PDFPlumber extracts text from the resume.
3. spaCy PhraseMatcher identifies technical skills.
4. The user enters a job description.
5. The application extracts skills from the job description.
6. Skill matching identifies matched and missing skills.
7. TF-IDF converts resume and job description text into numerical vectors.
8. Cosine similarity calculates text similarity.
9. The application displays the analysis results.

## Matching Algorithm

The application calculates its final score using:

**Final Score = (Skill Match Score × 0.60) + (Text Similarity × 0.40)**

This is a heuristic matching score, not a prediction of hiring probability.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend health check |
| POST | `/upload` | Upload and extract resume text |
| POST | `/analyze` | Analyze resume against job description |

## Testing

Run automated tests using:

```bash
python -m pytest -v
```

## Limitations

- Currently supports PDF resumes.
- Scanned PDFs require OCR support, which is not currently implemented.
- Skill detection depends on the skills database.
- The match score is an estimated similarity metric and does not guarantee job selection.

## Future Improvements

- Add OCR support for scanned resumes.
- Extract candidate information such as name, email, and phone number.
- Add more technical skills and synonyms.
- Improve skill matching accuracy.
- Add resume improvement suggestions.
- Deploy the application online.

## Author

Developed as a Python and Machine Learning portfolio project.

---

**AI Resume Analyzer — Analyze your resume. Identify skill gaps. Improve your opportunities.**