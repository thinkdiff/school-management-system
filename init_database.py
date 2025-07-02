#!/usr/bin/env python3
"""
Database Initialization Script for School Management System
This script will create the database structure and populate it with sample data.
"""

import os
import sys
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.connection import DatabaseConnection
from src.database.models import (
    UserModel, StudentModel, TeacherModel, ClassModel,
    AttendanceModel, AssignmentModel, GradeModel, AnnouncementModel
)
from src.auth.authentication import Authentication

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database with sample data"""
    
    logger.info("🚀 Starting database initialization...")
    
    try:
        # Test database connection
        db_connection = DatabaseConnection()
        db = db_connection.get_database()
        
        # Test connection
        db.command('ping')
        logger.info("✅ Successfully connected to MongoDB Atlas!")
        
        # Initialize models
        user_model = UserModel()
        student_model = StudentModel()
        teacher_model = TeacherModel()
        class_model = ClassModel()
        attendance_model = AttendanceModel()
        assignment_model = AssignmentModel()
        grade_model = GradeModel()
        announcement_model = AnnouncementModel()
        auth = Authentication()
        
        logger.info("📊 Creating database collections and indexes...")
        
        # Create indexes for better performance
        create_indexes(db)
        
        # Clear existing data (for fresh start)
        clear_existing_data(db)
        
        # Create sample data
        logger.info("👥 Creating users...")
        user_ids = create_users(user_model, auth)
        
        logger.info("🏫 Creating classes...")
        class_ids = create_classes(class_model)
        
        logger.info("👨‍🏫 Creating teachers...")
        teacher_ids = create_teachers(teacher_model, user_ids, class_ids)
        
        logger.info("👨‍🎓 Creating students...")
        student_ids = create_students(student_model, user_ids, class_ids)
        
        logger.info("📝 Creating assignments...")
        assignment_ids = create_assignments(assignment_model, class_ids, teacher_ids)
        
        logger.info("🎯 Creating grades...")
        create_grades(grade_model, student_ids, assignment_ids, teacher_ids)
        
        logger.info("📅 Creating attendance records...")
        create_attendance(attendance_model, student_ids, class_ids)
        
        logger.info("📢 Creating announcements...")
        create_announcements(announcement_model, user_ids)
        
        logger.info("✨ Database initialization completed successfully!")
        print("\n" + "="*50)
        print("🎉 SCHOOL MANAGEMENT SYSTEM DATABASE READY!")
        print("="*50)
        print("\n📊 Database Statistics:")
        print(f"   Users: {user_model.count_documents({})}")
        print(f"   Students: {student_model.count_documents({})}")
        print(f"   Teachers: {teacher_model.count_documents({})}")
        print(f"   Classes: {class_model.count_documents({})}")
        print(f"   Assignments: {assignment_model.count_documents({})}")
        print(f"   Grades: {grade_model.count_documents({})}")
        print(f"   Attendance Records: {attendance_model.count_documents({})}")
        print(f"   Announcements: {announcement_model.count_documents({})}")
        print("\n🔑 Default Login Credentials:")
        print("   Admin: admin / admin123")
        print("   Teacher: teacher1 / teacher123")
        print("   Student: student1 / student123")
        print("   Parent: parent1 / parent123")
        print("\n🚀 Start the application with: streamlit run app.py")
        print("="*50)
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise

def create_indexes(db):
    """Create database indexes for better performance"""
    try:
        # Users collection indexes
        db.users.create_index([("username", 1)], unique=True)
        db.users.create_index([("email", 1)], unique=True)
        db.users.create_index([("role", 1)])
        
        # Students collection indexes
        db.students.create_index([("student_id", 1)], unique=True)
        db.students.create_index([("user_id", 1)])
        db.students.create_index([("class_id", 1)])
        
        # Teachers collection indexes
        db.teachers.create_index([("teacher_id", 1)], unique=True)
        db.teachers.create_index([("user_id", 1)])
        
        # Classes collection indexes
        db.classes.create_index([("class_code", 1)], unique=True)
        db.classes.create_index([("grade_level", 1)])
        
        # Attendance collection indexes
        db.attendance.create_index([("student_id", 1, "date", 1)])
        db.attendance.create_index([("class_id", 1, "date", 1)])
        
        # Assignments collection indexes
        db.assignments.create_index([("class_id", 1)])
        db.assignments.create_index([("due_date", 1)])
        
        # Grades collection indexes
        db.grades.create_index([("student_id", 1)])
        db.grades.create_index([("assignment_id", 1)])
        
        # Announcements collection indexes
        db.announcements.create_index([("target_audience", 1)])
        db.announcements.create_index([("created_at", -1)])
        
        logger.info("✅ Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"⚠️ Some indexes may already exist: {str(e)}")

def clear_existing_data(db):
    """Clear existing data for fresh start"""
    collections = [
        'users', 'students', 'teachers', 'classes',
        'attendance', 'assignments', 'grades', 'announcements'
    ]
    
    for collection_name in collections:
        try:
            result = db[collection_name].delete_many({})
            logger.info(f"   Cleared {result.deleted_count} documents from {collection_name}")
        except Exception as e:
            logger.warning(f"   Could not clear {collection_name}: {str(e)}")

def create_users(user_model, auth):
    """Create sample users"""
    user_ids = {}
    
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@school.com',
            'password': 'admin123',
            'role': 'admin',
            'full_name': 'System Administrator',
            'profile': {
                'phone': '+1234567890',
                'address': '123 School Admin St',
                'gender': 'other'
            }
        },
        {
            'username': 'teacher1',
            'email': 'teacher1@school.com',
            'password': 'teacher123',
            'role': 'teacher',
            'full_name': 'Sarah Johnson',
            'profile': {
                'phone': '+1234567891',
                'address': '456 Teacher Ave',
                'gender': 'female',
                'date_of_birth': '1985-03-15'
            }
        },
        {
            'username': 'teacher2',
            'email': 'teacher2@school.com',
            'password': 'teacher123',
            'role': 'teacher',
            'full_name': 'Michael Brown',
            'profile': {
                'phone': '+1234567892',
                'address': '789 Educator Blvd',
                'gender': 'male',
                'date_of_birth': '1980-07-22'
            }
        },
        {
            'username': 'teacher3',
            'email': 'teacher3@school.com',
            'password': 'teacher123',
            'role': 'teacher',
            'full_name': 'Emily Davis',
            'profile': {
                'phone': '+1234567893',
                'address': '321 Faculty Dr',
                'gender': 'female',
                'date_of_birth': '1988-11-08'
            }
        },
        {
            'username': 'student1',
            'email': 'student1@school.com',
            'password': 'student123',
            'role': 'student',
            'full_name': 'John Smith',
            'profile': {
                'phone': '+1234567894',
                'address': '111 Student Lane',
                'gender': 'male',
                'date_of_birth': '2008-05-12'
            }
        },
        {
            'username': 'student2',
            'email': 'student2@school.com',
            'password': 'student123',
            'role': 'student',
            'full_name': 'Emma Wilson',
            'profile': {
                'phone': '+1234567895',
                'address': '222 Pupil Place',
                'gender': 'female',
                'date_of_birth': '2008-09-25'
            }
        },
        {
            'username': 'student3',
            'email': 'student3@school.com',
            'password': 'student123',
            'role': 'student',
            'full_name': 'Alex Martinez',
            'profile': {
                'phone': '+1234567896',
                'address': '333 Learner Loop',
                'gender': 'male',
                'date_of_birth': '2007-12-03'
            }
        },
        {
            'username': 'student4',
            'email': 'student4@school.com',
            'password': 'student123',
            'role': 'student',
            'full_name': 'Sophie Chen',
            'profile': {
                'phone': '+1234567897',
                'address': '444 Scholar St',
                'gender': 'female',
                'date_of_birth': '2008-02-18'
            }
        },
        {
            'username': 'student5',
            'email': 'student5@school.com',
            'password': 'student123',
            'role': 'student',
            'full_name': 'David Thompson',
            'profile': {
                'phone': '+1234567898',
                'address': '555 Academic Ave',
                'gender': 'male',
                'date_of_birth': '2007-08-30'
            }
        },
        {
            'username': 'parent1',
            'email': 'parent1@school.com',
            'password': 'parent123',
            'role': 'parent',
            'full_name': 'Robert Smith',
            'profile': {
                'phone': '+1234567899',
                'address': '111 Student Lane',
                'gender': 'male',
                'date_of_birth': '1975-03-20'
            }
        },
        {
            'username': 'parent2',
            'email': 'parent2@school.com',
            'password': 'parent123',
            'role': 'parent',
            'full_name': 'Linda Wilson',
            'profile': {
                'phone': '+1234567800',
                'address': '222 Pupil Place',
                'gender': 'female',
                'date_of_birth': '1978-06-14'
            }
        }
    ]
    
    for user_data in users_data:
        try:
            # Hash password
            user_data['password'] = auth.hash_password(user_data['password'])
            
            # Create user
            user_id = user_model.create_user(user_data)
            user_ids[user_data['username']] = user_id
            logger.info(f"   Created user: {user_data['username']} ({user_data['role']})")
            
        except Exception as e:
            logger.error(f"   Failed to create user {user_data['username']}: {str(e)}")
    
    return user_ids

def create_classes(class_model):
    """Create sample classes"""
    class_ids = {}
    
    classes_data = [
        {
            'class_code': 'GR10A',
            'class_name': 'Grade 10 - Section A',
            'grade_level': 10,
            'academic_year': '2024-2025',
            'max_students': 30,
            'subjects': ['Mathematics', 'English', 'Science', 'History', 'Geography']
        },
        {
            'class_code': 'GR10B',
            'class_name': 'Grade 10 - Section B',
            'grade_level': 10,
            'academic_year': '2024-2025',
            'max_students': 30,
            'subjects': ['Mathematics', 'English', 'Science', 'History', 'Geography']
        },
        {
            'class_code': 'GR11A',
            'class_name': 'Grade 11 - Section A',
            'grade_level': 11,
            'academic_year': '2024-2025',
            'max_students': 25,
            'subjects': ['Advanced Mathematics', 'English Literature', 'Physics', 'Chemistry', 'Biology']
        },
        {
            'class_code': 'GR09A',
            'class_name': 'Grade 9 - Section A',
            'grade_level': 9,
            'academic_year': '2024-2025',
            'max_students': 32,
            'subjects': ['Basic Mathematics', 'English', 'General Science', 'Social Studies']
        }
    ]
    
    for class_data in classes_data:
        try:
            class_id = class_model.create_class(class_data)
            class_ids[class_data['class_code']] = class_id
            logger.info(f"   Created class: {class_data['class_name']}")
        except Exception as e:
            logger.error(f"   Failed to create class {class_data['class_code']}: {str(e)}")
    
    return class_ids

def create_teachers(teacher_model, user_ids, class_ids):
    """Create sample teachers"""
    teacher_ids = {}
    
    teachers_data = [
        {
            'teacher_id': 'TCH001',
            'user_id': user_ids.get('teacher1'),
            'subjects': ['Mathematics', 'Advanced Mathematics'],
            'hire_date': datetime(2020, 8, 15),
            'class_ids': [class_ids.get('GR10A'), class_ids.get('GR11A')],
            'department': 'Mathematics'
        },
        {
            'teacher_id': 'TCH002',
            'user_id': user_ids.get('teacher2'),
            'subjects': ['English', 'English Literature'],
            'hire_date': datetime(2018, 9, 1),
            'class_ids': [class_ids.get('GR10B'), class_ids.get('GR11A')],
            'department': 'English'
        },
        {
            'teacher_id': 'TCH003',
            'user_id': user_ids.get('teacher3'),
            'subjects': ['Science', 'Physics', 'Chemistry', 'Biology'],
            'hire_date': datetime(2019, 8, 20),
            'class_ids': [class_ids.get('GR09A'), class_ids.get('GR10A')],
            'department': 'Science'
        }
    ]
    
    for teacher_data in teachers_data:
        try:
            if teacher_data['user_id']:
                teacher_id = teacher_model.create_teacher(teacher_data)
                teacher_ids[teacher_data['teacher_id']] = teacher_id
                logger.info(f"   Created teacher: {teacher_data['teacher_id']}")
        except Exception as e:
            logger.error(f"   Failed to create teacher {teacher_data['teacher_id']}: {str(e)}")
    
    return teacher_ids

def create_students(student_model, user_ids, class_ids):
    """Create sample students"""
    student_ids = {}
    
    students_data = [
        {
            'student_id': 'STU001',
            'user_id': user_ids.get('student1'),
            'class_id': class_ids.get('GR10A'),
            'admission_date': datetime(2023, 8, 1),
            'parent_ids': [user_ids.get('parent1')],
            'subjects': ['Mathematics', 'English', 'Science', 'History', 'Geography']
        },
        {
            'student_id': 'STU002',
            'user_id': user_ids.get('student2'),
            'class_id': class_ids.get('GR10A'),
            'admission_date': datetime(2023, 8, 1),
            'parent_ids': [user_ids.get('parent2')],
            'subjects': ['Mathematics', 'English', 'Science', 'History', 'Geography']
        },
        {
            'student_id': 'STU003',
            'user_id': user_ids.get('student3'),
            'class_id': class_ids.get('GR11A'),
            'admission_date': datetime(2022, 8, 1),
            'parent_ids': [],
            'subjects': ['Advanced Mathematics', 'English Literature', 'Physics', 'Chemistry', 'Biology']
        },
        {
            'student_id': 'STU004',
            'user_id': user_ids.get('student4'),
            'class_id': class_ids.get('GR10B'),
            'admission_date': datetime(2023, 8, 1),
            'parent_ids': [],
            'subjects': ['Mathematics', 'English', 'Science', 'History', 'Geography']
        },
        {
            'student_id': 'STU005',
            'user_id': user_ids.get('student5'),
            'class_id': class_ids.get('GR11A'),
            'admission_date': datetime(2022, 8, 1),
            'parent_ids': [],
            'subjects': ['Advanced Mathematics', 'English Literature', 'Physics', 'Chemistry', 'Biology']
        }
    ]
    
    for student_data in students_data:
        try:
            if student_data['user_id'] and student_data['class_id']:
                student_id = student_model.create_student(student_data)
                student_ids[student_data['student_id']] = student_id
                logger.info(f"   Created student: {student_data['student_id']}")
        except Exception as e:
            logger.error(f"   Failed to create student {student_data['student_id']}: {str(e)}")
    
    return student_ids

def create_assignments(assignment_model, class_ids, teacher_ids):
    """Create sample assignments"""
    assignment_ids = {}
    
    assignments_data = [
        {
            'title': 'Algebra Practice Test',
            'description': 'Complete all problems in Chapter 5. Show your work for full credit.',
            'class_id': class_ids.get('GR10A'),
            'subject': 'Mathematics',
            'due_date': datetime.now() + timedelta(days=7),
            'created_by': list(teacher_ids.values())[0] if teacher_ids else None,
            'max_points': 100,
            'instructions': 'Use proper mathematical notation and explain your reasoning.'
        },
        {
            'title': 'Science Lab Report',
            'description': 'Write a comprehensive lab report on the photosynthesis experiment.',
            'class_id': class_ids.get('GR10A'),
            'subject': 'Science',
            'due_date': datetime.now() + timedelta(days=10),
            'created_by': list(teacher_ids.values())[2] if len(teacher_ids) > 2 else None,
            'max_points': 75,
            'instructions': 'Include hypothesis, methodology, results, and conclusion sections.'
        },
        {
            'title': 'English Essay - Shakespeare',
            'description': 'Write a 1000-word essay analyzing themes in Romeo and Juliet.',
            'class_id': class_ids.get('GR10B'),
            'subject': 'English',
            'due_date': datetime.now() + timedelta(days=14),
            'created_by': list(teacher_ids.values())[1] if len(teacher_ids) > 1 else None,
            'max_points': 100,
            'instructions': 'Use MLA format and cite at least 3 sources.'
        },
        {
            'title': 'Physics Problem Set',
            'description': 'Solve problems related to motion and forces.',
            'class_id': class_ids.get('GR11A'),
            'subject': 'Physics',
            'due_date': datetime.now() + timedelta(days=5),
            'created_by': list(teacher_ids.values())[2] if len(teacher_ids) > 2 else None,
            'max_points': 80,
            'instructions': 'Show all calculations and include diagrams where appropriate.'
        }
    ]
    
    for assignment_data in assignments_data:
        try:
            if assignment_data['class_id'] and assignment_data['created_by']:
                assignment_id = assignment_model.create_assignment(assignment_data)
                assignment_ids[assignment_data['title']] = assignment_id
                logger.info(f"   Created assignment: {assignment_data['title']}")
        except Exception as e:
            logger.error(f"   Failed to create assignment {assignment_data['title']}: {str(e)}")
    
    return assignment_ids

def create_grades(grade_model, student_ids, assignment_ids, teacher_ids):
    """Create sample grades"""
    import random
    
    for student_id in student_ids.values():
        for assignment_id in assignment_ids.values():
            try:
                # Generate random grade (70-100 range for realistic data)
                points_earned = random.randint(70, 100)
                max_points = 100
                percentage = (points_earned / max_points) * 100
                
                grade_data = {
                    'student_id': student_id,
                    'assignment_id': assignment_id,
                    'points_earned': points_earned,
                    'max_points': max_points,
                    'percentage': percentage,
                    'graded_by': list(teacher_ids.values())[0] if teacher_ids else None,
                    'comments': f'Good work! Score: {points_earned}/{max_points}',
                    'graded_date': datetime.now() - timedelta(days=random.randint(1, 30))
                }
                
                if grade_data['graded_by']:
                    grade_model.record_grade(grade_data)
                    
            except Exception as e:
                logger.warning(f"   Could not create grade: {str(e)}")
    
    logger.info(f"   Created sample grades for students")

def create_attendance(attendance_model, student_ids, class_ids):
    """Create sample attendance records"""
    import random
    
    # Create attendance for the last 30 days
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).date()
        
        for student_id in student_ids.values():
            try:
                # 90% chance of being present (realistic attendance)
                status = 'present' if random.random() > 0.1 else random.choice(['absent', 'late'])
                
                attendance_data = {
                    'student_id': student_id,
                    'class_id': list(class_ids.values())[0] if class_ids else None,
                    'date': date,
                    'status': status,
                    'remarks': 'Regular attendance' if status == 'present' else 'Family emergency' if status == 'absent' else 'Traffic delay'
                }
                
                if attendance_data['class_id']:
                    attendance_model.mark_attendance(attendance_data)
                    
            except Exception as e:
                logger.warning(f"   Could not create attendance record: {str(e)}")
    
    logger.info(f"   Created attendance records for last 30 days")

def create_announcements(announcement_model, user_ids):
    """Create sample announcements"""
    announcements_data = [
        {
            'title': 'Welcome to New Academic Year 2024-2025',
            'content': 'We are excited to welcome all students back for the new academic year. Please check your class schedules and contact your teachers if you have any questions.',
            'created_by': user_ids.get('admin'),
            'target_audience': 'all',
            'priority': 'high'
        },
        {
            'title': 'Parent-Teacher Conference',
            'content': 'Parent-teacher conferences will be held next week. Please schedule your appointments through the school office.',
            'created_by': user_ids.get('admin'),
            'target_audience': 'parent',
            'priority': 'normal'
        },
        {
            'title': 'Science Fair Registration Open',
            'content': 'Registration for the annual science fair is now open. Students interested in participating should submit their project proposals by the end of this month.',
            'created_by': user_ids.get('teacher3'),
            'target_audience': 'student',
            'priority': 'normal'
        },
        {
            'title': 'System Maintenance Notice',
            'content': 'The school management system will undergo maintenance this weekend. The system may be temporarily unavailable on Saturday from 2 AM to 6 AM.',
            'created_by': user_ids.get('admin'),
            'target_audience': 'all',
            'priority': 'low'
        }
    ]
    
    for announcement_data in announcements_data:
        try:
            if announcement_data['created_by']:
                announcement_model.create_announcement(announcement_data)
                logger.info(f"   Created announcement: {announcement_data['title']}")
        except Exception as e:
            logger.error(f"   Failed to create announcement {announcement_data['title']}: {str(e)}")

if __name__ == "__main__":
    try:
        print("🏫 School Management System - Database Initialization")
        print("=" * 55)
        initialize_database()
    except KeyboardInterrupt:
        print("\n⚠️ Initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Initialization failed: {str(e)}")
        sys.exit(1)