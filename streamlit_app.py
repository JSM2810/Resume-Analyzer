import streamlit as st
import tempfile
import os
import json
from llm_service import generate_career_feedback

from app.parser import parse_file
from app.nlp_pipeline import clean_text, extract_skills, load_skills
from app.matcher import rank_resumes_by_job, explain_match
from app.skill_gap import compute_skill_gap, prioritize_missing_skills
from app.suggestions import generate_suggestions

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 Resume Analyzer – See How Well Your Resume Fits a Job")

skills_list = load_skills()

with open("data/job_roles.json", "r") as f:
    roles = json.load(f)

selected_role = st.selectbox("Select Target Role", list(roles.keys()))

uploaded_files = st.file_uploader(
    "📤 Upload Your Resume(s) to Analyze (PDF/DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if st.button("🔍 Analyze Resume"):

    if not uploaded_files:
        st.warning("Please upload at least one resume to start the analysis.")
    else:

        resumes_texts = []
        filenames = []

        for f in uploaded_files:
            content = f.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f.name)[1]) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            text = parse_file(tmp_path, f.name)
            cleaned = clean_text(text)

            resumes_texts.append(cleaned)
            filenames.append(f.name)

        st.subheader("🏆 Resume Match Results")

        role_data = roles[selected_role]
        job_skills = role_data["required_skills"]

        for idx in range(len(resumes_texts)):

            st.markdown("---")
            st.markdown(f"### 📄 {filenames[idx]}")

            resume_text = resumes_texts[idx]
            resume_skills = extract_skills(resume_text, skills_list)

            result = explain_match(resume_skills, job_skills)

            gap = compute_skill_gap(resume_skills, job_skills)
            priority = prioritize_missing_skills(gap["missing"])
            suggestions = generate_suggestions(priority)

            match_percent = result["match_percent"]

            st.markdown("#### 🎯 Resume Match Score")
            st.write(f"**Match Score:** {match_percent}%")
            st.progress(match_percent / 100)

            st.markdown("#### 📊 Skill Gap Analysis")

            st.markdown("**✅ Matched Skills**")
            st.write(", ".join(gap["matched"]) if gap["matched"] else "None")

            st.markdown("**❌ Missing Skills**")
            st.write(", ".join(gap["missing"]) if gap["missing"] else "None")

            st.markdown("**➕ Extra Skills**")
            st.write(", ".join(gap["extra"]) if gap["extra"] else "None")

            st.markdown("#### 🚦 Importance of Missing Skills")

            st.error("🔥 High Priority")
            st.write(", ".join(priority["high_priority"]) if priority["high_priority"] else "None")

            st.warning("⚠️ Medium Priority")
            st.write(", ".join(priority["medium_priority"]) if priority["medium_priority"] else "None")

            st.info("ℹ️ Low Priority")
            st.write(", ".join(priority["low_priority"]) if priority["low_priority"] else "None")

            st.markdown("#### 💡 Suggestions")
            for s in suggestions:
                st.info(s)

            missing_skills_str = ", ".join(gap["missing"]) if gap["missing"] else "None"

            with st.spinner("Generating AI Career Feedback..."):
                ai_feedback = generate_career_feedback(
                    resume_text=resume_text,
                    role_name=selected_role,
                    match_percentage=match_percent,
                    missing_skills=missing_skills_str
                )

            st.markdown("#### 🤖 AI Career Feedback")
            st.write(ai_feedback)