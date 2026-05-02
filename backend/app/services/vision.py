import os
import gc
from ultralytics import YOLO

class VisionModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisionModel, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.is_custom = False
        return cls._instance

    def _load_model(self):
        """Loads the model only when needed to save RAM."""
        if self.model is not None:
            return
            
        weights_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "weights", "best.pt")
        if os.path.exists(weights_path):
            self.model = YOLO(weights_path)
            self.is_custom = True
        else:
            self.model = YOLO("yolov8n.pt")
            self.is_custom = False

    def run_inference(self, img_path: str, conf_threshold: float = 0.25):
        """
        Runs YOLO inference on the given image path.
        Returns a list of dicts with detected anomalies.
        """
        self._load_model()
        
        results = self.model(img_path, conf=conf_threshold, verbose=False)
        
        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()
        
        detections = []
        detected_findings = []
        
        for i, box in enumerate(boxes):
            class_id = int(classes[i])
            anomaly_name = self.model.names[class_id]
            
            if anomaly_name != "No finding":
                x1, y1, x2, y2 = box
                detected_findings.append(anomaly_name)
                detections.append({
                    "name": anomaly_name,
                    "confidence": float(confidences[i]),
                    "box": [float(x1), float(y1), float(x2), float(y2)]
                })
        
        # Explicitly clear results and collect garbage to free RAM
        del results
        gc.collect()
                
        return detections, list(set(detected_findings))

# Singleton instance - will not load model until first use
vision_engine = VisionModel()
