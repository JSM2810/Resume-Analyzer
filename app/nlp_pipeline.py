import re
import spacy
from rapidfuzz import fuzz
from pathlib import Path

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = text.replace(".", " ")
    return text.strip().lower()

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

SKILLS_PATH = Path("data/skills_list.txt")

def load_skills(path=SKILLS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return [s.strip().lower() for s in f if s.strip()]

def extract_skills(cleaned_text, skills_list, threshold=80):
    found = set()

    for skill in skills_list:
        if skill in cleaned_text:
            found.add(skill)
        else:
            score = fuzz.partial_ratio(skill, cleaned_text)
            if score >= threshold:
                found.add(skill)

    return sorted(found)

CRITICAL_SKILLS = {
    "python",
    "sql",
    "machine learning",
    "java"
}

def analyze_skill_gap(matched_skills, role_skills):
    matched = set(matched_skills)
    role = set(role_skills)

    missing = list(role - matched)

    critical_missing = [s for s in missing if s in CRITICAL_SKILLS]
    optional_missing = [s for s in missing if s not in CRITICAL_SKILLS]

    return {
        "matched": list(matched),
        "missing": missing,
        "critical_missing": critical_missing,
        "optional_missing": optional_missing
    }

def generate_suggestions(skill_gap):
    suggestions = []

    if skill_gap["critical_missing"]:
        suggestions.append(
            f"Focus first on critical skills: {', '.join(skill_gap['critical_missing'])}"
        )

    if skill_gap["optional_missing"]:
        suggestions.append(
            f"Consider learning: {', '.join(skill_gap['optional_missing'])}"
        )

    if not suggestions:
        suggestions.append(
            "Excellent match! Your resume aligns well with the job role."
        )

    return suggestions
def build_resume_scores(resume_names, similarity_scores):
    results = []

    for name, score in zip(resume_names, similarity_scores):
        results.append({
            "resume": name,
            "score": round(score * 100, 2)
        })

    return results
def rank_resumes(results):
    ranked = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    for idx, res in enumerate(ranked, start=1):
        res["rank"] = idx

    return ranked
