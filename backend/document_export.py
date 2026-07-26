import os
from docx import Document
from docx.shared import Pt

OUTPUT_DIR = "outputs"


def create_cover_letter_docx(cover_letter_text: str, filename: str = "cover_letter.docx") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = Document()
    for paragraph_text in cover_letter_text.split("\n\n"):
        if paragraph_text.strip():
            p = doc.add_paragraph(paragraph_text.strip())
            p.paragraph_format.space_after = Pt(12)

    output_path = os.path.join(OUTPUT_DIR, filename)
    doc.save(output_path)
    return output_path

if __name__ == "__main__":
    sample_letter = "Dear Hiring Manager,\n\nThis is a test paragraph.\n\nSincerely,\nHimanshu"
    path = create_cover_letter_docx(sample_letter)
    print(f"Saved to: {path}")