from resume_parser import extract_resume_text, normalize_text
from jd_handler import validate_jd

if __name__ == "__main__":
    resume_text = normalize_text(extract_resume_text("Himanshu_Agarwal_AI.pdf"))
    print(f"Resume text length: {len(resume_text)}")

    jd = validate_jd("We are looking for a Software Engineer with React experience.")
    print(f"JD validated, length: {len(jd)}")