
import pytest
from backend import parser


def test_clean_text():
    result = parser.clean_text(
        "• Java     Developer\n● Python"
    )

    assert result == "Java Developer Python"


def test_parse_resume_success(monkeypatch):
    monkeypatch.setattr(
        parser,
        "extract_text",
        lambda path: "Java Developer"
    )

    result = parser.parse_resume("resume2.pdf")

    assert result == "Java Developer"


def test_parse_empty_resume(monkeypatch):
    monkeypatch.setattr(
        parser,
        "extract_text",
        lambda path: "   "
    )

    with pytest.raises(ValueError):
        parser.parse_resume("resume2.pdf")
