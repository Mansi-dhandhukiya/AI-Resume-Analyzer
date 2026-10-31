
from backend.skills import extract_skills


def test_extract_java_and_python():
    skills = extract_skills(
        "I have experience in Java and Python."
    )

    assert "Java" in skills
    assert "Python" in skills


def test_extract_spring_boot():
    skills = extract_skills(
        "I have worked with Spring Boot."
    )

    assert "Spring Boot" in skills


def test_empty_text():
    skills = extract_skills("")

    assert skills == []
