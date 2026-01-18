import argparse
import json
import sys
from . import parser
from . import analyzer
import os


def login():
    username = input("Username: ")
    password = input("Password: ")
    # Here you would typically validate the username and password
    print(f"Logged in as {username}")


def main(argv=None):
    login()
    p = argparse.ArgumentParser(description="Simple Resume Analyzer")
    p.add_argument("path", help="Path to resume file (pdf/docx/txt)")
    p.add_argument("--skills", help="Path to skills file", default=os.path.join(os.path.dirname(__file__), "skills.txt"))
    p.add_argument("--output", help="Write JSON output to file")
    args = p.parse_args(argv)

    try:
        text = parser.extract_text(args.path)
    except Exception as e:
        print(f"Failed to extract text: {e}", file=sys.stderr)
        sys.exit(2)

    report = analyzer.analyze(text, args.skills)

    out = json.dumps(report, indent=2, ensure_ascii=False)
    print(out)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)


if __name__ == "__main__":
    main()