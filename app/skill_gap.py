CRITICAL_SKILLS = {
    "python", "sql", "machine learning", "java",
    "data structures", "react", "javascript"
}

def compute_skill_gap(resume_skills, job_skills):
    resume_set = set([s.lower().strip() for s in resume_skills])
    job_set = set([s.lower().strip() for s in job_skills])

    matched_skills = sorted(resume_set & job_set)
    missing_skills = sorted(job_set - resume_set)
    extra_skills = sorted(resume_set - job_set)

    return {
        "matched": matched_skills,
        "missing": missing_skills,
        "extra": extra_skills
    }


def analyze_missing_skills(missing_skills):
    critical_missing = [s for s in missing_skills if s in CRITICAL_SKILLS]
    optional_missing = [s for s in missing_skills if s not in CRITICAL_SKILLS]

    return {
        "critical_missing": critical_missing,
        "optional_missing": optional_missing
    }
HIGH_PRIORITY_SKILLS = {
    "python", "sql", "machine learning", "data structures",
    "react", "javascript"
}
MEDIUM_PRIORITY_SKILLS = {
    "docker","aws","git","linux","rest api"
}

def prioritize_missing_skills(missing_skills):
    high=[]
    medium=[]
    low=[]

    for skill in missing_skills:
        s=skill.lower()
        if s in HIGH_PRIORITY_SKILLS:
            high.append(skill)
        elif s in MEDIUM_PRIORITY_SKILLS:
            medium.append(skill)
        else:
            low.append(skill)
    return {
        "high_priority":high,
        "medium_priority":medium,
        "low_priority":low
    }