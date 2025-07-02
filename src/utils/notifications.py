from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from src.database.models import (
    UserModel, StudentModel, TeacherModel, ClassModel,
    AttendanceModel, GradeModel, AssignmentModel
)
from src.utils.email_service import EmailService

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for managing and sending notifications"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.user_model = UserModel()
        self.student_model = StudentModel()
        self.teacher_model = TeacherModel()
    
    def send_low_attendance_alerts(self, threshold: float = 75.0) -> int:
        """Send alerts for students with low attendance"""
        attendance_model = AttendanceModel()
        alerts_sent = 0
        
        try:
            # Get all active students
            students = self.student_model.find_many({'status': 'active'})
            
            for student in students:
                # Calculate attendance for last 30 days
                start_date = datetime.now() - timedelta(days=30)
                attendance_records = attendance_model.get_student_attendance(
                    student['_id'], start_date
                )
                
                if attendance_records:
                    present_count = len([r for r in attendance_records if r.get('status') == 'present'])
                    attendance_rate = (present_count / len(attendance_records)) * 100
                    
                    if attendance_rate < threshold:
                        # Get parent emails
                        parent_emails = self._get_parent_emails(student.get('parent_ids', []))
                        
                        if parent_emails:
                            attendance_info = {
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'status': 'low_attendance',
                                'attendance_rate': round(attendance_rate, 1)
                            }
                            
                            success = self.email_service.send_attendance_alert(
                                student, parent_emails, attendance_info
                            )
                            
                            if success:
                                alerts_sent += 1
                                logger.info(f"Low attendance alert sent for student {student.get('student_id')}")
            
            return alerts_sent
            
        except Exception as e:
            logger.error(f"Error sending low attendance alerts: {str(e)}")
            return 0
    
    def send_assignment_reminders(self, days_before: int = 3) -> int:
        """Send assignment due date reminders"""
        assignment_model = AssignmentModel()
        reminders_sent = 0
        
        try:
            # Get assignments due in the next few days
            start_date = datetime.now()
            end_date = start_date + timedelta(days=days_before)
            
            # Find assignments due in this period
            assignments = assignment_model.find_many({
                'is_active': True,
                'due_date': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            })
            
            for assignment in assignments:
                # Get students in the class
                class_students = self.student_model.get_students_by_class(
                    assignment['class_id']
                )
                
                if class_students:
                    # Get student emails
                    student_emails = []
                    for student in class_students:
                        user_data = self.user_model.find_by_id(student['user_id'])
                        if user_data and user_data.get('email'):
                            student_emails.append(user_data['email'])
                    
                    if student_emails:
                        days_left = (assignment['due_date'] - datetime.now()).days
                        assignment_info = {
                            'title': assignment['title'],
                            'subject': assignment.get('subject', 'Unknown'),
                            'due_date': assignment['due_date'].strftime('%Y-%m-%d'),
                            'description': assignment.get('description', ''),
                            'days_until_due': max(0, days_left)
                        }
                        
                        success = self.email_service.send_assignment_reminder(
                            student_emails, assignment_info
                        )
                        
                        if success:
                            reminders_sent += 1
                            logger.info(f"Assignment reminder sent for {assignment['title']}")
            
            return reminders_sent
            
        except Exception as e:
            logger.error(f"Error sending assignment reminders: {str(e)}")
            return 0
    
    def send_grade_notifications(self, grade_id: str) -> bool:
        """Send notification when a new grade is posted"""
        try:
            grade_model = GradeModel()
            assignment_model = AssignmentModel()
            
            # Get grade information
            grade = grade_model.find_by_id(grade_id)
            if not grade:
                return False
            
            # Get student information
            student = self.student_model.find_by_id(grade['student_id'])
            if not student:
                return False
            
            # Get assignment information
            assignment = assignment_model.find_by_id(grade['assignment_id'])
            if not assignment:
                return False
            
            # Get parent emails
            parent_emails = self._get_parent_emails(student.get('parent_ids', []))
            
            if parent_emails:
                grade_info = {
                    'assignment_title': assignment['title'],
                    'subject': assignment.get('subject', 'Unknown'),
                    'points_earned': grade.get('points_earned', 0),
                    'max_points': grade.get('max_points', 0),
                    'percentage': grade.get('percentage', 0)
                }
                
                success = self.email_service.send_grade_notification(
                    student, parent_emails, grade_info
                )
                
                if success:
                    logger.info(f"Grade notification sent for student {student.get('student_id')}")
                
                return success
            
            return True  # No parents to notify, but not an error
            
        except Exception as e:
            logger.error(f"Error sending grade notification: {str(e)}")
            return False
    
    def send_welcome_notifications(self, user_id: str, temporary_password: str) -> bool:
        """Send welcome notification to new user"""
        try:
            user_data = self.user_model.find_by_id(user_id)
            if not user_data:
                return False
            
            success = self.email_service.send_welcome_email(user_data, temporary_password)
            
            if success:
                logger.info(f"Welcome notification sent to {user_data.get('email')}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending welcome notification: {str(e)}")
            return False
    
    def send_announcement_notifications(self, announcement: Dict[str, Any]) -> int:
        """Send announcement notifications based on target audience"""
        notifications_sent = 0
        
        try:
            target_audience = announcement.get('target_audience', 'all')
            
            # Get recipient emails based on target audience
            recipient_emails = []
            
            if target_audience == 'all':
                # Send to all active users
                all_users = self.user_model.find_many({'is_active': True})
                recipient_emails = [user['email'] for user in all_users if user.get('email')]
            
            elif target_audience in ['admin', 'teacher', 'student', 'parent']:
                # Send to specific role
                role_users = self.user_model.get_users_by_role(target_audience)
                recipient_emails = [user['email'] for user in role_users if user.get('email')]
            
            elif target_audience == 'parents':
                # Send to all parents
                parent_users = self.user_model.get_users_by_role('parent')
                recipient_emails = [user['email'] for user in parent_users if user.get('email')]
            
            # Send emails in batches to avoid overwhelming the email server
            batch_size = 50
            for i in range(0, len(recipient_emails), batch_size):
                batch_emails = recipient_emails[i:i + batch_size]
                
                success = self.email_service.send_announcement_email(
                    batch_emails, announcement
                )
                
                if success:
                    notifications_sent += len(batch_emails)
            
            logger.info(f"Announcement notifications sent to {notifications_sent} recipients")
            return notifications_sent
            
        except Exception as e:
            logger.error(f"Error sending announcement notifications: {str(e)}")
            return 0
    
    def _get_parent_emails(self, parent_ids: List[str]) -> List[str]:
        """Get email addresses for parent user IDs"""
        parent_emails = []
        
        for parent_id in parent_ids:
            parent_user = self.user_model.find_by_id(parent_id)
            if parent_user and parent_user.get('email'):
                parent_emails.append(parent_user['email'])
        
        return parent_emails
    
    def send_daily_digest(self) -> int:
        """Send daily digest to administrators"""
        try:
            # Get admin users
            admin_users = self.user_model.get_users_by_role('admin')
            admin_emails = [user['email'] for user in admin_users if user.get('email')]
            
            if not admin_emails:
                return 0
            
            # Collect daily statistics
            today = datetime.now().date()
            
            # Today's attendance
            attendance_model = AttendanceModel()
            today_attendance = attendance_model.find_many({'date': today})
            present_count = len([a for a in today_attendance if a.get('status') == 'present'])
            
            # New registrations today
            new_users_today = self.user_model.find_many({
                'created_at': {
                    '$gte': datetime.combine(today, datetime.min.time()),
                    '$lt': datetime.combine(today + timedelta(days=1), datetime.min.time())
                }
            })
            
            # Create digest content
            subject = f"Daily Digest - {today.strftime('%B %d, %Y')}"
            
            body = f"""
Daily School Management System Digest
Date: {today.strftime('%B %d, %Y')}

Today's Statistics:
- Students Present: {present_count}
- New User Registrations: {len(new_users_today)}
- Total Active Students: {self.student_model.count_documents({'status': 'active'})}
- Total Active Teachers: {self.teacher_model.count_documents({'status': 'active'})}

New Users Today:
            """
            
            for user in new_users_today:
                body += f"- {user.get('full_name', 'Unknown')} ({user.get('role', 'Unknown')})
"
            
            body += """

This is an automated daily digest. Please contact the system administrator if you have any questions.

Best regards,
School Management System
            """
            
            success = self.email_service.send_email(admin_emails, subject, body)
            
            if success:
                logger.info("Daily digest sent to administrators")
                return len(admin_emails)
            
            return 0
            
        except Exception as e:
            logger.error(f"Error sending daily digest: {str(e)}")
            return 0