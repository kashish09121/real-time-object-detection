import pytest
import numpy as np
from detector import ObjectDetector

@pytest.fixture
def detector():
    # Attempt to initialize, model path can be updated if we mock
    return ObjectDetector(model_path="yolov8n.pt")

def test_model_initialization(detector):
    assert detector.model_path == "yolov8n.pt"

def test_process_frame_empty(detector):
    # Create an empty black frame
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # In CI, if model isn't downloaded, process_frame handles it gracefully 
    # (returns frame, []) if is_model_loaded() is False.
    processed_frame, detections = detector.process_frame(frame, conf_threshold=0.5)
    
    assert isinstance(processed_frame, np.ndarray)
    assert isinstance(detections, list)
    
def test_class_filtering():
    detector = ObjectDetector(model_path="yolov8n.pt")
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    _, detections = detector.process_frame(frame, conf_threshold=0.1, selected_classes=["person", "car"])
    
    assert isinstance(detections, list)
