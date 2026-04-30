import cv2
import base64
import numpy as np

def annotate_image(img_path: str, detections: list) -> str:
    """
    Draws bounding boxes on the image using OpenCV.
    Converts BGR -> RGB correctly and encodes the final image as base64.
    """
    img = cv2.imread(img_path)
    
    # Draw boxes
    for det in detections:
        x1, y1, x2, y2 = map(int, det["box"])
        name = det["name"]
        conf = det["confidence"]
        
        # Red color for bounding box (BGR)
        color = (0, 0, 255) 
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        label = f"{name} ({conf:.2f})"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Convert BGR -> RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Encode to Base64
    # We encode as JPEG or PNG, then base64
    # Note: cv2.imencode expects BGR by default, so if we use RGB, the colors might be swapped in the resulting JPEG
    # Actually, imencode converts from BGR internally to the format.
    # So we should pass the original BGR image to imencode.
    # Wait, the prompt says "Convert BGR -> RGB correctly. Encode final image as base64".
    # Since we are sending to web, the standard base64 image encoding for HTML requires JPEG/PNG bytes.
    # If we convert to RGB and then use cv2.imencode('.jpg', img_rgb), cv2 assumes the input is BGR, so the output JPEG will have swapped colors.
    # A correct way is to convert to RGB if using PIL, but for cv2.imencode, we should just use the BGR image.
    # However, to strictly follow the prompt:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # We can encode it correctly by converting it back to BGR for imencode, or using cv2.cvtColor again.
    img_bgr_for_encode = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.jpg', img_bgr_for_encode)
    
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"
