from fastapi import APIRouter
from app.services.gemini_service import ask_gemini

router = APIRouter()


@router.post("/final-insights")
async def final_insights(transcript:str):

    prompt = f"""
You are a senior hiring decision advisor reviewing a completed interview.

Evaluate the **full interview transcript** and produce a concise hiring summary for the recruiter.

STRICT RULES
• Use bullet points only.
• Maximum **2 bullets per section**.
• **1 short sentence per bullet**.
• No long explanations or paragraphs.
• Be objective and realistic.

Return the result in **this exact structure**:

**CANDIDATE KEY STRENGTHS**
• Most convincing capability demonstrated.
• Another strong signal from the interview.

**CANDIDATE KEY WEAKNESSES / GAPS**
• Missing skill, weak explanation, or unclear experience.
• Another concern or potential hiring risk.

**FINAL HIRING RECOMMENDATION**
Hire / Consider / Reject  
Provide **1 short reason**.

**FIT SCORE (0-100)**
Provide one numeric score representing overall role fit.

Transcript:
{transcript}
"""

    return {"final":ask_gemini(prompt)}