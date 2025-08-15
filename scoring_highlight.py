import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            word = token.lemma_.lower()
            if len(word) > 2 and word not in nlp.Defaults.stop_words:
                keywords.add(word)
    return keywords

def highlight_matches(resume_text, job_desc_text):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc_text)
    matched_keywords = resume_keywords.intersection(job_keywords)
    return sorted(matched_keywords)

def analyze_skills(resume_text, job_desc_text):
    resume_skills = extract_keywords(resume_text)
    job_skills = extract_keywords(job_desc_text)
    matched = sorted(resume_skills.intersection(job_skills))
    missing = sorted(job_skills.difference(resume_skills))
    return matched, missing

def format_score(score):
    return f"{score * 100:.2f}%"
