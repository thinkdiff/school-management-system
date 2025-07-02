from typing import Dict, Any, List
import streamlit as st
from src.database.models import UserModel, StudentModel, TeacherModel
from src.auth.authentication import Authentication
import logging

logger = logging.getLogger(__name__)

class Authorization:
    """Role-based access control and authorization"""
    
    def __init__(self):
        self.auth = Authentication()
        self.user_model = UserModel()
        self.student_model = StudentModel()
        self.teacher_model = TeacherModel()
    
    def get_user_role(self) -> str:
        """Get current user's role"""
        if not st.session_state.get('authenticated', False):
            return 'guest'
        
        user_data = st.session_state.get('user_data', {})
        return user_data.get('role', 'guest')
    
    def get_user_id(self) -> str:
        """Get current user's ID"""
        if not st.session_state.get('authenticated', False):
            return ''
        
        user_data = st.session_state.get('user_data', {})
        return user_data.get('_id', '')
    
    def get_accessible_pages(self) -> List[str]:
        """Get list of pages accessible to current user"""
        role = self.get_user_role()
        
        pages = {
            'admin': [
                'Dashboard', 'User Management', 'Class Management', 
                'Student Management', 'Teacher Management', 'Attendance',
                'Assignments', 'Grades', 'Reports', 'Announcements', 
                'System Settings'
            ],
            'teacher': [
                'Dashboard', 'My Classes', 'Attendance', 'Assignments',
                'Grades', 'Students', 'Announcements'
            ],
            'student': [
                'Dashboard', 'My Classes', 'Assignments', 'Grades',
                'Attendance', 'Announcements'
            ],
            'parent': [
                'Dashboard', 'Child Progress', 'Attendance', 'Grades',
                'Announcements', 'Communication'
            ]
        }
        
        return pages.get(role, ['Dashboard'])
    
    def can_access_page(self, page_name: str) -> bool:
        """Check if current user can access a specific page"""
        accessible_pages = self.get_accessible_pages()
        return page_name in accessible_pages
    
    def can_view_student_data(self, student_id: str) -> bool:
        """Check if current user can view specific student data"""
        role = self.get_user_role()
        user_id = self.get_user_id()
        
        if role == 'admin':
            return True
        
        if role == 'teacher':
            # Teachers can view students in their classes
            teacher_data = self.teacher_model.get_teacher_by_user_id(user_id)
            if teacher_data:
                student_data = self.student_model.find_by_id(student_id)
                if student_data and student_data.get('class_id') in teacher_data.get('class_ids', []):
                    return True
        
        if role == 'student':
            # Students can only view their own data
            student_data = self.student_model.get_student_by_user_id(user_id)
            if student_data and student_data['_id'] == student_id:
                return True
        
        if role == 'parent':
            # Parents can view their children's data
            student_data = self.student_model.find_by_id(student_id)
            if student_data and user_id in student_data.get('parent_ids', []):
                return True
        
        return False
    
    def can_modify_student_data(self, student_id: str) -> bool:
        """Check if current user can modify specific student data"""
        role = self.get_user_role()
        
        if role == 'admin':
            return True
        
        if role == 'teacher':
            # Teachers can modify attendance, grades, etc. for their students
            return self.can_view_student_data(student_id)
        
        return False
    
    def can_manage_class(self, class_id: str) -> bool:
        """Check if current user can manage a specific class"""
        role = self.get_user_role()
        user_id = self.get_user_id()
        
        if role == 'admin':
            return True
        
        if role == 'teacher':
            teacher_data = self.teacher_model.get_teacher_by_user_id(user_id)
            if teacher_data and class_id in teacher_data.get('class_ids', []):
                return True
        
        return False
    
    def get_user_classes(self) -> List[Dict[str, Any]]:
        """Get classes accessible to current user"""
        role = self.get_user_role()
        user_id = self.get_user_id()
        
        from src.database.models import ClassModel
        class_model = ClassModel()
        
        if role == 'admin':
            return class_model.get_active_classes()
        
        if role == 'teacher':
            teacher_data = self.teacher_model.get_teacher_by_user_id(user_id)
            if teacher_data:
                class_ids = teacher_data.get('class_ids', [])
                classes = []
                for class_id in class_ids:
                    class_data = class_model.find_by_id(class_id)
                    if class_data:
                        classes.append(class_data)
                return classes
        
        if role == 'student':
            student_data = self.student_model.get_student_by_user_id(user_id)
            if student_data:
                class_data = class_model.find_by_id(student_data.get('class_id'))
                return [class_data] if class_data else []
        
        return []
    
    def get_user_students(self) -> List[Dict[str, Any]]:
        """Get students accessible to current user"""
        role = self.get_user_role()
        user_id = self.get_user_id()
        
        if role == 'admin':
            return self.student_model.find_many({'status': 'active'})
        
        if role == 'teacher':
            teacher_data = self.teacher_model.get_teacher_by_user_id(user_id)
            if teacher_data:
                students = []
                for class_id in teacher_data.get('class_ids', []):
                    class_students = self.student_model.get_students_by_class(class_id)
                    students.extend(class_students)
                return students
        
        if role == 'student':
            student_data = self.student_model.get_student_by_user_id(user_id)
            return [student_data] if student_data else []
        
        if role == 'parent':
            # Get children of this parent
            children = self.student_model.find_many({
                'parent_ids': user_id,
                'status': 'active'
            })
            return children
        
        return []
    
    def require_role(self, required_roles: List[str]) -> bool:
        """Check if current user has one of the required roles"""
        current_role = self.get_user_role()
        
        if current_role not in required_roles:
            st.error(f"Access denied. Required role: {', '.join(required_roles)}")
            return False
        
        return True
    
    def require_authentication(self) -> bool:
        """Check if user is authenticated"""
        if not st.session_state.get('authenticated', False):
            st.error("Please log in to access this feature.")
            return False
        
        return True