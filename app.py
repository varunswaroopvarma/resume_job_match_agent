from flask import Flask, request, render_template, redirect, url_for, flash
from pathlib import Path
from resume_parser import extract_resume_text
from preprocess_text import preprocess_text
from job_matcher import match_score
from scoring_highlight import analyze_skills, format_score

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        file = request.files.get("resume_file")

        if not file or file.filename == '':
            flash('No resume file uploaded')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Only PDF or TXT files are allowed')
            return redirect(request.url)

        if not job_description:
            flash('Job description is required')
            return redirect(request.url)

        filename = file.filename
        filepath = UPLOAD_FOLDER / filename
        file.save(filepath)

        try:
            resume_raw_text = extract_resume_text(str(filepath))
        except ValueError as e:
            flash(str(e))
            try:
                filepath.unlink()
            except Exception:
                pass
            return redirect(request.url)

        # Delete the temp file after extracting
        try:
            filepath.unlink()
        except Exception as e:
            flash(f"Could not delete temporary file: {e}")

        resume_processed = preprocess_text(resume_raw_text)
        job_processed = preprocess_text(job_description)

        score = match_score(resume_processed, job_processed)
        matched_keywords, missing_keywords = analyze_skills(resume_raw_text, job_description)

        return render_template(
            "result.html",
            score=format_score(score),
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            job_description=job_description,
            resume_text=resume_raw_text
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
