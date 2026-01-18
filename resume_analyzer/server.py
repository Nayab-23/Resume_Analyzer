import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory, abort

from .parser import extract_text
from .analyzer import analyze

app = Flask(__name__, static_folder=None)


@app.route("/", methods=["GET"])
def index():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
    try:
        return send_from_directory(root, "index.html")
    except Exception:
        abort(404)


@app.route("/analyze", methods=["POST"])
def analyze_route():
    if "resume" not in request.files:
        return jsonify({"error": "no file provided, use form field 'resume'"}), 400
    f = request.files["resume"]
    if f.filename == "":
        return jsonify({"error": "empty filename"}), 400

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f.filename)[1])
    try:
        f.save(tmp.name)
        text = extract_text(tmp.name)
        skills_file = os.path.join(os.path.dirname(__file__), "skills.txt")
        report = analyze(text, skills_file)
        return jsonify(report)
    finally:
        try:
            tmp.close()
            os.unlink(tmp.name)
        except Exception:
            pass


def run(host="127.0.0.1", port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run()
