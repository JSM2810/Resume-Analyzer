import streamlit as st
import tempfile
import os

from app.parser import parse_file
from app.nlp_pipeline import clean_text, extract_skills, load_skills
from app.matcher import rank_resumes_by_job, explain_match
from app.skill_gap import compute_skill_gap, prioritize_missing_skills
from app.suggestions import generate_suggestions

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 Resume Analyzer – See How Well Your Resume Fits a Job")

skills_list = load_skills()
job_description = st.text_area(
    "🎯 Paste the Job Description You’re Targeting",

    height=200,
    placeholder=(
        "Paste the full job description you are applying for.\n\n"

        "Example:\n"
        "• Software Developer Intern\n"
        "• Skills: Python, SQL, Git, Data Structures\n"
        "• Basic knowledge of APIs and databases"
    ),
    help="This is used to check how well your resume matches the role and what skills you are missing."
)

uploaded_files = st.file_uploader(
    "📤 Upload Your Resume(s) to Analyze (PDF/DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True,
    help="Upload your resume to analyze how well it matches the target job role"
)
if st.button("🔍 Analyze Resume"):

    if not job_description or not uploaded_files:
        st.warning("Please upload at least one resume and paste a job description to start the analysis.")

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

        rankings = rank_resumes_by_job(
            resumes_texts,
            job_description,
            top_k=len(resumes_texts)
        )

        st.subheader("🏆 Resume Match Results")
        job_skills = extract_skills(job_description, skills_list)
        
        if not job_skills:
            st.error("No skills detected in job description. Please add explicit skills.")
            st.stop()

        for idx, score in rankings:
            st.markdown("---")
            st.markdown(f"### 📄 {filenames[idx]}")
        
        
            resume_skills = extract_skills(resumes_texts[idx], skills_list)

            result = explain_match(resume_skills, job_skills)

            gap = compute_skill_gap(resume_skills, job_skills)
            priority = prioritize_missing_skills(gap["missing"])


            priority = prioritize_missing_skills(gap["missing"])
            suggestions = generate_suggestions(priority)

            st.markdown("#### 🎯 Resume Match Score")
            st.write(f"**Match Score:** {result['match_percent']}%")
            match_percent = result["match_percent"]

            st.progress(match_percent / 100)
            st.markdown(f"### ✅ {match_percent}% Match with Target Role")

            st.write(
                f"Your resume matches **{match_percent}%** of the required skills for this role."
                )       

            st.markdown("#### 🧠 Resume Strength Summary")

            if match_percent >= 75:
                st.success(
        "Your resume is **strongly aligned** with the target role. "
        "You meet most of the required skills and appear job-ready."
    )
            elif match_percent >= 40:
                st.info(
        "Your resume shows **partial alignment** with the target role. "
        "Adding a few missing skills can significantly improve your match."
    )
            else:
                st.warning(
        "Your resume currently shows **low alignment** with the target role. "
        "This may be due to missing skills or an unclear job description."
    )

            st.markdown("#### 📊 Skill Comparison with Job Requirements")


            st.markdown("**❌ Skills Missing for This Role**")
            st.write(", ".join(result["missing_skills"]) if result["missing_skills"] else "No missing skills detected")


            st.markdown("#### 📊 Skill Gap Analysis")

            st.markdown("**✅ Matched Skills**")
            st.write(", ".join(gap["matched"]) if gap["matched"] else "None")

            st.markdown("**❌ Missing Skills**")
            st.write(", ".join(gap["missing"]) if gap["missing"] else "None")

            st.markdown("**➕ Extra Skills**")
            st.write(", ".join(gap["extra"]) if gap["extra"] else "None")   

            st.markdown("#### 🚦 Importance of Missing Skills")

            st.error("🔥 High Priority (Must-have for this job)")
            st.write(", ".join(priority["high_priority"]) if priority["high_priority"] else "None")

            st.warning("⚠️ Medium Priority(Good to have)")
            st.write(", ".join(priority["medium_priority"]) if priority["medium_priority"] else "None") 
            st.info("ℹ️ Low Priority (Optional)")
            st.write(", ".join(priority["low_priority"]) if priority["low_priority"] else "None")


            st.markdown("**💡 What You Should Do Next**")
            for s in suggestions:
                st.info(s)
