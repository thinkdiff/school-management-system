import pytest
from unittest.mock import patch, MagicMock
from src.database.models import UserModel, StudentModel, TeacherModel, ClassModel

class TestUserModel:
    """Test UserModel class"""
    
    @patch('src.database.models.BaseModel.__init__')
    def test_user_model_init(self, mock_base_init):
        """Test UserModel initialization"""
        UserModel()
        mock_base_init.assert_called_once_with('users')
    
    @patch('src.database.models.BaseModel.find_one')
    @patch('src.database.models.BaseModel.create')
    def test_create_user_success(self, mock_create, mock_find_one):
        """Test successful user creation"""
        # Setup
        mock_find_one.return_value = None  # No existing user
        mock_create.return_value = "507f1f77bcf86cd799439011"
        
        user_model = UserModel()
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'hashedpassword',
            'role': 'student',
            'full_name': 'Test User'
        }
        
        # Test
        result = user_model.create_user(user_data)
        
        # Assert
        assert result == "507f1f77bcf86cd799439011"
        mock_create.assert_called_once()
    
    @patch('src.database.models.BaseModel.find_one')
    def test_create_user_duplicate_username(self, mock_find_one):
        """Test user creation with duplicate username"""
        # Setup - simulate existing user
        mock_find_one.return_value = {'username': 'testuser'}
        
        user_model = UserModel()
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'hashedpassword',
            'role': 'student',
            'full_name': 'Test User'
        }
        
        # Test
        with pytest.raises(ValueError, match="Username already exists"):
            user_model.create_user(user_data)
    
    def test_create_user_missing_required_field(self):
        """Test user creation with missing required field"""
        user_model = UserModel()
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            # Missing password, role, full_name
        }
        
        with pytest.raises(ValueError, match="Missing required field"):
            user_model.create_user(user_data)
    
    @patch('src.database.models.BaseModel.find_one')
    def test_authenticate(self, mock_find_one):
        """Test user authentication"""
        # Setup
        expected_user = {
            'username': 'testuser',
            'password': 'hashedpassword',
            'is_active': True
        }
        mock_find_one.return_value = expected_user
        
        user_model = UserModel()
        
        # Test
        result = user_model.authenticate('testuser', 'hashedpassword')
        
        # Assert
        assert result == expected_user
        mock_find_one.assert_called_once_with({
            'username': 'testuser',
            'password': 'hashedpassword',
            'is_active': True
        })
    
    @patch('src.database.models.BaseModel.find_many')
    def test_get_users_by_role(self, mock_find_many):
        """Test getting users by role"""
        # Setup
        expected_users = [
            {'username': 'teacher1', 'role': 'teacher'},
            {'username': 'teacher2', 'role': 'teacher'}
        ]
        mock_find_many.return_value = expected_users
        
        user_model = UserModel()
        
        # Test
        result = user_model.get_users_by_role('teacher')
        
        # Assert
        assert result == expected_users
        mock_find_many.assert_called_once_with({'role': 'teacher', 'is_active': True})

class TestStudentModel:
    """Test StudentModel class"""
    
    @patch('src.database.models.BaseModel.__init__')
    def test_student_model_init(self, mock_base_init):
        """Test StudentModel initialization"""
        StudentModel()
        mock_base_init.assert_called_once_with('students')
    
    @patch('src.database.models.BaseModel.find_one')
    @patch('src.database.models.BaseModel.create')
    def test_create_student_success(self, mock_create, mock_find_one):
        """Test successful student creation"""
        # Setup
        mock_find_one.return_value = None  # No existing student
        mock_create.return_value = "507f1f77bcf86cd799439012"
        
        student_model = StudentModel()
        student_data = {
            'student_id': 'STU001',
            'user_id': '507f1f77bcf86cd799439011',
            'class_id': '507f1f77bcf86cd799439013',
            'admission_date': '2025-01-01'
        }
        
        # Test
        result = student_model.create_student(student_data)
        
        # Assert
        assert result == "507f1f77bcf86cd799439012"
        mock_create.assert_called_once()
    
    @patch('src.database.models.BaseModel.find_one')
    def test_create_student_duplicate_id(self, mock_find_one):
        """Test student creation with duplicate student ID"""
        # Setup - simulate existing student
        mock_find_one.return_value = {'student_id': 'STU001'}
        
        student_model = StudentModel()
        student_data = {
            'student_id': 'STU001',
            'user_id': '507f1f77bcf86cd799439011',
            'class_id': '507f1f77bcf86cd799439013',
            'admission_date': '2025-01-01'
        }
        
        # Test
        with pytest.raises(ValueError, match="Student ID already exists"):
            student_model.create_student(student_data)
    
    @patch('src.database.models.BaseModel.find_one')
    def test_get_student_by_user_id(self, mock_find_one):
        """Test getting student by user ID"""
        # Setup
        expected_student = {
            'student_id': 'STU001',
            'user_id': '507f1f77bcf86cd799439011'
        }
        mock_find_one.return_value = expected_student
        
        student_model = StudentModel()
        
        # Test
        result = student_model.get_student_by_user_id('507f1f77bcf86cd799439011')
        
        # Assert
        assert result == expected_student
        mock_find_one.assert_called_once_with({'user_id': '507f1f77bcf86cd799439011'})

class TestClassModel:
    """Test ClassModel class"""
    
    @patch('src.database.models.BaseModel.__init__')
    def test_class_model_init(self, mock_base_init):
        """Test ClassModel initialization"""
        ClassModel()
        mock_base_init.assert_called_once_with('classes')
    
    @patch('src.database.models.BaseModel.find_one')
    @patch('src.database.models.BaseModel.create')
    def test_create_class_success(self, mock_create, mock_find_one):
        """Test successful class creation"""
        # Setup
        mock_find_one.return_value = None  # No existing class
        mock_create.return_value = "507f1f77bcf86cd799439014"
        
        class_model = ClassModel()
        class_data = {
            'class_code': 'CLS001',
            'class_name': 'Grade 10A',
            'grade_level': 10,
            'academic_year': '2025-2026'
        }
        
        # Test
        result = class_model.create_class(class_data)
        
        # Assert
        assert result == "507f1f77bcf86cd799439014"
        mock_create.assert_called_once()
    
    @patch('src.database.models.BaseModel.find_many')
    def test_get_active_classes(self, mock_find_many):
        """Test getting active classes"""
        # Setup
        expected_classes = [
            {'class_code': 'CLS001', 'is_active': True},
            {'class_code': 'CLS002', 'is_active': True}
        ]
        mock_find_many.return_value = expected_classes
        
        class_model = ClassModel()
        
        # Test
        result = class_model.get_active_classes()
        
        # Assert
        assert result == expected_classes
        mock_find_many.assert_called_once_with({'is_active': True})