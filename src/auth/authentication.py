import bcrypt
import streamlit as st
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from src.database.models import UserModel

logger = logging.getLogger(__name__)

class Authentication:
    """Authentication and authorization management"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.max_login_attempts = 3
        self.lockout_duration = 15  # minutes
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password"""
        try:
            # Check for account lockout
            if self._is_account_locked(username):
                logger.warning(f"Account locked for user: {username}")
                return None
            
            # Find user by username
            user = self.user_model.find_one({'username': username, 'is_active': True})
            
            if not user:
                self._record_failed_attempt(username)
                logger.warning(f"User not found: {username}")
                return None
            
            # Verify password
            if self.verify_password(password, user['password']):
                # Reset failed attempts on successful login
                self._reset_failed_attempts(username)
                
                # Update last login
                self.user_model.update_by_id(user['_id'], {
                    'last_login': datetime.utcnow()
                })
                
                # Remove sensitive data
                user.pop('password', None)
                
                logger.info(f"Successful login for user: {username}")
                return user
            else:
                self._record_failed_attempt(username)
                logger.warning(f"Invalid password for user: {username}")
                return None
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Create a new user account"""
        try:
            # Hash the password
            if 'password' in user_data:
                user_data['password'] = self.hash_password(user_data['password'])
            
            # Create user
            user_id = self.user_model.create_user(user_data)
            logger.info(f"Created new user: {user_data['username']}")
            return True
            
        except Exception as e:
            logger.error(f"User creation error: {str(e)}")
            return False
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Authenticate with old password
            user = self.authenticate_user(username, old_password)
            if not user:
                return False
            
            # Hash new password
            new_password_hash = self.hash_password(new_password)
            
            # Update password
            success = self.user_model.update_one(
                {'username': username},
                {'password': new_password_hash}
            )
            
            if success:
                logger.info(f"Password changed for user: {username}")
            
            return success
                
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return False
    
    def reset_password(self, username: str, new_password: str) -> bool:
        """Reset user password (admin function)"""
        try:
            # Hash new password
            new_password_hash = self.hash_password(new_password)
            
            # Update password
            success = self.user_model.update_one(
                {'username': username},
                {'password': new_password_hash}
            )
            
            if success:
                logger.info(f"Password reset for user: {username}")
            
            return success
                
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return False
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed attempts"""
        if 'failed_attempts' not in st.session_state:
            st.session_state.failed_attempts = {}
        
        user_attempts = st.session_state.failed_attempts.get(username, {})
        
        if user_attempts.get('count', 0) >= self.max_login_attempts:
            lockout_time = user_attempts.get('lockout_time')
            if lockout_time and datetime.now() < lockout_time:
                return True
            else:
                # Reset attempts after lockout period
                self._reset_failed_attempts(username)
        
        return False
    
    def _record_failed_attempt(self, username: str):
        """Record a failed login attempt"""
        if 'failed_attempts' not in st.session_state:
            st.session_state.failed_attempts = {}
        
        if username not in st.session_state.failed_attempts:
            st.session_state.failed_attempts[username] = {'count': 0}
        
        st.session_state.failed_attempts[username]['count'] += 1
        
        if st.session_state.failed_attempts[username]['count'] >= self.max_login_attempts:
            st.session_state.failed_attempts[username]['lockout_time'] = \
                datetime.now() + timedelta(minutes=self.lockout_duration)
    
    def _reset_failed_attempts(self, username: str):
        """Reset failed login attempts for a user"""
        if 'failed_attempts' in st.session_state and username in st.session_state.failed_attempts:
            del st.session_state.failed_attempts[username]
    
    def logout_user(self):
        """Logout current user"""
        try:
            if 'user_data' in st.session_state and st.session_state.user_data:
                username = st.session_state.user_data.get('username', 'Unknown')
                logger.info(f"User logged out: {username}")
            
            # Clear session state
            st.session_state.authenticated = False
            st.session_state.user_data = None
            
            # Clear other session data
            keys_to_clear = ['current_page', 'selected_class', 'selected_student']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
                    
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
    
    def get_user_permissions(self, role: str) -> Dict[str, bool]:
        """Get user permissions based on role"""
        permissions = {
            'admin': {
                'manage_users': True,
                'manage_classes': True,
                'manage_subjects': True,
                'view_reports': True,
                'manage_system': True,
                'view_all_students': True,
                'manage_announcements': True
            },
            'teacher': {
                'manage_users': False,
                'manage_classes': False,
                'manage_subjects': False,
                'view_reports': True,
                'manage_system': False,
                'view_all_students': False,
                'manage_attendance': True,
                'manage_assignments': True,
                'manage_grades': True,
                'view_class_students': True
            },
            'student': {
                'manage_users': False,
                'manage_classes': False,
                'manage_subjects': False,
                'view_reports': False,
                'manage_system': False,
                'view_own_data': True,
                'submit_assignments': True,
                'view_grades': True,
                'view_attendance': True
            },
            'parent': {
                'manage_users': False,
                'manage_classes': False,
                'manage_subjects': False,
                'view_reports': False,
                'manage_system': False,
                'view_child_data': True,
                'view_child_grades': True,
                'view_child_attendance': True,
                'communicate_teachers': True
            }
        }
        
        return permissions.get(role, {})
    
    def has_permission(self, user_role: str, permission: str) -> bool:
        """Check if user has specific permission"""
        permissions = self.get_user_permissions(user_role)
        return permissions.get(permission, False)
    
    def require_permission(self, permission: str) -> bool:
        """Decorator to require specific permission"""
        if not st.session_state.get('authenticated', False):
            st.error("Please log in to access this feature.")
            return False
        
        user_data = st.session_state.get('user_data', {})
        user_role = user_data.get('role', '')
        
        if not self.has_permission(user_role, permission):
            st.error("You don't have permission to access this feature.")
            return False
        
        return True