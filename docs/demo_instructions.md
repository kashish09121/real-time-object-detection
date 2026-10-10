# Demonstration Video Preparation Guide

**Project:** Real-Time Object Detection Platform
**Creator:** Kashish

## Recording Setup
1. Ensure your webcam is working and well-lit.
2. Start your local MySQL server.
3. Open MySQL Workbench and connect to the `vision_platform` database.
4. Launch the Streamlit application: `streamlit run main.py`.
5. Use a screen recording tool (e.g., OBS Studio, Windows Game Bar `Win + Alt + R`, or Zoom).

## Demonstration Script (1–2 Minutes)

* **0–15 seconds:** 
  - Show the Streamlit dashboard home screen.
  - Introduce the project: "Hello, this is my Real-Time Object Detection Platform, created by Kashish."
  - Point out the sidebar showing successful MySQL and Model connections.

* **15–35 seconds:** 
  - Click **Start Detection** with the webcam source.
  - Show yourself on camera. Hold up an object like a cell phone or bottle to demonstrate YOLO detecting it and drawing bounding boxes.

* **35–55 seconds:** 
  - In the sidebar, change the **Confidence Threshold** (e.g., raise it to 0.8) and show how it affects detections.
  - Change the **Object Classes** filter to only detect "person" and show that other objects are ignored.

* **55–80 seconds:** 
  - Point to the **Real-Time KPI metrics** (FPS, Objects in Frame).
  - Switch to the **Detection Logs** tab and click "Refresh" to show logs populating.
  - Switch to the **Analytics** tab to show the charts updating.

* **80–100 seconds:** 
  - Click **Stop** in the Streamlit app.
  - Switch your screen to MySQL Workbench.
  - Run `SELECT * FROM detection_logs ORDER BY timestamp DESC LIMIT 20;` to prove records were actually inserted into the database.

* **100–120 seconds:** 
  - Briefly show the VS Code project structure or the GitHub repository page.
  - Conclude: "Thank you for watching."

## Post-Recording
1. Review the video to ensure no sensitive passwords are shown.
2. Upload the video to Google Drive or YouTube (as an Unlisted video).
3. Add the video link to the `README.md` placeholder.
