import fitz  # PyMuPDF
import re

def parse_clinical_report(file_bytes: bytes, filename: str) -> dict:
    """
    Parses a PDF or TXT clinical report to extract 'Findings' and 'Impression'.
    Provides fallback if sections are missing.
    """
    text = ""
    
    if filename.lower().endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    else:
        # Assume text file
        text = file_bytes.decode("utf-8")
        
    return extract_sections(text)

def extract_sections(text: str) -> dict:
    """
    Extracts text sections based on common medical report headers.
    """
    # Simple regex based extraction
    findings_match = re.search(r'(?i)findings?[:\n]+(.*?)(?=\n[A-Z][a-z]+:|\Z)', text, re.DOTALL)
    impression_match = re.search(r'(?i)impression[:\n]+(.*?)(?=\n[A-Z][a-z]+:|\Z)', text, re.DOTALL)
    
    findings = findings_match.group(1).strip() if findings_match else "Not provided"
    impression = impression_match.group(1).strip() if impression_match else "Not provided"
    
    # Fallback if both are missing
    if findings == "Not provided" and impression == "Not provided":
        # Just use the whole text as impression if it's short, or split it up.
        impression = text.strip() if text.strip() else "Not provided"
        
    return {
        "findings": findings,
        "impression": impression
    }
