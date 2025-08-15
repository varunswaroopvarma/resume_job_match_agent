from sentence_transformers import SentenceTransformer, util

# Load pre-trained model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Generate embedding vector for the input text.
    """
    return model.encode(text, convert_to_tensor=True)

def match_score(resume_text, job_description_text):
    """
    Compute cosine similarity score between resume and job description embeddings.
    Returns a float score between 0 and 1 (higher means better match).
    """
    emb_resume = get_embedding(resume_text)
    emb_job = get_embedding(job_description_text)
    similarity = util.pytorch_cos_sim(emb_resume, emb_job)
    return float(similarity)

# Example usage
if __name__ == "__main__":
    resume_sample = "experienced data scientist proficient in machine learning, python, and AI"
    job_desc_sample = "looking for a machine learning engineer skilled in python and data analysis"
    score = match_score(resume_sample, job_desc_sample)
    print(f"Match Score: {score:.4f}")
