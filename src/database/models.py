from src.database.connection import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserModel(BaseModel):
    """User model for authentication and user management"""
    
    def __init__(self):
        super().__init__('users')
    
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user with validation"""
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role', 'full_name']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if username or email already exists
        if self.find_one({'username': user_data['username']}):
            raise ValueError("Username already exists")
        
        if self.find_one({'email': user_data['email']}):
            raise ValueError("Email already exists")
        
        # Set default values
        user_data.setdefault('is_active', True)
        user_data.setdefault('profile', {})
        
        return self.create(user_data)
    
    def authenticate(self, username: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password hash"""
        return self.find_one({
            'username': username,
            'password': password_hash,
            'is_active': True
        })
    
    def get_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get all users by role"""
        return self.find_many({'role': role, 'is_active': True})

class StudentModel(BaseModel):
    """Student model for student-specific data"""
    
    def __init__(self):
        super().__init__('students')
    
    def create_student(self, student_data: Dict[str, Any]) -> str:
        """Create a new student record"""
        required_fields = ['student_id', 'user_id', 'class_id', 'admission_date']
        for field in required_fields:
            if field not in student_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if student_id already exists
        if self.find_one({'student_id': student_data['student_id']}):
            raise ValueError("Student ID already exists")
        
        # Set default values
        student_data.setdefault('status', 'active')
        student_data.setdefault('parent_ids', [])
        student_data.setdefault('subjects', [])
        
        return self.create(student_data)
    
    def get_student_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get student record by user ID"""
        return self.find_one({'user_id': user_id})
    
    def get_students_by_class(self, class_id: str) -> List[Dict[str, Any]]:
        """Get all students in a class"""
        return self.find_many({'class_id': class_id, 'status': 'active'})

class TeacherModel(BaseModel):
    """Teacher model for teacher-specific data"""
    
    def __init__(self):
        super().__init__('teachers')
    
    def create_teacher(self, teacher_data: Dict[str, Any]) -> str:
        """Create a new teacher record"""
        required_fields = ['teacher_id', 'user_id', 'subjects', 'hire_date']
        for field in required_fields:
            if field not in teacher_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if teacher_id already exists
        if self.find_one({'teacher_id': teacher_data['teacher_id']}):
            raise ValueError("Teacher ID already exists")
        
        # Set default values
        teacher_data.setdefault('status', 'active')
        teacher_data.setdefault('class_ids', [])
        
        return self.create(teacher_data)
    
    def get_teacher_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get teacher record by user ID"""
        return self.find_one({'user_id': user_id})

class ClassModel(BaseModel):
    """Class model for class management"""
    
    def __init__(self):
        super().__init__('classes')
    
    def create_class(self, class_data: Dict[str, Any]) -> str:
        """Create a new class"""
        required_fields = ['class_code', 'class_name', 'grade_level', 'academic_year']
        for field in required_fields:
            if field not in class_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if class_code already exists
        if self.find_one({'class_code': class_data['class_code']}):
            raise ValueError("Class code already exists")
        
        # Set default values
        class_data.setdefault('is_active', True)
        class_data.setdefault('max_students', 30)
        class_data.setdefault('subjects', [])
        
        return self.create(class_data)
    
    def get_active_classes(self) -> List[Dict[str, Any]]:
        """Get all active classes"""
        return self.find_many({'is_active': True})

class AttendanceModel(BaseModel):
    """Attendance model for tracking student attendance"""
    
    def __init__(self):
        super().__init__('attendance')
    
    def mark_attendance(self, attendance_data: Dict[str, Any]) -> str:
        """Mark attendance for a student"""
        required_fields = ['student_id', 'class_id', 'date', 'status']
        for field in required_fields:
            if field not in attendance_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if attendance already marked for this date
        existing = self.find_one({
            'student_id': attendance_data['student_id'],
            'date': attendance_data['date']
        })
        
        if existing:
            # Update existing attendance
            return self.update_by_id(existing['_id'], attendance_data)
        else:
            # Create new attendance record
            return self.create(attendance_data)
    
    def get_student_attendance(self, student_id: str, start_date: datetime = None, end_date: datetime = None) -> List[Dict[str, Any]]:
        """Get attendance records for a student"""
        query = {'student_id': student_id}
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['date'] = date_query
        
        return self.find_many(query, sort=[('date', -1)])

class AssignmentModel(BaseModel):
    """Assignment model for managing assignments"""
    
    def __init__(self):
        super().__init__('assignments')
    
    def create_assignment(self, assignment_data: Dict[str, Any]) -> str:
        """Create a new assignment"""
        required_fields = ['title', 'description', 'class_id', 'subject', 'due_date', 'created_by']
        for field in required_fields:
            if field not in assignment_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Set default values
        assignment_data.setdefault('max_points', 100)
        assignment_data.setdefault('is_active', True)
        assignment_data.setdefault('submissions', [])
        
        return self.create(assignment_data)
    
    def get_assignments_by_class(self, class_id: str) -> List[Dict[str, Any]]:
        """Get all assignments for a class"""
        return self.find_many({'class_id': class_id, 'is_active': True}, sort=[('due_date', 1)])

class GradeModel(BaseModel):
    """Grade model for managing student grades"""
    
    def __init__(self):
        super().__init__('grades')
    
    def record_grade(self, grade_data: Dict[str, Any]) -> str:
        """Record a grade for a student"""
        required_fields = ['student_id', 'assignment_id', 'points_earned', 'max_points', 'graded_by']
        for field in required_fields:
            if field not in grade_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Calculate percentage and letter grade
        percentage = (grade_data['points_earned'] / grade_data['max_points']) * 100
        grade_data['percentage'] = percentage
        
        # Check if grade already exists
        existing = self.find_one({
            'student_id': grade_data['student_id'],
            'assignment_id': grade_data['assignment_id']
        })
        
        if existing:
            # Update existing grade
            return self.update_by_id(existing['_id'], grade_data)
        else:
            # Create new grade record
            return self.create(grade_data)
    
    def get_student_grades(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all grades for a student"""
        return self.find_many({'student_id': student_id}, sort=[('created_at', -1)])

class AnnouncementModel(BaseModel):
    """Announcement model for managing announcements"""
    
    def __init__(self):
        super().__init__('announcements')
    
    def create_announcement(self, announcement_data: Dict[str, Any]) -> str:
        """Create a new announcement"""
        required_fields = ['title', 'content', 'created_by', 'target_audience']
        for field in required_fields:
            if field not in announcement_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Set default values
        announcement_data.setdefault('is_active', True)
        announcement_data.setdefault('priority', 'normal')
        
        return self.create(announcement_data)
    
    def get_announcements_for_role(self, role: str) -> List[Dict[str, Any]]:
        """Get announcements for a specific role"""
        return self.find_many({
            'target_audience': {'$in': [role, 'all']},
            'is_active': True
        }, sort=[('created_at', -1)])