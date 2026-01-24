# Resume-Analyzer
NLP-based Resume Analyzer for job matching

---

## Project Overview

Recruiters often screen resumes in seconds or through automated systems.  
This project helps candidates understand how well their resume matches a specific job description and identifies missing or weak skills that need improvement.

The system processes unstructured resume and job description text using Natural Language Processing (NLP) and semantic similarity techniques.

---

## Key Features

- Resume and Job Description similarity scoring  
- Skill and keyword extraction using NLP  
- Semantic matching using sentence embeddings  
- Identification of missing or weak skills  
- Clear and interpretable feedback  

---

## Tech Stack

- **Language:** Python  
- **Frontend:** Streamlit  
- **Backend:** Python-based NLP pipeline  
- **Libraries & Tools:**  
  - spaCy  
  - Sentence Transformers (MiniLM)  
  - scikit-learn  
  - RapidFuzz  
  - NumPy  

---

## How It Works

1. Resume and Job Description are provided as input  
2. Text is cleaned and preprocessed using NLP techniques  
3. Important skills and keywords are extracted  
4. Semantic similarity is calculated using embeddings  
5. A match score and improvement feedback are generated  

---

## Architecture

The project follows a modular architecture where:
- Text preprocessing  
- Skill extraction  
- Similarity calculation  
- Result generation  

are implemented as separate components, making the system easy to maintain and extend.

---

## How to Run the Project

1. Clone the repository  
   ```bash
   git clone https://github.com/JSM2810/Resume-Analyzer.git
## Domain

1. Primary Domain: HR Tech / Recruitment

2. Application Type: Resume screening and job–candidate matching

Note: The NLP pipeline is reusable for other document similarity tasks.

## Limitations

1. Output depends on the quality of the job description

2. Creative resume formats may reduce parsing accuracy

3. Skill extraction accuracy can be improved with fine-tuning
