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
You are an AI hiring screening assistant helping recruiters quickly assess candidate fit.

Compare the candidate resume against the job description and produce a **concise pre-evaluation**.

STRICT RULES
• Use bullet points only.
• Maximum **2 bullets per section**.
• **1 short sentence per bullet**.
• No paragraphs or explanations.
• Keep language professional and recruiter-focused.

Return the response in **this exact structure**:

**MATCH SCORE (0-100)**
Provide ONE numeric score representing overall role fit.

**PROFILE SUMMARY**
• Very brief candidate background snapshot.
• Key domain or years of experience if available.

**KEY MATCHES**
• Top relevant skill or experience aligned with the job.
• Another strong alignment with the role.

**GAPS / RISKS**
• Missing or weak skill relative to the JD.
• Any unclear experience or hiring concern.

**INTERVIEW FOCUS**

Technical verification:
• One technical capability recruiter should validate.

Behavioural verification:
• One behavioural or collaboration aspect to probe.

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    return {"insights": ask_gemini(prompt)}