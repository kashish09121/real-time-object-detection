import mysql.connector
from mysql.connector import Error
import config
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self):
        self.host = config.DB_HOST
        self.port = config.DB_PORT
        self.database = config.DB_NAME
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.connection = None

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            self.connection = None
        return False

    def is_connected(self):
        """Check if the database connection is active."""
        if self.connection is not None and self.connection.is_connected():
            return True
        return False

    def close(self):
        """Close the database connection safely."""
        if self.is_connected():
            self.connection.close()
            logging.info("MySQL connection closed.")

    def log_detection(self, object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h):
        """Insert a detection event into the database."""
        if not self.is_connected():
            return False
            
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO detection_logs 
                (object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (object_class, float(confidence), int(bbox_x), int(bbox_y), int(bbox_w), int(bbox_h))
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            logging.error(f"Failed to insert record into MySQL table: {e}")
            return False

    def get_recent_logs(self, limit=50):
        """Retrieve recent detection logs."""
        if not self.is_connected():
            return []
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"""
                SELECT log_id, timestamp, object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h 
                FROM detection_logs 
                ORDER BY timestamp DESC 
                LIMIT {limit}
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            logging.error(f"Failed to retrieve records: {e}")
            return []
            
    def get_class_counts(self):
        """Retrieve count of detections per object class."""
        if not self.is_connected():
            return []
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT object_class, COUNT(*) as count 
                FROM detection_logs 
                GROUP BY object_class
                ORDER BY count DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            logging.error(f"Failed to retrieve class counts: {e}")
            return []
            
    def get_detections_over_time(self):
        """Retrieve detection counts over time."""
        if not self.is_connected():
            return []
            
        try:
            # Group by minute intervals
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:00') as time_interval, COUNT(*) as count
                FROM detection_logs
                GROUP BY time_interval
                ORDER BY time_interval ASC
                LIMIT 100
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            logging.error(f"Failed to retrieve detections over time: {e}")
            return []
