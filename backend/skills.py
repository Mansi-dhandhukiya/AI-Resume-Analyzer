
import json
import spacy
from spacy.matcher import PhraseMatcher
from pathlib import Path


# Load English NLP pipeline
nlp = spacy.blank("en")


# Load skills dictionary
def load_skills():

    file_path = Path(__file__).with_name("skills.json")

    with open(file_path, "r", encoding="utf-8") as file:
        skills_data = json.load(file)

    return skills_data


# Create PhraseMatcher
def create_matcher():

    skills_data = load_skills()

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    for skill, synonyms in skills_data.items():

        patterns = [nlp.make_doc(skill)]

        for synonym in synonyms:
            patterns.append(nlp.make_doc(synonym))

        matcher.add(skill, patterns)

    return matcher


# Extract skills from text
def extract_skills(text):

    matcher = create_matcher()

    doc = nlp(text)

    matches = matcher(doc)

    found_skills = []

    for match_id, start, end in matches:

        skill = nlp.vocab.strings[match_id]

        if skill not in found_skills:
            found_skills.append(skill)

    return found_skills
