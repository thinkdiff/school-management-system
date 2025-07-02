import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
import logging
from src.config.settings import Settings

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for sending notifications and communications"""
    
    def __init__(self):
        self.settings = Settings()
        self.config = self.settings.get_email_config()
    
    def send_email(self, 
                   to_addresses: List[str], 
                   subject: str, 
                   body: str, 
                   html_body: Optional[str] = None,
                   attachments: Optional[List[Dict[str, Any]]] = None) -> bool:
        """Send email to recipients"""
        
        if not self.config['smtp_server'] or not self.config['username']:
            logger.warning("Email configuration not complete. Skipping email send.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['username']
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject
            
            # Add text body
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML body if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    self._add_attachment(msg, attachment)
            
            # Connect to server and send email
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['username'], self.config['password'])
            
            text = msg.as_string()
            server.sendmail(self.config['username'], to_addresses, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {', '.join(to_addresses)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, attachment: Dict[str, Any]):
        """Add attachment to email message"""
        try:
            filename = attachment.get('filename', 'attachment')
            content = attachment.get('content', b'')
            content_type = attachment.get('content_type', 'application/octet-stream')
            
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(content)
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            msg.attach(part)
            
        except Exception as e:
            logger.error(f"Failed to add attachment {attachment.get('filename', 'unknown')}: {str(e)}")
    
    def send_welcome_email(self, user_data: Dict[str, Any], temporary_password: str) -> bool:
        """Send welcome email to new user"""
        subject = "Welcome to School Management System"
        
        body = f"""
Dear {user_data.get('full_name', 'User')},

Welcome to the School Management System!

Your account has been created with the following details:
Username: {user_data.get('username')}
Role: {user_data.get('role', '').title()}
Temporary Password: {temporary_password}

Please log in and change your password immediately for security.

If you have any questions, please contact the system administrator.

Best regards,
School Management System Team
        """
        
        html_body = f"""
<html>
<body>
    <h2>Welcome to School Management System!</h2>
    <p>Dear {user_data.get('full_name', 'User')},</p>
    
    <p>Your account has been created successfully.</p>
    
    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <h3>Account Details:</h3>
        <p><strong>Username:</strong> {user_data.get('username')}</p>
        <p><strong>Role:</strong> {user_data.get('role', '').title()}</p>
        <p><strong>Temporary Password:</strong> <code>{temporary_password}</code></p>
    </div>
    
    <p><strong>Important:</strong> Please log in and change your password immediately for security.</p>
    
    <p>If you have any questions, please contact the system administrator.</p>
    
    <p>Best regards,<br>School Management System Team</p>
</body>
</html>
        """
        
        return self.send_email([user_data.get('email')], subject, body, html_body)
    
    def send_password_reset_email(self, user_data: Dict[str, Any], new_password: str) -> bool:
        """Send password reset email"""
        subject = "Password Reset - School Management System"
        
        body = f"""
Dear {user_data.get('full_name', 'User')},

Your password has been reset as requested.

New Temporary Password: {new_password}

Please log in and change your password immediately.

If you did not request this password reset, please contact the system administrator immediately.

Best regards,
School Management System Team
        """
        
        return self.send_email([user_data.get('email')], subject, body)
    
    def send_attendance_alert(self, student_data: Dict[str, Any], parent_emails: List[str], attendance_info: Dict[str, Any]) -> bool:
        """Send attendance alert to parents"""
        subject = f"Attendance Alert - {student_data.get('full_name', 'Student')}"
        
        body = f"""
Dear Parent/Guardian,

This is to inform you about your child's attendance:

Student Name: {student_data.get('full_name', 'Unknown')}
Date: {attendance_info.get('date', 'Unknown')}
Status: {attendance_info.get('status', 'Unknown').title()}

Attendance Rate (Last 30 days): {attendance_info.get('attendance_rate', 0)}%

If you have any concerns, please contact the school.

Best regards,
School Management System
        """
        
        return self.send_email(parent_emails, subject, body)
    
    def send_grade_notification(self, student_data: Dict[str, Any], parent_emails: List[str], grade_info: Dict[str, Any]) -> bool:
        """Send grade notification to parents"""
        subject = f"New Grade Posted - {student_data.get('full_name', 'Student')}"
        
        body = f"""
Dear Parent/Guardian,

A new grade has been posted for your child:

Student Name: {student_data.get('full_name', 'Unknown')}
Assignment: {grade_info.get('assignment_title', 'Unknown')}
Subject: {grade_info.get('subject', 'Unknown')}
Grade: {grade_info.get('points_earned', 0)}/{grade_info.get('max_points', 0)} ({grade_info.get('percentage', 0)}%)

You can view detailed progress reports by logging into the parent portal.

Best regards,
School Management System
        """
        
        return self.send_email(parent_emails, subject, body)
    
    def send_assignment_reminder(self, student_emails: List[str], assignment_info: Dict[str, Any]) -> bool:
        """Send assignment reminder to students"""
        subject = f"Assignment Reminder - {assignment_info.get('title', 'Assignment')}"
        
        days_left = assignment_info.get('days_until_due', 0)
        
        body = f"""
Dear Student,

This is a reminder about your upcoming assignment:

Title: {assignment_info.get('title', 'Unknown')}
Subject: {assignment_info.get('subject', 'Unknown')}
Due Date: {assignment_info.get('due_date', 'Unknown')}
Days Remaining: {days_left}

Description:
{assignment_info.get('description', 'No description available')}

Please ensure you submit your assignment on time.

Best regards,
Your Teacher
        """
        
        return self.send_email(student_emails, subject, body)
    
    def send_announcement_email(self, recipient_emails: List[str], announcement: Dict[str, Any]) -> bool:
        """Send announcement via email"""
        subject = f"Announcement: {announcement.get('title', 'School Announcement')}"
        
        body = f"""
School Announcement

Title: {announcement.get('title', 'Unknown')}
Priority: {announcement.get('priority', 'Normal').title()}
Date: {announcement.get('created_at', 'Unknown')}

Message:
{announcement.get('content', 'No content available')}

Best regards,
School Administration
        """
        
        return self.send_email(recipient_emails, subject, body)