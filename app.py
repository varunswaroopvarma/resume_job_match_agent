import streamlit as st
import pathlib
from resume_parser import extract_resume_text
from preprocess_text import preprocess_text
from job_matcher import match_score
from scoring_highlight import analyze_skills, format_score

def main():
    st.title("Resume and Job Description Match AI")

    resume_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
    job_description = st.text_area("Paste Job Description text here")

    if resume_file and job_description:
        filename = resume_file.name
        dot_index = filename.rfind('.')
        if dot_index == -1:
            st.error("Uploaded file must have an extension like .pdf or .txt")
            return
        ext = filename[dot_index:]  # e.g., ".pdf" or ".txt"

        temp_filename = "temp_resume" + ext

        with open(temp_filename, "wb") as f:
            f.write(resume_file.getbuffer())

        try:
            resume_raw_text = extract_resume_text(temp_filename)
        except ValueError as e:
            st.error(str(e))
            # Attempt to delete temp file before exit
            try:
                pathlib.Path(temp_filename).unlink()
            except Exception:
                pass
            return

        # Delete the temporary file after extracting text
        try:
            pathlib.Path(temp_filename).unlink()
        except Exception as e:
            st.warning(f"Could not delete temporary file: {e}")

        resume_processed = preprocess_text(resume_raw_text)
        job_processed = preprocess_text(job_description)

        score = match_score(resume_processed, job_processed)
        matched_keywords, missing_keywords = analyze_skills(resume_raw_text, job_description)

        st.subheader("Match Score")
        st.write(format_score(score))

        st.subheader("Matching Skills")
        if matched_keywords:
            st.write(", ".join(matched_keywords))
        else:
            st.write("No matching skills found.")

        st.subheader("Missing (Required) Skills")
        if missing_keywords:
            st.write(", ".join(missing_keywords))
        else:
            st.success("Your resume covers all required skills!")

if __name__ == "__main__":
    main()
