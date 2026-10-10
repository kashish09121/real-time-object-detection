CREATE DATABASE IF NOT EXISTS vision_platform;

USE vision_platform;

CREATE TABLE IF NOT EXISTS detection_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    object_class VARCHAR(100) NOT NULL,
    confidence DECIMAL(6,5) NOT NULL,
    bbox_x INT NOT NULL,
    bbox_y INT NOT NULL,
    bbox_w INT NOT NULL,
    bbox_h INT NOT NULL
);

-- Optional: Create index on timestamp for faster time-based queries
CREATE INDEX idx_timestamp ON detection_logs(timestamp);
-- Optional: Create index on object_class for faster grouping
CREATE INDEX idx_object_class ON detection_logs(object_class);
