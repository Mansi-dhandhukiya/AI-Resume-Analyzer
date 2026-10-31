
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_skill_match(resume_skills, jd_skills):

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched_skills = sorted(resume_set.intersection(jd_set))

    missing_skills = sorted(jd_set - resume_set)

    extra_skills = sorted(resume_set - jd_set)

    if len(jd_set) == 0:
        skill_score = 0
    else:
        skill_score = (len(matched_skills) / len(jd_set)) * 100

    return {
        "skill_score": round(skill_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }


def calculate_similarity(resume_text, jd_text):
    # Check for empty input
    if not resume_text or not jd_text:
        return 0.0

    resume_text = resume_text.strip()
    jd_text = jd_text.strip()

    if not resume_text or not jd_text:
        return 0.0

    try:
        # Convert text into numerical vectors
        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform([
            resume_text,
            jd_text
        ])

        # Calculate cosine similarity
        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(float(similarity * 100), 2)

    except ValueError:
        # Handle text with no meaningful vocabulary
        return 0.0


def analyze_resume(resume_text, jd_text, resume_skills, jd_skills):

    skill_result = calculate_skill_match(
        resume_skills,
        jd_skills
    )

    similarity_score = calculate_similarity(
        resume_text,
        jd_text
    )

    final_score = (
        0.60 * skill_result["skill_score"]
        + 0.40 * similarity_score
    )

    return {
        "final_score": round(final_score, 2),
        "skill_score": skill_result["skill_score"],
        "similarity_score": similarity_score,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "extra_skills": skill_result["extra_skills"]
    }
