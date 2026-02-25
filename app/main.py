from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routes import pre_eval, audio_eval, final_eval

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(pre_eval.router)
app.include_router(audio_eval.router)
app.include_router(final_eval.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})