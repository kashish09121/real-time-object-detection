import streamlit as st
import cv2
import time
from detector import ObjectDetector
from database import DatabaseManager
import config
import tempfile

def render_dashboard():
    st.set_page_config(page_title="Real-Time Object Detection", page_icon="👁️", layout="wide")
    
    st.title("Real-Time Object Detection and Monitoring Platform")
    st.markdown("**Project Created By: Kashish** | Powered by YOLO, OpenCV, and MySQL")
    
    # Initialize components in session state
    if 'detector' not in st.session_state:
        st.session_state.detector = ObjectDetector(config.DEFAULT_MODEL)
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseManager()
    if 'is_detecting' not in st.session_state:
        st.session_state.is_detecting = False
    
    # Check Database Connection Status
    db_status = st.session_state.db.connect()
    
    # --- Sidebar ---
    with st.sidebar:
        st.header("Settings")
        
        # Connection Status
        if db_status:
            st.success("✅ MySQL Connected")
        else:
            st.error("❌ MySQL Disconnected")
            
        if st.session_state.detector.is_model_loaded():
            st.success("✅ YOLO Model Loaded")
        else:
            st.error("❌ Model Loading Failed")
            
        st.markdown("---")
        
        # Detection Controls
        st.subheader("Detection Configuration")
        conf_threshold = st.slider("Confidence Threshold", 0.1, 0.95, config.CONFIDENCE_THRESHOLD, 0.05)
        
        classes_options = ["All"] + config.COCO_CLASSES
        selected_classes = st.multiselect("Object Classes", options=classes_options, default=["All"])
        
        source = st.selectbox("Video Source", ["Webcam", "Video File"])
        video_file = None
        if source == "Video File":
            video_file = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov'])
            
        enable_logging = st.checkbox("Enable Database Logging", value=True)
        log_interval = st.number_input("Logging Interval (frames)", min_value=1, max_value=300, value=10, help="Log to database every N frames to avoid spam.")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Detection", type="primary", use_container_width=True):
                st.session_state.is_detecting = True
        with col2:
            if st.button("Stop", type="secondary", use_container_width=True):
                st.session_state.is_detecting = False
                
    # --- Main Content ---
    
    tab1, tab2, tab3 = st.tabs(["Live Feed & KPIs", "Detection Logs", "Analytics"])
    
    # Initialize placeholder for video and metrics
    frame_placeholder = tab1.empty()
    metrics_placeholder = tab1.empty()
    
    if not st.session_state.is_detecting:
        frame_placeholder.info("Detection is stopped. Press 'Start Detection' in the sidebar.")
    
    # Tab 2: Logs
    with tab2:
        logs_placeholder = st.empty()
        if st.button("Refresh Logs"):
            pass # Triggers a rerun
        
        if db_status:
            logs_data = st.session_state.db.get_recent_logs()
            if logs_data:
                md = "| ID | Timestamp | Class | Confidence | Box X | Box Y | Box W | Box H |\n|---|---|---|---|---|---|---|---|\n"
                for row in logs_data:
                    md += f"| {row['log_id']} | {row['timestamp']} | {row['object_class']} | {row['confidence']:.2f} | {row['bbox_x']} | {row['bbox_y']} | {row['bbox_w']} | {row['bbox_h']} |\n"
                logs_placeholder.markdown(md)
            else:
                logs_placeholder.info("No logs found in the database.")
        else:
            logs_placeholder.warning("Database not connected.")
            
    # Tab 3: Analytics
    with tab3:
        if db_status:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                counts_data = st.session_state.db.get_class_counts()
                if counts_data:
                    md = "| Object Class | Count |\n|---|---|\n"
                    for row in counts_data:
                        md += f"| {row['object_class']} | {row['count']} |\n"
                    st.markdown("### Detections by Object Class\n" + md)
                else:
                    st.info("Not enough data for class counts chart.")
                    
            with col_chart2:
                time_data = st.session_state.db.get_detections_over_time()
                if time_data:
                    md = "| Time Interval | Count |\n|---|---|\n"
                    for row in time_data:
                        md += f"| {row['time_interval']} | {row['count']} |\n"
                    st.markdown("### Detections Over Time\n" + md)
                else:
                    st.info("Not enough data for timeline chart.")
        else:
            st.warning("Database not connected.")

    # Detection Loop
    if st.session_state.is_detecting:
        cap = None
        if source == "Webcam":
            cap = cv2.VideoCapture(0)
        elif source == "Video File" and video_file is not None:
            # Save uploaded file temporarily to read with OpenCV
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(video_file.read())
            tfile.close()
            cap = cv2.VideoCapture(tfile.name)
            
        if cap is None or not cap.isOpened():
            st.error("Error: Could not open video source.")
            st.session_state.is_detecting = False
            st.rerun()
            
        frame_count = 0
        total_objects_session = 0
        unique_classes_session = set()
        last_logged_time = {}
        
        prev_time = time.time()
        
        while st.session_state.is_detecting:
            ret, frame = cap.read()
            if not ret:
                st.info("Video stream ended.")
                st.session_state.is_detecting = False
                break
                
            frame_count += 1
            
            # Convert BGR to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            processed_frame, detections = st.session_state.detector.process_frame(
                frame_rgb, 
                conf_threshold=conf_threshold, 
                selected_classes=selected_classes
            )
            
            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if curr_time - prev_time > 0 else 0
            prev_time = curr_time
            
            # Update metrics
            current_objects = len(detections)
            total_objects_session += current_objects
            avg_conf = sum([d['confidence'] for d in detections]) / current_objects if current_objects > 0 else 0
            
            for d in detections:
                unique_classes_session.add(d['class_name'])
                
            # Database Logging
            if enable_logging and db_status:
                curr_t = time.time()
                for d in detections:
                    cls = d['class_name']
                    # Log object if it hasn't been logged in the last 1 second
                    if curr_t - last_logged_time.get(cls, 0) > 1.0:
                        st.session_state.db.log_detection(
                            cls, d['confidence'], 
                            d['bbox_x'], d['bbox_y'], d['bbox_w'], d['bbox_h']
                        )
                        last_logged_time[cls] = curr_t
            
            # Display frame
            frame_placeholder.image(processed_frame, channels="RGB", use_container_width=True)
            
            # Display metrics
            with metrics_placeholder.container():
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Objects in Frame", current_objects)
                c2.metric("Processing FPS", f"{fps:.1f}")
                c3.metric("Avg Confidence", f"{avg_conf:.1%}")
                c4.metric("Session Detections", total_objects_session)
                
            # Prevent 100% CPU on extremely fast processing
            time.sleep(0.01)
            
        # Cleanup
        if cap is not None:
            cap.release()
            
        st.session_state.db.close()
