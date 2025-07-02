import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.auth.authorization import Authorization
from src.database.models import (
    UserModel, StudentModel, TeacherModel, ClassModel,
    AttendanceModel, AssignmentModel, GradeModel, AnnouncementModel
)
import logging

logger = logging.getLogger(__name__)

def render_dashboard():
    """Render the main dashboard based on user role"""
    
    auth = Authorization()
    role = auth.get_user_role()
    
    # Get current page from session state
    current_page = st.session_state.get('current_page', 'Dashboard')
    
    # Route to appropriate page renderer
    if current_page == 'Dashboard':
        if role == 'admin':
            render_admin_dashboard()
        elif role == 'teacher':
            render_teacher_dashboard()
        elif role == 'student':
            render_student_dashboard()
        elif role == 'parent':
            render_parent_dashboard()
    elif current_page == 'User Management':
        render_user_management()
    elif current_page == 'Class Management':
        render_class_management()
    elif current_page == 'Student Management':
        render_student_management()
    elif current_page == 'Teacher Management':
        render_teacher_management()
    elif current_page == 'My Classes':
        render_my_classes()
    elif current_page == 'Attendance':
        render_attendance()
    elif current_page == 'Assignments':
        render_assignments()
    elif current_page == 'Grades':
        render_grades()
    elif current_page == 'Students':
        render_students()
    elif current_page == 'Reports':
        render_reports()
    elif current_page == 'Announcements':
        render_announcements()
    elif current_page == 'System Settings':
        render_system_settings()
    elif current_page == 'Child Progress':
        render_child_progress()
    elif current_page == 'Communication':
        render_communication()
    else:
        st.error(f"Page '{current_page}' not found.")

