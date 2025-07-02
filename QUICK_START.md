# 🏫 School Management System - Quick Start Guide

## 🚀 Your MongoDB Atlas Database is Ready!

I've configured your school management system to work with your MongoDB Atlas cluster. Here's everything you need to know:

### 📊 Database Configuration
- **MongoDB URI**: `mongodb+srv://workdhruvpathak:Miss@121831125@fastapi.nwebt2x.mongodb.net/`
- **Database Name**: `school_management`
- **Status**: ✅ Ready to connect and store data

---

## 🛠️ Setup Instructions

### Option 1: Quick Setup (Recommended)

**For Linux/Mac:**
```bash
# 1. Make scripts executable
chmod +x setup.sh run_init.sh run_app.sh

# 2. Run setup
./setup.sh

# 3. Initialize database with sample data
./run_init.sh

# 4. Start the application
./run_app.sh
```

**For Windows:**
```batch
# 1. Run setup
setup.bat

# 2. Initialize database with sample data
run_init.bat

# 3. Start the application
run_app.bat
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python init_database.py

# 4. Start application
streamlit run app.py
```

---

## 🔑 Default Login Credentials

Once the system is running, you can log in with these accounts:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| **Admin** | `admin` | `admin123` | Full system access |
| **Teacher** | `teacher1` | `teacher123` | Sarah Johnson - Math & Science |
| **Teacher** | `teacher2` | `teacher123` | Michael Brown - English |
| **Teacher** | `teacher3` | `teacher123` | Emily Davis - Science |
| **Student** | `student1` | `student123` | John Smith - Grade 10A |
| **Student** | `student2` | `student123` | Emma Wilson - Grade 10A |
| **Student** | `student3` | `student123` | Alex Martinez - Grade 11A |
| **Parent** | `parent1` | `parent123` | Robert Smith (John's father) |
| **Parent** | `parent2` | `parent123` | Linda Wilson (Emma's mother) |

---

## 🗄️ Database Structure Created

The initialization script will create and populate these collections:

### 👥 Users Collection
- **11 users** across all roles (admin, teachers, students, parents)
- Secure password hashing with bcrypt
- Complete user profiles with contact information

### 🏫 Classes Collection
- **4 classes**: Grade 9A, Grade 10A, Grade 10B, Grade 11A
- Subject assignments and capacity limits
- Academic year 2024-2025 setup

### 👨‍🏫 Teachers Collection
- **3 teachers** with different specializations
- Department assignments and class responsibilities
- Hire dates and subject expertise

### 👨‍🎓 Students Collection
- **5 students** distributed across classes
- Parent-child relationships established
- Admission dates and subject enrollment

### 📝 Assignments Collection
- **4 sample assignments** across different subjects
- Due dates, instructions, and point values
- Subject-specific content (Math, Science, English, Physics)

### 🎯 Grades Collection
- **Realistic grade data** for all student-assignment combinations
- Scores ranging from 70-100% for demonstration
- Grading dates and teacher comments

### 📅 Attendance Collection
- **30 days of attendance data** for all students
- 90% attendance rate (realistic simulation)
- Various statuses: present, absent, late

### 📢 Announcements Collection
- **4 announcements** for different audiences
- Welcome messages, parent-teacher conferences, events
- Priority levels and target audience settings

---

## 🌟 Key Features You Can Test

### 🔐 Authentication & Security
- ✅ Role-based login system
- ✅ Session management with timeout
- ✅ Account lockout protection
- ✅ Secure password hashing

### 📊 Admin Dashboard
- ✅ System overview with live metrics
- ✅ User distribution charts
- ✅ Recent activity monitoring
- ✅ User management capabilities

### 👩‍🏫 Teacher Dashboard
- ✅ Class and student management
- ✅ Assignment creation and grading
- ✅ Attendance marking interface
- ✅ Performance analytics

### 👨‍🎓 Student Dashboard
- ✅ Personal academic overview
- ✅ Assignment and grade tracking
- ✅ Attendance monitoring
- ✅ Progress visualization

### 👨‍👩‍👧 Parent Dashboard
- ✅ Child progress monitoring
- ✅ Grade and attendance tracking
- ✅ Communication with teachers
- ✅ Performance analytics

---

## 📱 Application Features

### 🎨 User Interface
- **Modern, responsive design** with role-specific navigation
- **Interactive charts and graphs** using Plotly
- **Intuitive sidebar navigation** with quick actions
- **Real-time data updates** and notifications

### 💾 Data Management
- **MongoDB Atlas integration** with your cluster
- **Automatic data validation** and integrity checks
- **Indexed collections** for optimal performance
- **Comprehensive audit trails** with timestamps

### 🔔 Notification System
- **Email integration** ready for SMTP configuration
- **Automated alerts** for low attendance
- **Assignment reminders** with due date notifications
- **Grade notifications** to parents

---

## 🌐 Access Your Application

1. **Start the application** using the steps above
2. **Open your browser** to: `http://localhost:8501`
3. **Login** with any of the default credentials
4. **Explore** the role-specific dashboards and features

---

## 🔧 Customization Options

### 📧 Email Configuration
Edit `.env` file to add your SMTP settings:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### 🎨 UI Customization
- Modify `.streamlit/config.toml` for theme colors
- Update CSS in UI components for styling
- Add your school logo and branding

### 📊 Data Customization
- Add more users, classes, or subjects
- Modify grade scales and attendance policies
- Customize report templates and analytics

---

## 🆘 Troubleshooting

### Common Issues:

**Database Connection Error:**
- Verify your MongoDB Atlas cluster is active
- Check the connection string in `.env` file
- Ensure IP address is whitelisted in MongoDB Atlas

**Module Import Errors:**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**Permission Errors (Linux/Mac):**
- Make scripts executable: `chmod +x *.sh`

**Port Already in Use:**
- Change port in `.env`: `PORT=8502`
- Or stop other applications using port 8501

---

## 📞 Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure MongoDB Atlas connection is working
4. Check the application logs in the `logs/` directory

---

## 🎉 You're All Set!

Your school management system is now fully configured with:
- ✅ **MongoDB Atlas** database connection
- ✅ **Sample data** for immediate testing
- ✅ **Complete user management** system
- ✅ **Role-based dashboards** for all user types
- ✅ **Real-time analytics** and reporting
- ✅ **Professional UI** with modern design

**Start exploring your new school management system!** 🚀