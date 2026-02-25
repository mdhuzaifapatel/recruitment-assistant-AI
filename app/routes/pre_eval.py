from fastapi import APIRouter, UploadFile, File
import uuid, os

from app.services.gemini_service import ask_gemini
from app.services.text_service import extract_text

router = APIRouter()

UPLOAD="uploads"

@router.post("/pre-eval")
async def pre_eval(resume: UploadFile, jd:UploadFile):
    rpath = f"{UPLOAD}/{uuid.uuid4()}_{resume.filename}"
    jpath = f"{UPLOAD}/{uuid.uuid4()}_{jd.filename}"

    with open(rpath, "wb") as f:
        f.write(await resume.read())
    
    with open(jpath, "wb") as f:
        f.write(await jd.read())

    resume_text = extract_text(rpath)
    # print(resume_text)
    jd_text = extract_text(jpath)
    # print(jd_text)

    prompt = f"""
        You are an AI hiring screening assistant.

        Compare the candidate resume with the job description and produce a SHORT recruiter pre-evaluation.

        IMPORTANT RULES:
        - Keep output concise
        - Use bullet points only
        - Maximum 2-3 bullets per section
        - Avoid long explanations

        Return EXACTLY these sections:

        MATCH SCORE (0-100):
        Give one numeric score representing overall role fit.

        PROFILE SUMMARY:
        Very short candidate background snapshot (1-2 lines).

        KEY MATCHES:
        Top skills/experience aligned with JD.

        GAPS / RISKS:
        Missing skills, unclear experience, or hiring concerns.

        INTERVIEW FOCUS:
        1 technical thing recruiter should verify
        1 behavioural thing recruiter should verify

        Resume:
        {resume_text}

        Job Description:
        {jd_text}
        """
    return {"insights": ask_gemini(prompt)}