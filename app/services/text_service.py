import pdfplumber
import docx


def read_txt(path):
    """
    Robust text reader supporting UTF-8, UTF-16, ANSI, Windows exports.
    """

    encodings = ["utf-8", "utf-16", "latin-1"]

    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except:
            continue

    # last fallback (binary safe)
    with open(path, "rb") as f:
        return f.read().decode(errors="ignore")


def read_pdf(path):
    text=""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text() or ""
    return text


def read_docx(path):
    d=docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs)


def extract_text(path):

    lower = path.lower()

    if lower.endswith(".pdf"):
        return read_pdf(path)

    elif lower.endswith(".docx"):
        return read_docx(path)

    elif lower.endswith(".txt"):
        return read_txt(path)

    # fallback attempt
    return read_txt(path)