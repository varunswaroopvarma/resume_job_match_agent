import spacy
from spacy.cli import download

# Download the model if not present
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Cleans, tokenizes, removes stopwords, and lemmatizes the input text.
    Returns a preprocessed text string.
    """
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_stop or token.is_punct or token.is_space or token.like_num:
            continue
        lemma = token.lemma_.lower()
        if lemma:
            tokens.append(lemma)
    return " ".join(tokens)

# Example usage
if __name__ == "__main__":
    sample_text = "Experienced Python developer with 5 years in AI and machine learning."
    cleaned_text = preprocess_text(sample_text)
    print("Preprocessed Text:\n", cleaned_text)
