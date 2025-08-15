import spacy

# Ensure spaCy model is loaded; download if missing
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """
    Extracts skill-like keywords (nouns/proper nouns/adjectives) from text,
    returns a set of normalized keywords.
    """
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            word = token.lemma_.lower()
            if len(word) > 2 and word not in nlp.Defaults.stop_words:
                keywords.add(word)
    return keywords

def highlight_matches(resume_text, job_desc_text):
    """
    Finds common skill keywords between resume and job description.
    """
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc_text)
    matched_keywords = resume_keywords.intersection(job_keywords)
    return sorted(matched_keywords)

def analyze_skills(resume_text, job_desc_text):
    """
    Returns two sorted lists:
    - matched skills (present in both resume and job description)
    - missing skills (in job description but not in resume)
    """
    resume_skills = extract_keywords(resume_text)
    job_skills = extract_keywords(job_desc_text)
    matched = sorted(resume_skills.intersection(job_skills))
    missing = sorted(job_skills.difference(resume_skills))
    return matched, missing

def format_score(score):
    """
    Converts similarity score (0-1) to a percentage string.
    """
    return f"{score * 100:.2f}%"
