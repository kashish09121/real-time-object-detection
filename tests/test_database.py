import pytest
from database import DatabaseManager

@pytest.fixture
def db():
    return DatabaseManager()

def test_db_initialization(db):
    assert db.host is not None
    assert db.database == "vision_platform"
    
def test_db_connection_fail_gracefully(db):
    # Intentionally bad port to test failure handling
    db.port = 99999 
    status = db.connect()
    
    assert status == False
    assert db.is_connected() == False
    
def test_log_detection_no_connection(db):
    # Ensure logging doesn't crash when not connected
    db.connection = None
    result = db.log_detection("person", 0.95, 10, 10, 100, 100)
    assert result == False
