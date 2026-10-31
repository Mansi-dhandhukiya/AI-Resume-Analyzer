
import pdfplumber
import re


def extract_text(pdf_path):
    """
    Extract text from all pages of a PDF resume.
    """

    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    return extracted_text


def clean_text(text):
    """
    Clean unnecessary spaces and special characters.
    """

    # Remove bullet symbols
    text = re.sub(r"[•●▪◦]", " ", text)

    # Replace multiple spaces and newlines with one space
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text


def parse_resume(pdf_path):
    """
    Extract and clean resume text.
    """

    text = extract_text(pdf_path)

    if not text.strip():
        raise ValueError("No readable text found in PDF.")

    cleaned_text = clean_text(text)

    return cleaned_text
