from pydantic import BaseModel
from typing import List, Dict, Any

class AnalyzeResponse(BaseModel):
    annotated_image: str  # Base64 encoded image
    summary: str          # Patient-friendly explanation
    detections: List[Dict[str, Any]] # Raw detections if needed
    raw_report: Dict[str, str] # Findings and Impression
