import os, json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

from models import ResumeFitContent, StylePreference

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def build_generation_prompt(
        resume_text: str,
        jd_text: str,
        style: StylePreference,
        resume_fit_content: ResumeFitContent = None,
) -> str:
    tone_instruction = {
        "formal": "Use a professional, polished tone appropriate for traditional corporate environments.",
        "conversational": "Use a warm, natural tone that still feels professional - like a confident conversation, not a stiff template.",
    }[style.tone]

    length_instruction = {
        "brief": "Keep the cover letter concise - 3 short paragraphs at most.",
        "detailed": "Write a full cover letter - 4-5 paragraphs covering background, specific fit and closing.",
    }[style.length]

    confidence_instruction = {
        "humble": "Frame achievements with modest, grounded language - avoid overselling.",
        "assertive": "Frame achievements with confident, direct language - state impact clearly without hedging.",
    }[style.confidence]

    context_Section = ""
    if resume_fit_content:
        if resume_fit_content.strong_matches:
            context_section += f"\nKnown strong matches to emphasize: {', '.join(resume_fit_content.strong_matches)}."
        if resume_fit_content.missing_keywords:
            context_section += f"\nKnown gaps to address tactfully, (e.g., via transferable experience, without pretending to have them): {', '.join(resume_fit_content.missing_keywords)}."

    prompt = f"""You are an expert career writer helping a candidate craft application material for a specific job.

STYLE REQUIREMENTS:
- {tone_instruction}
- {length_instruction}
- {confidence_instruction}
- Avoid generic AI-sounding phrases like "I am excited to apply," "team player," "fast learner," or "passionate about. Write like a real, specific person not a template.
- Never fabricate skills, experiences, or achievements not present in the resume.
{context_Section}

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Generate two things:
1. A complete cover letter tailored to this specific job, following the style requirements above.
2. 3-5 rewritten resume bullet points that reframe the candidate's actual experience to better match the job description's language and priorities - still 100% based on real resume content, just reworded/reordered for relevance.

Respond only with a valid JSON object (no markdown, no backticks, no extra text) with exactly this structure:
{{
    "cover_letter": "<full cover letter text, with paragraph breaks as \\n\\n>",
    "rewritten_bullets": [<list of 3-5 rewritten bullet point strings>]
}}
"""
    return prompt

def generate_cover_letter(
        resume_text: str,
        jd_text: str,
        style: StylePreference,
        resume_fit_content: ResumeFitContent = None,
) -> dict:
    prompt = build_generation_prompt(resume_text, jd_text, style, resume_fit_content)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
            )
        )
    except genai_errors.APIError as e:
        raise RuntimeError(f"Gemini API call failed: {e}")

    if not response.text:
        raise RuntimeError("Gemini API returned an empty response.")

    try:
        result = json.loads(response.text.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini does not return valid JSON. Raw Response text: {response.text.strip()}. Error: {e}")

    return result

def load_jd_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    from resume_parser import extract_resume_text, normalize_text
    from jd_handler import validate_jd

    resume_text = normalize_text(extract_resume_text("Himanshu_Agarwal_AI.pdf"))

    jd_raw = load_jd_from_file("jd1.txt")
    jd_text = validate_jd(jd_raw)

    style = StylePreference(tone="conversational", length="brief", confidence="assertive")
    result = generate_cover_letter(resume_text, jd_text, style)

    print("COVER LETTER:\n")
    print(result["cover_letter"])
    print("\n\nREWRITTEN BULLETS:\n")
    for bullet in result["rewritten_bullets"]:
        print(f"- {bullet}")