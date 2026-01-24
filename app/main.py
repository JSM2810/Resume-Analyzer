from fastapi import FastAPI, UploadFile, File, Form
from app.parser import parse_file
from app.nlp_pipeline import clean_text, extract_skills, load_skills
from app.matcher import rank_resumes_by_job

app = FastAPI()
skills_list = load_skills()

@app.post("/match")
async def match(job_description: str = Form(...), files: list[UploadFile] = File(...)):
    resumes_texts = []
    filenames = []
    for f in files:
        content = await f.read()
        tmp = f"/tmp/{f.filename}"
        with open(tmp, "wb") as fh:
            fh.write(content)
        txt = parse_file(tmp, f.filename)
        resumes_texts.append(clean_text(txt))
        filenames.append(f.filename)
    rankings = rank_resumes_by_job(resumes_texts, job_description, top_k=len(resumes_texts))
    results = []
    for idx, score in rankings:
        skills = extract_skills(resumes_texts[idx], skills_list)
        results.append({"filename": filenames[idx], "score": score, "skills": skills})
    return {"job": job_description, "results": results}
