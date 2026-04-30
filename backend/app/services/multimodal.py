import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.config import settings

def generate_multimodal_summary(findings: str, impression: str, vision_detections: list) -> str:
    """
    Uses LangChain and Gemini 2.5 Flash to generate a patient-friendly summary.
    """
    if settings.google_api_key:
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
        
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.0)
    
    prompt_template = """
You are an expert medical communicator. Your task is to translate a dense radiologist report into a plain-language summary for a patient.

Here is the clinical report:
Findings: {clinical_findings}
Impression: {clinical_impression}

Here are the anomalies detected by our Computer Vision model on the patient's X-ray:
Detected Visual Anomalies: {vision_detections}

Instructions:
1. Write a patient-friendly summary of the Impression at a 6th-grade reading level. Use a warm, reassuring tone.
2. If the Vision model detected an anomaly that matches the text report, explicitly mention that our AI also saw it on the scan.
3. If the report says everything is normal, reassure the patient clearly. Begin with an encouraging opening like "Your X-ray results are ready! The good news is..."
4. Provide a clear "Overall" conclusion sentence summarizing their health.
5. Do not provide medical advice or diagnoses. Add a disclaimer at the end exactly like this: "Please remember, this summary is to help you understand your report. It's very important to talk to your doctor about these results and any questions you have. They can give you the best medical advice."

Patient Summary:
"""

    prompt = PromptTemplate(
        input_variables=["clinical_findings", "clinical_impression", "vision_detections"],
        template=prompt_template,
    )
    
    chain = prompt | llm
    
    detections_str = ", ".join(vision_detections) if vision_detections else "None detected"
    
    response = chain.invoke({
        "clinical_findings": findings,
        "clinical_impression": impression,
        "vision_detections": detections_str
    })
    content = response.content
    if isinstance(content, list):
        # Extract text parts if the content is returned as a list of dictionaries
        text_parts = [block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"]
        return "".join(text_parts)
    return str(content)
