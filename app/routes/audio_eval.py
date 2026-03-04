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

        prompt= f"""
        You are observing a job interview that is currently in progress.

        Generate concise recruiter-facing insights from the conversation so far.

        Use the exact structure below.

        IMPORTANT RULES
        • Keep responses SHORT.
        • Maximum 1 short sentence per bullet.
        • Do NOT write paragraphs.
        • Only score if clear evidence exists in the transcript.
        • If no evidence exists write "No data yet".
        • Avoid repeating earlier insights.

        FORMAT:

        **REAL-TIME CONVERSATIONAL INSIGHTS**

        **Strength signals seen**
        • ...

        **Weakness signals or concerns**
        • ...

        **DYNAMIC INTERVIEW GUIDANCE**
        Suggest 2-3 follow-up questions the interviewer should ask next.

        • ...
        • ...

        **INSTANT EVALUATION METRICS**

        Technical Skills → score /10 OR "No data yet"  
        Problem Solving → score /10 OR "No data yet"  
        Communication → score /10 OR "No data yet"

        Transcript so far:
        {c}
        """
        outputs.append(ask_gemini(prompt))

    return {"transcript":transcript,"dynamic":outputs}