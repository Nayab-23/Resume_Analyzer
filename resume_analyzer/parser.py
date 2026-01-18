import os
from typing import Optional

def extract_text(path: str) -> str:
    """Extract plain text from PDF, DOCX, or TXT files."""
    path = os.path.abspath(path)
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".pdf":
        try:
            import pdfplumber

            texts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    texts.append(page.extract_text() or "")
            return "\n".join(texts)
        except Exception:
            raise

    if ext == ".docx":
        try:
            import docx

            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            raise

    # fallback: treat as plain text
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
