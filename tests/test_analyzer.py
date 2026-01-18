import pytest
from resume_analyzer import analyzer


SAMPLE = """
John Doe
Email: john.doe@example.com
Phone: +1 (555) 123-4567
Experienced Python developer with experience in Docker, AWS, and PostgreSQL.
Education: Bachelor of Science in Computer Science
"""


def test_extract_email():
    emails = analyzer.extract_emails(SAMPLE)
    assert "john.doe@example.com" in emails


def test_extract_phone():
    phones = analyzer.extract_phones(SAMPLE)
    assert any(p.endswith("1234567") or "555" in p for p in phones)


def test_skills(tmp_path):
    skills_file = tmp_path / "skills.txt"
    skills_file.write_text("Python\nDocker\nAWS\n")
    skills = analyzer.extract_skills(SAMPLE, str(skills_file))
    assert "Python" in skills
    assert "Docker" in skills
