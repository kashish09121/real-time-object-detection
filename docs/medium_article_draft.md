# Building a Real-Time Object Detection Platform Using Python, YOLO, OpenCV, and MySQL

*By Kashish*

## 1. Introduction
Computer vision is transforming how we interact with the world. From self-driving cars to security systems, the ability for machines to "see" and understand objects is powerful. For my academic project, I decided to build a complete Real-Time Object Detection Platform from scratch.

## 2. Project Objectives
The goal was to create a functional, robust application that could:
1. Detect objects in real-time via a webcam.
2. Provide a user-friendly dashboard for configuration.
3. Log detection events into a persistent database for analytics.

## 3. Learning OpenCV and Computer Vision
OpenCV is the backbone of video processing in Python. I used it to capture frames from the webcam (`cv2.VideoCapture`), convert color spaces (BGR to RGB for the UI), and draw bounding boxes and text labels. 

## 4. Understanding YOLO Object Detection
I integrated Ultralytics YOLOv8 (specifically `yolov8n.pt`, the nano model) for object detection. It is incredibly fast and lightweight, making it perfect for running on a standard student laptop without requiring a high-end GPU. YOLO processes the frame and returns bounding box coordinates, class labels, and confidence scores.

## 5. Designing a Modular Python Architecture
Instead of writing a single monolithic script, I separated the code into modular files:
- `detector.py`: Handles YOLO and OpenCV.
- `database.py`: Manages MySQL connections and queries.
- `ui.py`: Contains the Streamlit dashboard logic.
- `config.py`: Stores constants and loads environment variables.
- `main.py`: The entry point.

## 6. Integrating MySQL for Detection Event Logging
To keep track of what the camera saw, I integrated MySQL using `mysql-connector-python`. I created a table called `detection_logs` to store the timestamp, object class, confidence, and coordinates. To prevent database spamming, I implemented a logging interval that only saves records every few frames.

## 7. Building the Streamlit Dashboard
Streamlit made it easy to build a responsive, professional UI without writing raw HTML/CSS/JS. I created a sidebar for settings (confidence thresholds, class filtering) and main tabs for the live video feed, tabular logs, and Plotly analytics charts.

## 8. Challenges Encountered and Solutions
*(Kashish: Add a personal challenge here. For example: Figuring out how to prevent Streamlit from freezing while the `while` loop was processing video frames, or handling database disconnects gracefully.)*

## 9. Testing and Validation
I wrote automated tests using `pytest` to validate my configuration loading, database connection logic, and detector initialization. Testing without a physical webcam was achieved by passing numpy arrays (blank frames) to the detector.

## 10. Key Learning Outcomes
This project bridged the gap between machine learning and software engineering. I learned how to handle real-time data streams, manage database connections securely using `.env` files, and build interactive web applications.

## 11. Project Results and Limitations
The application runs smoothly at around *(Kashish: Insert your FPS here)* FPS on my machine. A current limitation is that the `yolov8n` model can struggle with very small objects. In the future, I plan to add support for exporting analytics to CSV and adding email alerts for specific object detections.

## 12. GitHub Repository and Demonstration Links
- **GitHub Repository**: [Insert URL]
- **Demo Video**: [Insert URL]

## 13. Conclusion
Building this platform was a fantastic learning experience. It proves that with the right Python libraries, building complex AI-integrated software is more accessible than ever.
