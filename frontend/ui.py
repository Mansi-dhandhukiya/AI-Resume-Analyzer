
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: black;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

.hero {
    background:linear-gradient(162deg, #0d1965, #491147);
    padding: 38px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
}

.hero h1 {
    color: white;
    font-size: 36px;
    margin-bottom: 10px;
}

.hero p {
    color: #e0e2ff;
    font-size: 16px;
}

.section-title {
    
    font-size: 20px;
    font-weight: 700;
    color: #3e66dd;
    margin-top: 10px;
    margin-bottom: 10px;
}

.info-card {
    background: white;
    padding: 23px;
    border-radius: 15px;
    border: 1px solid #e5e8f1;
    margin-bottom: 18px;
}

.score-card {
    background: white;
    border: 1px solid #e5e8f1;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
}

.score-label {
    color: #69718a;
    font-size: 14px;
}

.score-value {
     background: white;
    color: #5141a5;
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}

.skill-card {
    background: white;
    border: 1px solid #e5e8f1;
    border-radius: 15px;
    padding: 20px;
    min-height: 150px;
    margin-bottom: 12px;
    
}

.skill-card h4 {
    color: #252d4b;
    margin-bottom: 15px;
}

.skill-card p {
    
    color: #525b72;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #8990a5;
    margin-top: 45px;
    font-size: 13px;
}

.stButton > button {
    background: linear-gradient(120deg, #171c3b, #620073);
    color: black;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: 700;
    width: 100%;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #392c83;
    color: white;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>📄 AI Resume Analyzer</h1>
    <p>
        Make your next career move with confidence.
        Analyze your resume, discover skill gaps,
        and improve your job readiness.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- INPUT SECTION ----------------


left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown(
        '<div class="section-title">📎Upload Resume</div>',
        unsafe_allow_html=True
    )

    resume_file = st.file_uploader(
        "Choose your PDF resume",
        type=["pdf"],
        help="Upload a PDF file up to 5 MB."
    )

    if resume_file:
        st.success(f"Uploaded: {resume_file.name}")

with right:
    st.markdown(
        '<div class="section-title">💼 Job Description</div>',
        unsafe_allow_html=True
    )

    jd_text = st.text_area(
        "Paste the job description",
        height=190,
        placeholder="Paste the complete job description here..."
    )


# ---------------- ANALYZE BUTTON ----------------

st.write("")

analyze_button = st.button(
    "✨ Analyze My Resume",
    use_container_width=True
)


# ---------------- ANALYSIS ----------------

if analyze_button:

    if resume_file is None:
        st.warning("Please upload your PDF resume.")

    elif not jd_text.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume... Please wait"):

                # Upload PDF
                files = {
                    "file": (
                        resume_file.name,
                        resume_file.getvalue(),
                        "application/pdf"
                    )
                }

                upload_response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=60
                )

                upload_response.raise_for_status()

                resume_data = upload_response.json()
                resume_text = resume_data["resume_text"]

                # Analyze resume
                payload = {
                    "resume_text": resume_text,
                    "jd_text": jd_text
                }

                analysis_response = requests.post(
                    f"{API_URL}/analyze",
                    json=payload,
                    timeout=60
                )

                analysis_response.raise_for_status()

                result = analysis_response.json()

            st.success("Your resume has been analyzed successfully!")

            # ---------------- SCORE DASHBOARD ----------------

            st.markdown(
                '<div class="section-title">📊 Analysis Overview</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="score-card">
                    <div class="score-label">Overall Match Score</div>
                    <div class="score-value">
                        {result['final_score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="score-card">
                    <div class="score-label">Skill Match Score</div>
                    <div class="score-value">
                        {result['skill_score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="score-card">
                    <div class="score-label">Text Similarity</div>
                    <div class="score-value">
                        {result['similarity_score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            score = max(0, min(result["final_score"], 100))

            st.write("")

            st.markdown("**Overall Resume Match**")

            st.progress(score / 100)

            # ---------------- SKILL ANALYSIS ----------------

            st.markdown(
                '<div class="section-title">🎯 Skills Analysis</div>',
                unsafe_allow_html=True
            )

            matched = result["matched_skills"]
            missing = result["missing_skills"]
            extra = result["extra_skills"]

            s1, s2, s3 = st.columns(3)

            with s1:
                st.markdown(f"""
                <div class="skill-card">
                    <h4>✅ Matched Skills ({len(matched)})</h4>
                    <p>{", ".join(matched) if matched else "No matched skills found."}</p>
                </div>
                """, unsafe_allow_html=True)

            with s2:
                st.markdown(f"""
                <div class="skill-card">
                    <h4>❌ Missing Skills ({len(missing)})</h4>
                    <p>{", ".join(missing) if missing else "No missing skills found."}</p>
                </div>
                """, unsafe_allow_html=True)

            with s3:
                st.markdown(f"""
                <div class="skill-card">
                    <h4>⭐Extra Skills ({len(extra)})</h4>
                    <p>{", ".join(extra) if extra else "No extra skills found."}</p>
                </div>
                """, unsafe_allow_html=True)

            # ---------------- SUGGESTION ----------------

            st.markdown(
                '<div class="section-title">💡Improvement Tip</div>',
                unsafe_allow_html=True
            )

            if missing:
                st.info(
                    "Consider learning or demonstrating these missing skills: "
                    + ", ".join(missing)
                )
            else:
                st.success(
                    "All detected job-description skills are present in your resume!"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to FastAPI. "
                "Please start your backend server."
            )

        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    AI Resume Analyzer &copy; 2024. All rights reserved.
</div>
""", unsafe_allow_html=True)
