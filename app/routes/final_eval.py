from fastapi import APIRouter
from app.services.gemini_service import ask_gemini

router = APIRouter()


@router.post("/final-insights")
async def final_insights(transcript:str):

    prompt=f"""
You are a senior hiring decision advisor.

Evaluate the FULL interview transcript and generate:

Candidate Key Strengths
Candidate Key Weaknesses / Gaps
Final Hiring Recommendation (Hire / Consider / Reject)
Fit Score (0-100)

Be realistic and recruiter-style.

Transcript:
{transcript}
"""

    return {"final":ask_gemini(prompt)}