# Resume Analyzer

A small CLI tool to extract contact info, skills, and education from resumes (PDF, DOCX, TXT).

Quickstart

1. Create a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the analyzer:

```bash
python -m resume_analyzer.main path/to/resume.pdf
```

Output will be printed to stdout and can be saved with `--output out.json`.

Files of interest:
- [resume_analyzer/main.py](resume_analyzer/main.py)
- [resume_analyzer/parser.py](resume_analyzer/parser.py)
- [resume_analyzer/analyzer.py](resume_analyzer/analyzer.py)
