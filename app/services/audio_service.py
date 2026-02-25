import speech_recognition as sr
from pydub import AudioSegment
import uuid, os

UPLOAD="uploads"

def audio_to_text(path):

    wav=f"{UPLOAD}/{uuid.uuid4()}.wav"

    AudioSegment.from_file(path).export(wav,format="wav")

    r=sr.Recognizer()

    with sr.AudioFile(wav) as source:
        audio=r.record(source)

    try:
        txt=r.recognize_google(audio)
    except:
        txt=""

    os.remove(wav)
    return txt