import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Cleans, tokenizes, removes stopwords, and lemmatizes the input text.
    Returns a preprocessed text string.
    """
    doc = nlp(text)
    tokens = []
    for token in doc:
        # Skip stopwords, punctuation, spaces, numbers
        if (
            token.is_stop
            or token.is_punct
            or token.is_space
            or token.like_num
        ):
            continue
        # Use lemmatized (root) word, lowercased
        lemma = token.lemma_.lower()
        if lemma:  # Only add non-empty lemmas
            tokens.append(lemma)
    return " ".join(tokens)

# Example usage:
if __name__ == "__main__":
    sample_text = "Experienced Python developer with 5 years in AI and machine learning."
    cleaned_text = preprocess_text(sample_text)
    print("Preprocessed Text:\n", cleaned_text)
