from pydantic import BaseModel
from typing import Literal, Optional

class StylePreference(BaseModel):
    tone: Literal['formal', 'conversational'] = "formal"
    length: Literal['brief', 'detailed'] = "brief"
    confidence: Literal['humble', 'assertive'] = "humble"

class ResumeFitContent(BaseModel):
    """Optional context passed in from ResumeFitCheck's output, used to
    help CoverCraft emphasize genuine strengths and address real gaps."""
    strong_matches: Optional[List[str]] = None
    missing_keywords: Optional[List[str]] = None

class CoverCraftResponse(BaseModel):
    cover_letter: str
    rewritten_bullets: List[str]