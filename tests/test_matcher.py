
from backend.matcher import calculate_similarity


def test_empty_resume():
    result = calculate_similarity("", "Java Developer")
    assert result == 0.0


def test_empty_job_description():
    result = calculate_similarity("Java Developer", "")
    assert result == 0.0


def test_identical_text():
    result = calculate_similarity(
        "Java Spring Boot Developer",
        "Java Spring Boot Developer"
    )
    assert result == 100.0


def test_similarity_is_valid_percentage():
    result = calculate_similarity(
        "Java Python Spring Boot",
        "Java Developer"
    )
    assert 0.0 <= result <= 100.0
