import re
import os
from typing import List, Dict

EMAIL_RE = re.compile(r"[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+")
PHONE_RE = re.compile(r"(\+?\d[\d\-(). ]{7,}\d)")

DEGREE_KEYWORDS = [
    "bachelor",
    "master",
    "b.sc",
    "m.sc",
    "bs",
    "ms",
    "phd",
    "associate",
]


def extract_emails(text: str) -> List[str]:
    return sorted(set(m.group(0) for m in EMAIL_RE.finditer(text)))


def extract_phones(text: str) -> List[str]:
    matches = [m.group(0).strip() for m in PHONE_RE.finditer(text)]
    # basic cleanup
    cleaned = []
    for ph in matches:
        ph2 = re.sub(r"[^0-9+]+", "", ph)
        if 7 <= len(re.sub(r"\D", "", ph2)) <= 15:
            cleaned.append(ph2)
    return sorted(set(cleaned))


def extract_skills(text: str, skills_file: str) -> List[str]:
    if not os.path.exists(skills_file):
        return []
    with open(skills_file, "r", encoding="utf-8") as f:
        skills = [s.strip() for s in f if s.strip()]
    text_l = text.lower()
    found = []
    for s in skills:
        s_l = s.lower()
        if re.search(r"\b" + re.escape(s_l) + r"\b", text_l):
            found.append(s)
    return sorted(set(found))


def extract_education(text: str) -> List[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    found = []
    for line in lines:
        low = line.lower()
        for kw in DEGREE_KEYWORDS:
            if kw in low:
                found.append(line)
                break
    return found


def guess_name(text: str) -> str:
    # simple heuristic: first non-empty line with 2-4 words and capitalized words
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        words = line.split()
        if 1 < len(words) <= 4 and all(w[0].isupper() or w[0].isalpha() for w in words):
            return line
    return ""


def analyze(text: str, skills_file: str) -> Dict:
    return {
        "name": guess_name(text),
        "emails": extract_emails(text),
        "phones": extract_phones(text),
        "skills": extract_skills(text, skills_file),
        "education": extract_education(text),
        "summary_lines": [l for l in (text.splitlines()[:6]) if l.strip()],
    }
