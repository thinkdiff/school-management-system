from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format datetime object to string"""
    if not date_obj:
        return ""
    return date_obj.strftime(format_str)

def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None

def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    if not birth_date:
        return 0
    
    today = datetime.now()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return max(0, age)

def get_academic_year(date_obj: datetime = None) -> str:
    """Get academic year string (e.g., '2025-2026')"""
    if not date_obj:
        date_obj = datetime.now()
    
    # Academic year typically starts in August/September
    if date_obj.month >= 8:  # August or later
        start_year = date_obj.year
        end_year = date_obj.year + 1
    else:  # Before August
        start_year = date_obj.year - 1
        end_year = date_obj.year
    
    return f"{start_year}-{end_year}"

def calculate_grade_percentage(points_earned: float, max_points: float) -> float:
    """Calculate percentage from points"""
    if max_points <= 0:
        return 0.0
    return round((points_earned / max_points) * 100, 2)

def get_grade_color(percentage: float) -> str:
    """Get color code for grade display"""
    if percentage >= 90:
        return "#4CAF50"  # Green
    elif percentage >= 80:
        return "#8BC34A"  # Light Green
    elif percentage >= 70:
        return "#FFC107"  # Amber
    elif percentage >= 60:
        return "#FF9800"  # Orange
    else:
        return "#F44336"  # Red

def calculate_attendance_percentage(present_days: int, total_days: int) -> float:
    """Calculate attendance percentage"""
    if total_days <= 0:
        return 0.0
    return round((present_days / total_days) * 100, 2)

def generate_student_id(class_code: str, sequence_number: int) -> str:
    """Generate student ID"""
    current_year = datetime.now().year
    return f"{class_code}{current_year}{sequence_number:03d}"

def generate_teacher_id(department: str, sequence_number: int) -> str:
    """Generate teacher ID"""
    current_year = datetime.now().year
    dept_code = department[:3].upper() if department else "TCH"
    return f"{dept_code}{current_year}{sequence_number:03d}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    import re
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple consecutive underscores
    filename = re.sub(r'_{2,}', '_', filename)
    # Trim underscores from start and end
    filename = filename.strip('_')
    return filename

def validate_email(email: str) -> bool:
    """Validate email address format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's 10-15 digits
    return 10 <= len(digits_only) <= 15

def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data (e.g., phone numbers, IDs)"""
    if not data or len(data) <= visible_chars:
        return data
    
    visible_part = data[:visible_chars]
    masked_part = '*' * (len(data) - visible_chars)
    return visible_part + masked_part

def paginate_data(data: List[Dict[str, Any]], page: int, per_page: int) -> Dict[str, Any]:
    """Paginate data for display"""
    total_items = len(data)
    total_pages = (total_items + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_data = data[start_idx:end_idx]
    
    return {
        'data': paginated_data,
        'current_page': page,
        'total_pages': total_pages,
        'total_items': total_items,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None
    }

def export_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """Export data to CSV format"""
    try:
        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False)
        return csv_data
    except Exception as e:
        logger.error(f"Error exporting to CSV: {str(e)}")
        return ""

def import_from_csv(csv_data: str) -> List[Dict[str, Any]]:
    """Import data from CSV format"""
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Error importing from CSV: {str(e)}")
        return []

def generate_report_data(data: List[Dict[str, Any]], group_by: str) -> Dict[str, Any]:
    """Generate report data with grouping and statistics"""
    try:
        df = pd.DataFrame(data)
        
        if group_by not in df.columns:
            return {'error': f'Column {group_by} not found'}
        
        # Group by specified column
        grouped = df.groupby(group_by).size().reset_index(name='count')
        
        # Calculate statistics
        stats = {
            'total_records': len(data),
            'unique_groups': len(grouped),
            'groups': grouped.to_dict('records')
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error generating report data: {str(e)}")
        return {'error': str(e)}

def calculate_gpa(grades: List[Dict[str, Any]]) -> float:
    """Calculate GPA from grades"""
    if not grades:
        return 0.0
    
    grade_points = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }
    
    total_points = 0.0
    total_credits = 0
    
    for grade in grades:
        percentage = grade.get('percentage', 0)
        credits = grade.get('credits', 1)  # Default 1 credit
        
        # Convert percentage to letter grade
        if percentage >= 97:
            letter_grade = 'A+'
        elif percentage >= 93:
            letter_grade = 'A'
        elif percentage >= 90:
            letter_grade = 'A-'
        elif percentage >= 87:
            letter_grade = 'B+'
        elif percentage >= 83:
            letter_grade = 'B'
        elif percentage >= 80:
            letter_grade = 'B-'
        elif percentage >= 77:
            letter_grade = 'C+'
        elif percentage >= 73:
            letter_grade = 'C'
        elif percentage >= 70:
            letter_grade = 'C-'
        elif percentage >= 67:
            letter_grade = 'D+'
        elif percentage >= 63:
            letter_grade = 'D'
        elif percentage >= 60:
            letter_grade = 'D-'
        else:
            letter_grade = 'F'
        
        points = grade_points.get(letter_grade, 0.0)
        total_points += points * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return round(total_points / total_credits, 2)

def get_semester_from_date(date_obj: datetime = None) -> str:
    """Get current semester based on date"""
    if not date_obj:
        date_obj = datetime.now()
    
    month = date_obj.month
    
    if 1 <= month <= 5:  # January to May
        return "Spring"
    elif 6 <= month <= 7:  # June to July
        return "Summer"
    else:  # August to December
        return "Fall"

def time_ago(date_obj: datetime) -> str:
    """Get human-readable time difference"""
    if not date_obj:
        return "Unknown"
    
    now = datetime.now()
    
    # Handle timezone-naive datetime objects
    if date_obj.tzinfo is None:
        date_obj = date_obj.replace(tzinfo=None)
    if now.tzinfo is None:
        now = now.replace(tzinfo=None)
    
    diff = now - date_obj
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"