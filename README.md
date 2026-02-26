# 🚀 Resume Analyzer  
AI-Powered Role-Based Resume Matching & Career Feedback System

---

## 📌 Project Overview

Recruiters often screen resumes in seconds or through automated systems.  
This project helps candidates evaluate how well their resume aligns with a target role — even without providing a detailed job description.

The system uses Natural Language Processing (NLP), structured role intelligence, and AI-powered feedback to:

- Calculate resume match scores  
- Identify skill gaps  
- Prioritize missing skills  
- Generate structured AI career feedback  
- Provide a 30-day improvement roadmap  

Unlike traditional resume matchers, this system can internally generate structured role expectations and evaluate resumes against them.

---

## ✨ Key Features

- ✅ Role-based resume matching (No detailed JD required)  
- ✅ Dynamic pseudo Job Description generation  
- ✅ NLP-based skill extraction  
- ✅ Match score calculation with gap analysis  
- ✅ Missing skill prioritization (High / Medium / Low)  
- ✅ AI-generated structured career feedback  
- ✅ 30-day learning roadmap  
- ✅ Local LLM integration using Ollama (No paid API required)

---

## 🛠️ Tech Stack

### Language
- Python  

### Frontend
- Streamlit  

### Backend
- Modular Python NLP pipeline  

### AI / NLP Libraries
- spaCy  
- Sentence Transformers (MiniLM)  
- scikit-learn  
- RapidFuzz  
- NumPy  
- Ollama (LLaMA3 – Local LLM)

---

## ⚙️ How It Works

### 🔹 Mode 1: Role-Based Matching (Recommended)

1. User selects a target role (e.g., ML Engineer, Frontend Developer)  
2. System loads predefined role templates (skills, tools, responsibilities)  
3. A structured pseudo Job Description is generated internally  
4. Resume skills are extracted using NLP  
5. Match score and skill gap are calculated  
6. AI generates structured career feedback and a 30-day roadmap  

---

### 🔹 Mode 2: Traditional JD Matching

1. User pastes a job description  
2. Skills are extracted from the JD  
3. Resume is compared against extracted skills  
4. Match score and skill gaps are generated  

---

## 🏗️ Architecture

The project follows a modular architecture:

- `parser.py` → Resume parsing  
- `nlp_pipeline.py` → Text cleaning & skill extraction  
- `matcher.py` → Match score calculation  
- `skill_gap.py` → Skill gap computation & prioritization  
- `suggestions.py` → Actionable recommendations  
- `llm_service.py` → AI career feedback via Ollama  
- `job_roles.json` → Role-based configuration file  

This modular design ensures scalability, maintainability, and easy extension for new roles.

---

## 🤖 AI Career Feedback Includes

- Overall match evaluation  
- Key strengths aligned with role  
- Detailed skill gap analysis  
- Why missing skills matter  
- Step-by-step improvement plan  
- 30-day learning roadmap  
- Hiring readiness verdict  

All generated using a locally running LLM.
