import pytest
import os
from unittest.mock import patch, MagicMock
from src.config.settings import Settings
from src.auth.authentication import Authentication
from src.database.models import UserModel

@pytest.fixture
def auth_instance():
    """Create Authentication instance for testing"""
    return Authentication()

@pytest.fixture
def mock_user_data():
    """Mock user data for testing"""
    return {
        '_id': '507f1f77bcf86cd799439011',
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3P0L9v4g0C',
        'role': 'student',
        'full_name': 'Test User',
        'is_active': True,
        'created_at': '2025-01-01T00:00:00Z',
        'updated_at': '2025-01-01T00:00:00Z'
    }

class TestAuthentication:
    """Test Authentication class"""
    
    def test_hash_password(self, auth_instance):
        """Test password hashing"""
        password = "testpassword123"
        hashed = auth_instance.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 50  # bcrypt hashes are typically 60 chars
        assert hashed.startswith('$2b$')
    
    def test_verify_password_correct(self, auth_instance):
        """Test password verification with correct password"""
        password = "testpassword123"
        hashed = auth_instance.hash_password(password)
        
        assert auth_instance.verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self, auth_instance):
        """Test password verification with incorrect password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = auth_instance.hash_password(password)
        
        assert auth_instance.verify_password(wrong_password, hashed) is False
    
    @patch('src.auth.authentication.UserModel')
    def test_authenticate_user_success(self, mock_user_model, auth_instance, mock_user_data):
        """Test successful user authentication"""
        # Setup mock
        mock_user_model_instance = MagicMock()
        mock_user_model.return_value = mock_user_model_instance
        
        # Hash the test password
        test_password = "testpassword123"
        mock_user_data['password'] = auth_instance.hash_password(test_password)
        
        mock_user_model_instance.find_one.return_value = mock_user_data
        mock_user_model_instance.update_by_id.return_value = True
        
        # Test authentication
        result = auth_instance.authenticate_user('testuser', test_password)
        
        assert result is not None
        assert result['username'] == 'testuser'
        assert 'password' not in result  # Password should be removed
    
    @patch('src.auth.authentication.UserModel')
    def test_authenticate_user_invalid_username(self, mock_user_model, auth_instance):
        """Test authentication with invalid username"""
        # Setup mock
        mock_user_model_instance = MagicMock()
        mock_user_model.return_value = mock_user_model_instance
        mock_user_model_instance.find_one.return_value = None
        
        # Test authentication
        result = auth_instance.authenticate_user('invaliduser', 'password')
        
        assert result is None
    
    @patch('src.auth.authentication.UserModel')
    def test_authenticate_user_invalid_password(self, mock_user_model, auth_instance, mock_user_data):
        """Test authentication with invalid password"""
        # Setup mock
        mock_user_model_instance = MagicMock()
        mock_user_model.return_value = mock_user_model_instance
        
        # Hash a different password
        mock_user_data['password'] = auth_instance.hash_password('correctpassword')
        mock_user_model_instance.find_one.return_value = mock_user_data
        
        # Test authentication with wrong password
        result = auth_instance.authenticate_user('testuser', 'wrongpassword')
        
        assert result is None
    
    def test_get_user_permissions_admin(self, auth_instance):
        """Test admin user permissions"""
        permissions = auth_instance.get_user_permissions('admin')
        
        assert permissions['manage_users'] is True
        assert permissions['manage_system'] is True
        assert permissions['view_reports'] is True
    
    def test_get_user_permissions_student(self, auth_instance):
        """Test student user permissions"""
        permissions = auth_instance.get_user_permissions('student')
        
        assert permissions.get('manage_users', True) is False
        assert permissions.get('manage_system', True) is False
        assert permissions.get('view_own_data', False) is True
    
    def test_has_permission_valid(self, auth_instance):
        """Test has_permission with valid permission"""
        assert auth_instance.has_permission('admin', 'manage_users') is True
        assert auth_instance.has_permission('student', 'view_own_data') is True
    
    def test_has_permission_invalid(self, auth_instance):
        """Test has_permission with invalid permission"""
        assert auth_instance.has_permission('student', 'manage_users') is False
        assert auth_instance.has_permission('teacher', 'manage_system') is False