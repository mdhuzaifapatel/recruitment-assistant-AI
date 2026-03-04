from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(prompt: str):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        # config={
        #     "temperature":0.3,
        #     "max_output_tokens":250
        # }
    )
    
    return response.text