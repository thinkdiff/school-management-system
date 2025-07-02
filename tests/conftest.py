"""Test configuration and fixtures"""
import pytest
import os
from unittest.mock import MagicMock

# Set test environment variables
os.environ['MONGO_URI'] = 'mongodb://localhost:27017/'
os.environ['MONGO_DB_NAME'] = 'school_management_test'
os.environ['APP_SECRET_KEY'] = 'test-secret-key'
os.environ['APP_ENV'] = 'testing'

@pytest.fixture(scope="session")
def test_database():
    """Create test database connection"""
    # This would typically set up a test database
    # For now, we'll use mocks in individual tests
    pass

@pytest.fixture
def mock_streamlit_session():
    """Mock Streamlit session state"""
    mock_session = MagicMock()
    mock_session.authenticated = False
    mock_session.user_data = None
    mock_session.current_page = 'Dashboard'
    return mock_session

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        '_id': '507f1f77bcf86cd799439011',
        'username': 'testuser',
        'email': 'test@example.com',
        'role': 'student',
        'full_name': 'Test User',
        'is_active': True,
        'profile': {
            'phone': '+1234567890',
            'address': 'Test Address',
            'date_of_birth': None,
            'gender': None
        }
    }

@pytest.fixture
def sample_student_data():
    """Sample student data for testing"""
    return {
        '_id': '507f1f77bcf86cd799439012',
        'student_id': 'STU001',
        'user_id': '507f1f77bcf86cd799439011',
        'class_id': '507f1f77bcf86cd799439013',
        'admission_date': '2025-01-01',
        'status': 'active',
        'parent_ids': [],
        'subjects': ['math', 'science', 'english']
    }

@pytest.fixture
def sample_class_data():
    """Sample class data for testing"""
    return {
        '_id': '507f1f77bcf86cd799439013',
        'class_code': 'CLS001',
        'class_name': 'Grade 10A',
        'grade_level': 10,
        'academic_year': '2025-2026',
        'is_active': True,
        'max_students': 30,
        'subjects': ['math', 'science', 'english']
    }

@pytest.fixture
def sample_assignment_data():
    """Sample assignment data for testing"""
    return {
        '_id': '507f1f77bcf86cd799439014',
        'title': 'Math Assignment 1',
        'description': 'Solve the given problems',
        'class_id': '507f1f77bcf86cd799439013',
        'subject': 'math',
        'due_date': '2025-02-01',
        'created_by': '507f1f77bcf86cd799439015',
        'max_points': 100,
        'is_active': True,
        'submissions': []
    }