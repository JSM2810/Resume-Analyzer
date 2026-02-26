from sentence_transformers import SentenceTransformer, util
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from pathlib import Path

SKILLS_FILE=Path("data/skills_list.txt")

def load_skills():
    with open (SKILLS_FILE, "r", encoding="utf-8")as f:
        return[line.strip().lower() for line in f if line.strip()]
    
def extract_skills(text,skills_list):
    text = text.lower()
    found_skills = set()

    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    return list(found_skills)

model = SentenceTransformer("all-MiniLM-L6-v2")  

def embed_texts(texts):
    return model.encode(texts, convert_to_tensor=True, show_progress_bar=False)

def rank_resumes_by_job(resume_texts, job_text, top_k=5):
    job_emb = embed_texts([job_text])
    resume_embs = embed_texts(resume_texts)
    cos_scores = util.cos_sim(job_emb, resume_embs)[0].cpu().numpy()
    idxs = np.argsort(-cos_scores)[:top_k]
    return [(int(i), float(cos_scores[i])) for i in idxs]

def basic_skill_match(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }

CRITICAL_SKILLS = {
    "python",
    "sql",
    "machine learning",
    "java"
}

def classify_skill_gap(missing_skills):
    critical_missing = []
    optional_missing = []

    for skill in missing_skills:
        if skill.lower() in CRITICAL_SKILLS:
            critical_missing.append(skill)
        else:
            optional_missing.append(skill)

    return {
        "critical_missing": critical_missing,
        "optional_missing": optional_missing
    }

def explain_match(resume_skills, job_skills):

    resume_set = set([skill.lower().strip() for skill in resume_skills])
    job_set = set([skill.lower().strip() for skill in job_skills])

    matched = resume_set.intersection(job_set)

    match_percent = 0
    if len(job_set) > 0:
        match_percent = round((len(matched) / len(job_set)) * 100, 2)

    return {
        "matched": list(matched),
        "match_percent": match_percent
    }

def calculate_match_score(resume_text, job_description_text):
    vectorizer = TfidfVectorizer()

    documents = [resume_text, job_description_text]
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_matrix = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    raw_score = float(similarity_matrix[0][0])
    match_percentage = round(raw_score * 100, 2)

    def classify_match(score):
        if score >= 75:
            return "Excellent Match"
        elif score >= 50:
            return "Good Match"
        elif score >= 30:
            return "Average Match"
        else:
            return "Poor Match"

    match_level = classify_match(match_percentage)

    return {
        "match_percentage": match_percentage,
        "match_level": match_level,
        "raw_similarity_score": raw_score
    }