def render_admin_dashboard():
    """Render admin dashboard with system overview"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Admin Dashboard</h1>
        <p>System Overview and Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize models
    user_model = UserModel()
    student_model = StudentModel()
    teacher_model = TeacherModel()
    class_model = ClassModel()
    announcement_model = AnnouncementModel()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = student_model.count_documents({'status': 'active'})
        st.metric(
            label="👨‍🎓 Total Students",
            value=total_students,
            delta=f"+{total_students // 10} this month"
        )
    
    with col2:
        total_teachers = teacher_model.count_documents({'status': 'active'})
        st.metric(
            label="👩‍🏫 Total Teachers",
            value=total_teachers,
            delta=f"+{total_teachers // 20} this month"
        )
    
    with col3:
        total_classes = class_model.count_documents({'is_active': True})
        st.metric(
            label="🏢 Active Classes",
            value=total_classes,
            delta="+2 this term"
        )
    
    with col4:
        total_users = user_model.count_documents({'is_active': True})
        st.metric(
            label="👥 Total Users",
            value=total_users,
            delta=f"+{total_users // 50} this week"
        )
    
    st.markdown("---")
    
    # Charts and analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 User Distribution")
        
        # Get user counts by role
        pipeline = [
            {'$match': {'is_active': True}},
            {'$group': {'_id': '$role', 'count': {'$sum': 1}}}
        ]
        role_data = user_model.aggregate(pipeline)
        
        if role_data:
            df_roles = pd.DataFrame(role_data)
            df_roles.columns = ['Role', 'Count']
            df_roles['Role'] = df_roles['Role'].str.title()
            
            fig = px.pie(
                df_roles, 
                values='Count', 
                names='Role',
                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Recent Activity")
        
        # Show recent announcements
        recent_announcements = announcement_model.find_many(
            {'is_active': True},
            limit=5,
            sort=[('created_at', -1)]
        )
        
        if recent_announcements:
            for announcement in recent_announcements:
                with st.container():
                    st.markdown(f"**{announcement['title']}**")
                    st.markdown(f"{announcement['content'][:100]}...")
                    st.markdown(f"*{announcement['created_at'].strftime('%Y-%m-%d %H:%M')}*")
                    st.markdown("---")
        else:
            st.info("No recent announcements")
    
    # Recent registrations
    st.subheader("🆕 Recent Registrations")
    
    recent_users = user_model.find_many(
        {'is_active': True},
        limit=10,
        sort=[('created_at', -1)]
    )
    
    if recent_users:
        df_users = pd.DataFrame(recent_users)
        df_users = df_users[['full_name', 'username', 'email', 'role', 'created_at']]
        df_users['created_at'] = pd.to_datetime(df_users['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        df_users.columns = ['Full Name', 'Username', 'Email', 'Role', 'Created At']
        
        st.dataframe(df_users, use_container_width=True)
    else:
        st.info("No recent user registrations")

def render_teacher_dashboard():
    """Render teacher dashboard"""
    
    st.markdown("""
    <div class="main-header">
        <h1>👩‍🏫 Teacher Dashboard</h1>
        <p>Manage your classes and students</p>
    </div>
    """, unsafe_allow_html=True)
    
    auth = Authorization()
    user_id = auth.get_user_id()
    
    # Get teacher's classes
    teacher_classes = auth.get_user_classes()
    teacher_students = auth.get_user_students()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏢 My Classes",
            value=len(teacher_classes)
        )
    
    with col2:
        st.metric(
            label="👨‍🎓 My Students",
            value=len(teacher_students)
        )
    
    with col3:
        # Count pending assignments
        assignment_model = AssignmentModel()
        class_ids = [cls['_id'] for cls in teacher_classes]
        pending_assignments = 0
        for class_id in class_ids:
            assignments = assignment_model.get_assignments_by_class(class_id)
            pending_assignments += len([a for a in assignments if a.get('due_date', datetime.now()) > datetime.now()])
        
        st.metric(
            label="📝 Active Assignments",
            value=pending_assignments
        )
    
    with col4:
        # Calculate attendance rate for today
        attendance_model = AttendanceModel()
        today = datetime.now().date()
        total_possible_attendance = len(teacher_students)
        
        if total_possible_attendance > 0:
            present_count = 0
            for student in teacher_students:
                attendance = attendance_model.find_one({
                    'student_id': student['_id'],
                    'date': today
                })
                if attendance and attendance.get('status') == 'present':
                    present_count += 1
            
            attendance_rate = (present_count / total_possible_attendance) * 100
        else:
            attendance_rate = 0
        
        st.metric(
            label="📅 Today's Attendance",
            value=f"{attendance_rate:.1f}%"
        )
    
    st.markdown("---")
    
    # Quick actions and recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚡ Quick Actions")
        
        if st.button("✓️ Mark Attendance", type="primary", use_container_width=True):
            st.session_state.current_page = 'Attendance'
            st.rerun()
        
        if st.button("📝 Create Assignment", use_container_width=True):
            st.session_state.show_add_assignment_modal = True
        
        if st.button("📊 Enter Grades", use_container_width=True):
            st.session_state.current_page = 'Grades'
            st.rerun()
        
        if st.button("📢 Make Announcement", use_container_width=True):
            st.session_state.current_page = 'Announcements'
            st.rerun()
    
    with col2:
        st.subheader("📅 Upcoming Deadlines")
        
        # Show upcoming assignment deadlines
        all_assignments = []
        for class_data in teacher_classes:
            assignments = assignment_model.get_assignments_by_class(class_data['_id'])
            for assignment in assignments:
                if assignment.get('due_date', datetime.now()) > datetime.now():
                    assignment['class_name'] = class_data.get('class_name', 'Unknown')
                    all_assignments.append(assignment)
        
        # Sort by due date
        all_assignments.sort(key=lambda x: x.get('due_date', datetime.now()))
        
        if all_assignments:
            for assignment in all_assignments[:5]:  # Show top 5
                due_date = assignment.get('due_date', datetime.now())
                days_left = (due_date - datetime.now()).days
                
                with st.container():
                    st.markdown(f"**{assignment['title']}**")
                    st.markdown(f"Class: {assignment['class_name']}")
                    st.markdown(f"Due: {due_date.strftime('%Y-%m-%d')} ({days_left} days left)")
                    st.markdown("---")
        else:
            st.info("No upcoming deadlines")

def render_student_dashboard():
    """Render student dashboard"""
    
    st.markdown("""
    <div class="main-header">
        <h1>👨‍🎓 Student Dashboard</h1>
        <p>Your academic overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    auth = Authorization()
    user_id = auth.get_user_id()
    
    # Get student data
    student_model = StudentModel()
    student_data = student_model.get_student_by_user_id(user_id)
    
    if not student_data:
        st.error("Student data not found.")
        return
    
    # Get class information
    class_model = ClassModel()
    class_data = class_model.find_by_id(student_data.get('class_id', ''))
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏢 Current Class",
            value=class_data.get('class_name', 'N/A') if class_data else 'N/A'
        )
    
    with col2:
        # Get attendance percentage
        attendance_model = AttendanceModel()
        start_date = datetime.now() - timedelta(days=30)  # Last 30 days
        attendance_records = attendance_model.get_student_attendance(
            student_data['_id'], start_date
        )
        
        if attendance_records:
            present_count = len([a for a in attendance_records if a.get('status') == 'present'])
            attendance_percentage = (present_count / len(attendance_records)) * 100
        else:
            attendance_percentage = 0
        
        st.metric(
            label="📅 Attendance (30 days)",
            value=f"{attendance_percentage:.1f}%"
        )
    
    with col3:
        # Get pending assignments
        assignment_model = AssignmentModel()
        if class_data:
            assignments = assignment_model.get_assignments_by_class(class_data['_id'])
            pending_assignments = len([a for a in assignments if a.get('due_date', datetime.now()) > datetime.now()])
        else:
            pending_assignments = 0
        
        st.metric(
            label="📝 Pending Assignments",
            value=pending_assignments
        )
    
    with col4:
        # Get average grade
        grade_model = GradeModel()
        grades = grade_model.get_student_grades(student_data['_id'])
        
        if grades:
            avg_percentage = sum([g.get('percentage', 0) for g in grades]) / len(grades)
        else:
            avg_percentage = 0
        
        st.metric(
            label="📊 Average Grade",
            value=f"{avg_percentage:.1f}%"
        )
    
    st.markdown("---")
    
    # Recent grades and assignments
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Recent Grades")
        
        if grades:
            recent_grades = grades[:5]  # Show last 5 grades
            
            for grade in recent_grades:
                with st.container():
                    assignment_data = assignment_model.find_by_id(grade.get('assignment_id', ''))
                    assignment_title = assignment_data.get('title', 'Unknown Assignment') if assignment_data else 'Unknown Assignment'
                    
                    st.markdown(f"**{assignment_title}**")
                    st.markdown(f"Score: {grade.get('points_earned', 0)}/{grade.get('max_points', 0)} ({grade.get('percentage', 0):.1f}%)")
                    st.markdown(f"*{grade.get('created_at', datetime.now()).strftime('%Y-%m-%d')}*")
                    st.markdown("---")
        else:
            st.info("No grades available")
    
    with col2:
        st.subheader("📝 Upcoming Assignments")
        
        if class_data:
            assignments = assignment_model.get_assignments_by_class(class_data['_id'])
            upcoming_assignments = [a for a in assignments if a.get('due_date', datetime.now()) > datetime.now()]
            upcoming_assignments.sort(key=lambda x: x.get('due_date', datetime.now()))
            
            if upcoming_assignments:
                for assignment in upcoming_assignments[:5]:  # Show next 5
                    due_date = assignment.get('due_date', datetime.now())
                    days_left = (due_date - datetime.now()).days
                    
                    with st.container():
                        st.markdown(f"**{assignment['title']}**")
                        st.markdown(f"Subject: {assignment.get('subject', 'N/A')}")
                        st.markdown(f"Due: {due_date.strftime('%Y-%m-%d')} ({days_left} days left)")
                        st.markdown("---")
            else:
                st.info("No upcoming assignments")
        else:
            st.info("Class information not available")

