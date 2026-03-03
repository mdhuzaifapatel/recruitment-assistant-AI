from fastapi import APIRouter, UploadFile, File
import uuid

from app.services.audio_service import transcribe_chunk
from app.services.gemini_service import ask_gemini

router = APIRouter()
UPLOAD="uploads"


@router.post("/evaluate-audio")
async def evaluate_audio(audio:UploadFile=File(...)):

    path=f"{UPLOAD}/{uuid.uuid4()}_{audio.filename}"

    with open(path,"wb") as f:
        f.write(await audio.read())

    transcript=transcribe_chunk(path)
    print("TRANSCRIPT:", transcript)
    # progressive chunks simulate real-time interview
    chunks=[
        transcript[:len(transcript)//3],
        transcript[:2*len(transcript)//3],
        transcript
    ]

    outputs=[]

    for c in chunks:

        prompt=f"""
You are observing an interview that is still ongoing.

From the conversation so far, generate recruiter-usable real-time insights.

REAL-TIME CONVERSATIONAL INSIGHTS
• Strength signals seen
• Weakness signals or concerns

DYNAMIC INTERVIEW GUIDANCE
Suggest 2-3 follow-up questions interviewer should ask next.

INSTANT EVALUATION METRICS

Technical Skills → score /10 OR "No data yet"
Problem Solving → score /10 OR "No data yet"
Communication → score /10 OR "No data yet"

IMPORTANT:
Only score if evidence exists.

Transcript so far:
{c}
"""

        outputs.append(ask_gemini(prompt))

    return {"transcript":transcript,"dynamic":outputs}