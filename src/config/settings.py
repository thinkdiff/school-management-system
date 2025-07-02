import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    def __init__(self):
        self.load_settings()
    
    def load_settings(self):
        """Load all configuration settings"""
        
        # Database Configuration
        self.MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'school_management')
        
        # Application Configuration
        self.APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'default-secret-key')
        self.APP_ENV = os.getenv('APP_ENV', 'development')
        self.APP_DEBUG = os.getenv('APP_DEBUG', 'True').lower() == 'true'
        
        # Security Settings
        self.SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))
        self.MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 3))
        
        # Server Settings
        self.PORT = int(os.getenv('PORT', 8501))
        self.HOST = os.getenv('HOST', '0.0.0.0')
        
        # Email Configuration (Optional)
        self.SMTP_SERVER = os.getenv('SMTP_SERVER', '')
        self.SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
        self.EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
        self.EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        
        # Application Constants
        self.USER_ROLES = ['admin', 'teacher', 'student', 'parent']
        self.GRADE_SCALE = {
            'A+': (95, 100),
            'A': (90, 94),
            'B+': (85, 89),
            'B': (80, 84),
            'C+': (75, 79),
            'C': (70, 74),
            'D': (60, 69),
            'F': (0, 59)
        }
        
        # UI Configuration
        self.ITEMS_PER_PAGE = 10
        self.CHART_COLORS = [
            '#667eea', '#764ba2', '#f093fb', '#f5576c',
            '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'
        ]
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            'uri': self.MONGO_URI,
            'database': self.MONGO_DB_NAME
        }
    
    def get_email_config(self) -> Dict[str, Any]:
        """Get email configuration"""
        return {
            'smtp_server': self.SMTP_SERVER,
            'smtp_port': self.SMTP_PORT,
            'username': self.EMAIL_USERNAME,
            'password': self.EMAIL_PASSWORD
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.APP_ENV.lower() == 'production'
    
    def get_grade_from_score(self, score: float) -> str:
        """Get letter grade from numeric score"""
        for grade, (min_score, max_score) in self.GRADE_SCALE.items():
            if min_score <= score <= max_score:
                return grade
        return 'F'