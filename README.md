# Real-Time Object Detection Platform

**Project Created By:** Kashish

## Project Overview
This project is a complete, functional, real-time computer vision application that detects objects through a live webcam or uploaded video. It draws bounding boxes around detected objects, allows users to configure detection settings, displays real-time analytics through a modular dashboard, and automatically stores detection events in a MySQL database.

## Features
- **Real-Time Object Detection**: Uses YOLOv8 for fast and accurate object recognition.
- **Multiple Video Sources**: Supports webcam and uploaded video files.
- **Configurable Settings**: Adjust confidence thresholds, filter by object classes, and control logging intervals.
- **Interactive Dashboard**: Built with Streamlit for live viewing and analytics.
- **Database Logging**: Persistent storage of detection events in a MySQL database.
- **Analytics**: Real-time KPI metrics and historical charts using Plotly.

## Technology Stack
- **Python**: Core application logic.
- **OpenCV**: Video processing and frame manipulation.
- **Ultralytics YOLO**: Pretrained object detection model (YOLOv8n).
- **Streamlit**: Web-based dashboard.
- **MySQL**: Persistent storage for detection logs.
- **mysql-connector-python**: Python-to-MySQL connectivity.
- **Pandas & Plotly**: Data manipulation and interactive charts.

## Architecture
- `main.py`: Application entry point.
- `detector.py`: YOLO object detection engine.
- `database.py`: MySQL connection and query management.
- `ui.py`: Streamlit dashboard implementation.
- `config.py`: Configuration and environment variable handling.

## Prerequisites
- Python 3.9 or higher
- MySQL Server installed and running
- A webcam (for live detection)

## Installation Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Set up a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **YOLO Model Setup:**
   The `yolov8n.pt` model will be downloaded automatically by the Ultralytics library on the first run. Ensure you have an active internet connection.

5. **MySQL Configuration:**
   - Open MySQL Workbench or the MySQL command line.
   - Execute the SQL script to create the database and table:
     ```sql
     SOURCE database_schema.sql;
     ```
   - Alternatively, copy and paste the contents of `database_schema.sql` into your SQL client.

6. **Environment Variables:**
   - Copy the `.env.example` file to `.env`:
     ```powershell
     cp .env.example .env
     ```
   - Open `.env` and fill in your actual local MySQL credentials (`DB_USER` and `DB_PASSWORD`).

## Application Startup Commands

To launch the dashboard, run:
```powershell
streamlit run main.py
```

## Dashboard Usage Instructions
1. Open the local URL provided by Streamlit in your web browser.
2. In the sidebar, verify the MySQL Connection and Model Loaded statuses.
3. Select your video source (Webcam or Video File).
4. Adjust the Confidence Threshold and Object Classes if needed.
5. Click **Start Detection**.
6. View the live feed and real-time metrics in the first tab.
7. Switch to the **Detection Logs** tab to view recent database entries (click "Refresh Logs" to update).
8. Switch to the **Analytics** tab to view charts of detection data.
9. Click **Stop** in the sidebar to end the detection session and release the camera.

## Testing Instructions
To run the automated test suite using `pytest`:
```powershell
pytest tests/
```

## Troubleshooting
- **Model Download Fails**: Check your internet connection. You can also manually download `yolov8n.pt` and place it in the project root.
- **Webcam Not Opening**: Ensure no other application (e.g., Zoom, Teams) is using the webcam.
- **MySQL Connection Error**: Double-check your `.env` credentials and ensure the MySQL server is running.
- **Dependency Issues**: Ensure you are using the virtual environment where you installed `requirements.txt`.

## Screenshots
*(Add screenshots of the dashboard, detection feed, and database logs here)*

## Demo Video
[Link to Demo Video] *(Placeholder)*

## Learning Outcomes
- Implementing state-of-the-art computer vision models (YOLO).
- Processing video streams in real-time with OpenCV.
- Designing responsive web dashboards with Streamlit.
- Persisting structured data to a relational database (MySQL).
- Managing modular Python applications and secure configurations.

## Limitations and Future Improvements
- **Limitations**: The tiny model (`yolov8n`) might struggle with small objects or poor lighting. Logging every frame can rapidly increase database size.
- **Improvements**: Implement GPU acceleration for higher FPS, add user authentication, and support exporting data to CSV/PDF.
