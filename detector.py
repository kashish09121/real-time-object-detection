import cv2
from ultralytics import YOLO
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model_path = model_path
        self.model = None
        self.load_model()
        
    def load_model(self):
        """Load the YOLO model."""
        try:
            self.model = YOLO(self.model_path)
            logging.info(f"Successfully loaded YOLO model: {self.model_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to load YOLO model: {e}")
            self.model = None
            return False
            
    def is_model_loaded(self):
        return self.model is not None

    def process_frame(self, frame, conf_threshold=0.5, selected_classes=None):
        """
        Process a single frame to detect objects.
        Returns:
            processed_frame (numpy.ndarray): Frame with bounding boxes drawn.
            detections (list): List of dictionaries containing detection info.
        """
        if not self.is_model_loaded():
            return frame, []
            
        # Run inference
        results = self.model(frame, verbose=False)[0]
        
        detections = []
        
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf < conf_threshold:
                continue
                
            cls_id = int(box.cls[0])
            class_name = self.model.names[cls_id]
            
            # Filter by class if selected_classes is provided
            if selected_classes and "All" not in selected_classes and class_name not in selected_classes:
                continue
                
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            bbox_x = x1
            bbox_y = y1
            bbox_w = x2 - x1
            bbox_h = y2 - y1
            
            detections.append({
                'class_name': class_name,
                'confidence': conf,
                'bbox_x': bbox_x,
                'bbox_y': bbox_y,
                'bbox_w': bbox_w,
                'bbox_h': bbox_h
            })
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"{class_name} {conf:.2f}"
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
        return frame, detections
