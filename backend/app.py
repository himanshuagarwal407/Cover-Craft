import gradio as gr
import logging

from resume_parser import extract_resume_text, normalize_text
from jd_handler import validate_jd
from models import StylePreference
from generator import generate_cover_letter
from document_export import create_cover_letter_docx

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def run_generate(resume_file, jd_text, tone, length, confidence, progress=gr.Progress()):
    if resume_file is None:
        return "Please upload a resume file.", "", None

    try:
        progress(0.1, desc="Reading resume file...")
        raw_text = extract_resume_text(resume_file)

        if not raw_text or not raw_text.strip():
            return "Could not extract any text from the resume. It may be a scanned/image-based file.", "", None

        progress(0.3, desc="Cleaning extracted text...")
        resume_text = normalize_text(raw_text)

        progress(0.5, desc="Validating job description...")
        cleaned_jd = validate_jd(jd_text)

        style = StylePreference(tone=tone, length=length, confidence=confidence)

        progress(0.7, desc="Generating your cover letter (calling Gemini)...")
        logger.info("Calling Gemini API for generation")
        result = generate_cover_letter(resume_text, cleaned_jd, style)

        progress(0.9, desc="Preparing download...")
        docx_path = create_cover_letter_docx(result["cover_letter"])

        progress(1.0, desc="Done!")

    except ValueError as e:
        return f"Input error: {e}", "", None
    except RuntimeError as e:
        return f"Generation error: {e}", "", None

    bullets_output = "\n".join(f"- {b}" for b in result["rewritten_bullets"])
    return result["cover_letter"], bullets_output, docx_path


demo = gr.Interface(
    fn=run_generate,
    inputs=[
        gr.File(label="Upload Resume (PDF or DOCX)"),
        gr.Textbox(label="Paste Job Description", lines=10),
        gr.Dropdown(label="Tone", choices=["formal", "conversational"], value="formal"),
        gr.Dropdown(label="Length", choices=["brief", "detailed"], value="brief"),
        gr.Dropdown(label="Confidence", choices=["humble", "assertive"], value="assertive"),
    ],
    outputs=[
        gr.Textbox(label="Cover Letter", lines=15),
        gr.Textbox(label="Rewritten Resume Bullets", lines=8),
        gr.File(label="Download Cover Letter (.docx)"),
    ],
    title="CoverCraft",
    description="Upload your resume and a job description to generate a tailored cover letter and rewritten resume bullets."
)

if __name__ == "__main__":
    demo.launch()