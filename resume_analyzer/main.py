import argparse
import json
import sys
from . import parser
from . import analyzer
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would normally check the username and password
        if username == 'admin' and password == 'password':  # Replace with real authentication
            return redirect(url_for('analyze'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        path = request.form['path']
        skills = request.form.get('skills', os.path.join(os.path.dirname(__file__), "skills.txt"))
        output = request.form.get('output')

        try:
            text = parser.extract_text(path)
        except Exception as e:
            print(f"Failed to extract text: {e}", file=sys.stderr)
            return "Error extracting text", 500

        report = analyzer.analyze(text, skills)

        out = json.dumps(report, indent=2, ensure_ascii=False)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(out)
        return out

    return render_template('analyze.html')

if __name__ == "__main__":
    app.run(debug=True)