def render_parent_dashboard():
    """Render parent dashboard"""
    
    st.markdown("""
    <div class="main-header">
        <h1>👨‍👩‍👧 Parent Dashboard</h1>
        <p>Monitor your child's progress</p>
    </div>
    """, unsafe_allow_html=True)
    
    auth = Authorization()
    children = auth.get_user_students()  # Get parent's children
    
    if not children:
        st.info("No child records found.")
        return
    
    # If multiple children, let parent select
    if len(children) > 1:
        selected_child = st.selectbox(
            "Select Child:",
            children,
            format_func=lambda x: x.get('full_name', 'Unknown')
        )
    else:
        selected_child = children[0]
    
    if not selected_child:
        return
    
    # Get child's class information
    class_model = ClassModel()
    class_data = class_model.find_by_id(selected_child.get('class_id', ''))
    
    # Display child info
    st.subheader(f"👧 {selected_child.get('full_name', 'Child')}")
    
    # Key metrics for the child
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏢 Class",
            value=class_data.get('class_name', 'N/A') if class_data else 'N/A'
        )
    
    with col2:
        # Get attendance percentage
        attendance_model = AttendanceModel()
        start_date = datetime.now() - timedelta(days=30)  # Last 30 days
        attendance_records = attendance_model.get_student_attendance(
            selected_child['_id'], start_date
        )
        
        if attendance_records:
            present_count = len([a for a in attendance_records if a.get('status') == 'present'])
            attendance_percentage = (present_count / len(attendance_records)) * 100
        else:
            attendance_percentage = 0
        
        st.metric(
            label="📅 Attendance",
            value=f"{attendance_percentage:.1f}%"
        )
    
    with col3:
        # Get average grade
        grade_model = GradeModel()
        grades = grade_model.get_student_grades(selected_child['_id'])
        
        if grades:
            avg_percentage = sum([g.get('percentage', 0) for g in grades]) / len(grades)
        else:
            avg_percentage = 0
        
        st.metric(
            label="📊 Average Grade",
            value=f"{avg_percentage:.1f}%"
        )
    
    with col4:
        # Get pending assignments
        assignment_model = AssignmentModel()
        if class_data:
            assignments = assignment_model.get_assignments_by_class(class_data['_id'])
            pending_assignments = len([a for a in assignments if a.get('due_date', datetime.now()) > datetime.now()])
        else:
            pending_assignments = 0
        
        st.metric(
            label="📝 Pending Work",
            value=pending_assignments
        )
    
    st.markdown("---")
    
    # Child's progress charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Grade Trend")
        
        if grades:
            df_grades = pd.DataFrame(grades)
            df_grades['created_at'] = pd.to_datetime(df_grades['created_at'])
            df_grades = df_grades.sort_values('created_at')
            
            fig = px.line(
                df_grades, 
                x='created_at', 
                y='percentage',
                title='Grade Trend Over Time',
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No grade data available")
    
    with col2:
        st.subheader("📅 Attendance Pattern")
        
        if attendance_records:
            # Group attendance by status
            status_counts = {}
            for record in attendance_records:
                status = record.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                df_attendance = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
                
                fig = px.pie(
                    df_attendance, 
                    values='Count', 
                    names='Status',
                    title='Attendance Distribution (Last 30 Days)'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No attendance data available")

# Placeholder functions for other pages - these will be implemented in separate files
def render_user_management():
    st.title("User Management")
    st.info("User management interface coming soon...")

def render_class_management():
    st.title("Class Management")
    st.info("Class management interface coming soon...")

def render_student_management():
    st.title("Student Management")
    st.info("Student management interface coming soon...")

def render_teacher_management():
    st.title("Teacher Management")
    st.info("Teacher management interface coming soon...")

def render_my_classes():
    st.title("My Classes")
    st.info("Class details interface coming soon...")

def render_attendance():
    st.title("Attendance Management")
    st.info("Attendance management interface coming soon...")

def render_assignments():
    st.title("Assignments")
    st.info("Assignment management interface coming soon...")

def render_grades():
    st.title("Grades Management")
    st.info("Grade management interface coming soon...")

def render_students():
    st.title("Students")
    st.info("Student listing interface coming soon...")

def render_reports():
    st.title("Reports")
    st.info("Reporting interface coming soon...")

def render_announcements():
    st.title("Announcements")
    st.info("Announcement management interface coming soon...")

def render_system_settings():
    st.title("System Settings")
    st.info("System settings interface coming soon...")

def render_child_progress():
    st.title("Child Progress")
    st.info("Child progress interface coming soon...")

def render_communication():
    st.title("Communication")
    st.info("Communication interface coming soon...")