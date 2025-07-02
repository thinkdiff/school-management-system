import pytest
import os
from src.config.settings import Settings

class TestSettings:
    """Test Settings class"""
    
    def test_settings_initialization(self):
        """Test Settings class initialization"""
        settings = Settings()
        
        # Test default values
        assert settings.MONGO_DB_NAME == 'school_management'
        assert settings.APP_ENV == 'development'
        assert settings.SESSION_TIMEOUT_MINUTES == 30
        assert settings.MAX_LOGIN_ATTEMPTS == 3
        assert settings.PORT == 8501
        assert settings.HOST == '0.0.0.0'
    
    def test_user_roles(self):
        """Test user roles configuration"""
        settings = Settings()
        
        expected_roles = ['admin', 'teacher', 'student', 'parent']
        assert settings.USER_ROLES == expected_roles
    
    def test_grade_scale(self):
        """Test grade scale configuration"""
        settings = Settings()
        
        assert 'A+' in settings.GRADE_SCALE
        assert 'F' in settings.GRADE_SCALE
        assert settings.GRADE_SCALE['A+'] == (95, 100)
        assert settings.GRADE_SCALE['F'] == (0, 59)
    
    def test_get_database_config(self):
        """Test database configuration getter"""
        settings = Settings()
        config = settings.get_database_config()
        
        assert 'uri' in config
        assert 'database' in config
        assert config['database'] == 'school_management'
    
    def test_get_email_config(self):
        """Test email configuration getter"""
        settings = Settings()
        config = settings.get_email_config()
        
        assert 'smtp_server' in config
        assert 'smtp_port' in config
        assert 'username' in config
        assert 'password' in config
    
    def test_is_production(self):
        """Test production environment check"""
        settings = Settings()
        
        # Default should be development
        assert settings.is_production() is False
        
        # Test with production environment
        settings.APP_ENV = 'production'
        assert settings.is_production() is True
    
    def test_get_grade_from_score(self):
        """Test grade calculation from numeric score"""
        settings = Settings()
        
        assert settings.get_grade_from_score(98) == 'A+'
        assert settings.get_grade_from_score(92) == 'A'
        assert settings.get_grade_from_score(87) == 'B+'
        assert settings.get_grade_from_score(82) == 'B'
        assert settings.get_grade_from_score(77) == 'C+'
        assert settings.get_grade_from_score(72) == 'C'
        assert settings.get_grade_from_score(65) == 'D'
        assert settings.get_grade_from_score(55) == 'F'
        assert settings.get_grade_from_score(0) == 'F'
    
    @pytest.mark.parametrize("score,expected_grade", [
        (100, 'A+'),
        (95, 'A+'),
        (94, 'A'),
        (90, 'A'),
        (89, 'B+'),
        (85, 'B+'),
        (84, 'B'),
        (80, 'B'),
        (79, 'C+'),
        (75, 'C+'),
        (74, 'C'),
        (70, 'C'),
        (69, 'D'),
        (60, 'D'),
        (59, 'F'),
        (0, 'F')
    ])
    def test_grade_boundaries(self, score, expected_grade):
        """Test grade boundaries with parametrized tests"""
        settings = Settings()
        assert settings.get_grade_from_score(score) == expected_grade