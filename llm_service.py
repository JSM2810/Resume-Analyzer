import json
import requests

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3"   


def load_role_data():
    with open("data/job_roles.json", "r") as f:
        return json.load(f)


def build_pseudo_jd(role_name):
    roles = load_role_data()

    if role_name not in roles:
        return None

    role = roles[role_name]

    jd_text = f"""
Role: {role_name}

Responsibilities:
{chr(10).join(['- ' + r for r in role['responsibilities']])}

Required Skills:
{chr(10).join(['- ' + s for s in role['required_skills']])}

Tools & Technologies:
{chr(10).join(['- ' + t for t in role['tools']])}
"""
    return jd_text


def generate_career_feedback(resume_text, role_name=None, match_percentage=None, missing_skills=None):

    jd_text = build_pseudo_jd(role_name)

    prompt = f"""
You are an expert AI Career Advisor.

{jd_text}

{resume_text}

Current Match Percentage: {match_percentage}%
Missing Skills Identified: {missing_skills}

Provide a structured response:

1. Overall Match Evaluation
2. Key Strengths Aligned With Role
3. Skill Gap Analysis
4. Why Missing Skills Matter For This Role
5. Step-by-Step Improvement Plan
6. 30-Day Learning Roadmap
7. Final Hiring Readiness Verdict

Be professional, realistic, and actionable.
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )
    except:
        return "⚠️ AI service is not running. Please start Ollama."

    return response.json()["response"]