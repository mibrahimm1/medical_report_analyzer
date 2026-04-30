import os
from ultralytics import YOLO

class VisionModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisionModel, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        # Fallback to yolov8n.pt if best.pt is not found to prevent crashes during dev
        weights_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "weights", "best.pt")
        if os.path.exists(weights_path):
            self.model = YOLO(weights_path)
            self.is_custom = True
        else:
            self.model = YOLO("yolov8n.pt") # fallback for development
            self.is_custom = False

    def run_inference(self, img_path: str, conf_threshold: float = 0.25):
        """
        Runs YOLO inference on the given image path.
        Returns a list of dicts with detected anomalies.
        """
        results = self.model(img_path, conf=conf_threshold, verbose=False)
        
        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()
        
        detections = []
        detected_findings = []
        
        for i, box in enumerate(boxes):
            class_id = int(classes[i])
            anomaly_name = self.model.names[class_id]
            
            # Enforce "No Finding" filter logic
            if anomaly_name != "No finding":
                x1, y1, x2, y2 = box
                detected_findings.append(anomaly_name)
                detections.append({
                    "name": anomaly_name,
                    "confidence": float(confidences[i]),
                    "box": [float(x1), float(y1), float(x2), float(y2)]
                })
                
        return detections, list(set(detected_findings))

# Singleton instance
vision_engine = VisionModel()
