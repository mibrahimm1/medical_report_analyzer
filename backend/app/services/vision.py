import os
import cv2
import numpy as np
import onnxruntime as ort

class VisionModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisionModel, cls).__new__(cls)
            cls._instance.session = None
            cls._instance.names = {
                0: 'Aortic_enlargement', 1: 'Atelectasis', 2: 'Calcification', 
                3: 'Cardiomegaly', 4: 'Consolidation', 5: 'ILD', 6: 'Infiltration', 
                7: 'Lung_Opacity', 8: 'Nodule/Mass', 9: 'Other_lesion', 
                10: 'Pleural_effusion', 11: 'Pleural_thickening', 12: 'Pneumothorax', 
                13: 'Pulmonary_fibrosis', 14: 'No finding'
            }
        return cls._instance

    def _load_model(self):
        if self.session is not None:
            return
            
        weights_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "weights", "best.onnx")
        if not os.path.exists(weights_path):
            # If onnx doesn't exist, we'll have to wait for the user to upload it or use a fallback
            # But we just created it, so it should be there.
            raise FileNotFoundError(f"Model file not found at {weights_path}")
            
        # Use CPU only to save RAM
        self.session = ort.InferenceSession(weights_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape # e.g. [1, 3, 512, 512]

    def run_inference(self, img_path: str, conf_threshold: float = 0.25, iou_threshold: float = 0.45):
        self._load_model()
        
        # Load and preprocess image
        original_img = cv2.imread(img_path)
        h, w = original_img.shape[:2]
        
        # YOLOv8 expects RGB and specific size (512x512 based on export)
        input_w, input_h = self.input_shape[2], self.input_shape[3]
        img_resized = cv2.resize(original_img, (input_w, input_h))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize and reshape
        img_input = img_rgb.astype(np.float32) / 255.0
        img_input = img_input.transpose(2, 0, 1) # HWC to CHW
        img_input = np.expand_dims(img_input, axis=0) # Add batch dim
        
        # Run inference
        outputs = self.session.run(None, {self.input_name: img_input})
        output = outputs[0][0] # Shape (19, 5376)
        
        # Post-process: Transpose and extract boxes/scores
        output = output.T # Shape (5376, 19)
        
        boxes = []
        scores = []
        class_ids = []
        
        for row in output:
            classes_scores = row[4:]
            max_score = np.max(classes_scores)
            
            if max_score >= conf_threshold:
                class_id = np.argmax(classes_scores)
                
                # Filter out "No finding" (ID 14)
                if class_id == 14:
                    continue
                    
                # YOLOv8 box format: [x_center, y_center, width, height]
                x_center, y_center, width, height = row[:4]
                
                # Scale to original image size
                x1 = (x_center - width/2) * (w / input_w)
                y1 = (y_center - height/2) * (h / input_h)
                bw = width * (w / input_w)
                bh = height * (h / input_h)
                
                boxes.append([int(x1), int(y1), int(bw), int(bh)])
                scores.append(float(max_score))
                class_ids.append(int(class_id))
        
        # Apply NMS
        indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, iou_threshold)
        
        detections = []
        detected_findings = []
        
        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes[i]
                anomaly_name = self.names[class_ids[i]]
                detected_findings.append(anomaly_name)
                detections.append({
                    "name": anomaly_name,
                    "confidence": scores[i],
                    "box": [float(box[0]), float(box[1]), float(box[0] + box[2]), float(box[1] + box[3])] # x1, y1, x2, y2
                })
                
        return detections, list(set(detected_findings))

vision_engine = VisionModel()
