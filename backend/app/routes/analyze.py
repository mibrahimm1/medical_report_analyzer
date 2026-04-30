import os
import shutil
import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.response import AnalyzeResponse
from app.services.vision import vision_engine
from app.services.parsing import parse_clinical_report
from app.services.multimodal import generate_multimodal_summary
from app.services.annotation import annotate_image

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_report(
    image: UploadFile = File(...),
    report: UploadFile = File(...)
):
    if not image or not report:
        raise HTTPException(status_code=400, detail="Image and report files are required.")
    
    # Save uploaded image to a temporary file for YOLO and OpenCV
    temp_img_fd, temp_img_path = tempfile.mkstemp(suffix=".jpg")
    try:
        with os.fdopen(temp_img_fd, 'wb') as f:
            shutil.copyfileobj(image.file, f)
            
        # 1. Vision Engine - run YOLOv11 inference
        detections, detected_findings = vision_engine.run_inference(temp_img_path)
        
        # 2. Parsing Layer - extract findings and impression from report
        report_bytes = await report.read()
        parsed_data = parse_clinical_report(report_bytes, report.filename)
        
        # 3. Multimodal Orchestration
        summary = generate_multimodal_summary(
            findings=parsed_data["findings"],
            impression=parsed_data["impression"],
            vision_detections=detected_findings
        )
        
        # 4. Image Annotation
        annotated_image_base64 = annotate_image(temp_img_path, detections)
        
        return AnalyzeResponse(
            annotated_image=annotated_image_base64,
            summary=summary,
            detections=detections,
            raw_report=parsed_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
