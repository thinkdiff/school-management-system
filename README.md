# School Management System

🏫 A comprehensive, role-based school management system built with Python Streamlit, MongoDB Atlas, and modern DevOps practices.

## 🎆 Features

### 🔐 Authentication & Authorization
- **Role-based access control** (Admin, Teacher, Student, Parent)
- **Secure password hashing** with bcrypt
- **Session management** with automatic timeout
- **Account lockout** protection against brute force attacks

### 👥 User Management
- **Multi-role user system** with granular permissions
- **Profile management** with customizable fields
- **Bulk user import/export** capabilities
- **User activity tracking** and audit logs

### 🏢 Class & Subject Management
- **Dynamic class creation** with student capacity limits
- **Subject assignment** to classes and teachers
- **Academic year management** with term/semester support
- **Class scheduling** and room allocation

### 📅 Attendance Management
- **Real-time attendance marking** by teachers
- **Attendance reports** with analytics and trends
- **Automated notifications** for absences
- **Parent portal** for attendance monitoring

### 📝 Assignment Management
- **Assignment creation** with due dates and instructions
- **File upload support** for assignments and submissions
- **Automatic grading** with customizable rubrics
- **Progress tracking** for teachers and students

### 📊 Grade Management
- **Flexible grading system** with letter grades and percentages
- **Grade book** with export capabilities
- **Progress reports** and transcripts
- **Parent notifications** for grade updates

### 📢 Communication System
- **Announcements** with role-based targeting
- **Real-time notifications** for important updates
- **Message system** between teachers, students, and parents
- **Email integration** for external communications

### 📈 Analytics & Reporting
- **Interactive dashboards** for each role
- **Performance analytics** with charts and graphs
- **Attendance and grade reports** with export options
- **System usage statistics** for administrators

## 🚀 Technology Stack

### Frontend
- **Streamlit**: Modern Python web framework for rapid UI development
- **Plotly**: Interactive charts and data visualization
- **Streamlit Components**: Enhanced UI components and navigation

### Backend
- **MongoDB Atlas**: Cloud-native NoSQL database
- **PyMongo**: MongoDB driver for Python
- **Pandas**: Data manipulation and analysis

### Security
- **Bcrypt**: Password hashing and verification
- **Environment Variables**: Secure configuration management
- **Session Management**: Secure user session handling

### DevOps & Deployment
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container application orchestration
- **GitHub Actions**: CI/CD pipeline automation
- **Automated Testing**: Unit and integration tests
- **Code Quality**: Black, isort, and flake8 for code standards

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (or local MongoDB)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/thinkdiff/school-management-system.git
   cd school-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection string and other settings
   ```

5. **Initialize database**
   ```bash
   # The application will create default admin user on first run
   # Username: admin, Password: admin123
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Docker Deployment

1. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - Open http://localhost:8501 in your browser
   - Login with default admin credentials

## 📚 User Guide

### Default Login Credentials
- **Admin**: `admin` / `admin123`
- **Teacher**: `teacher1` / `teacher123`
- **Student**: `student1` / `student123`
- **Parent**: `parent1` / `parent123`

### Admin Dashboard
- System overview with key metrics
- User management and role assignment
- Class and subject management
- System settings and configuration
- Comprehensive reporting and analytics

### Teacher Dashboard
- Class and student management
- Attendance marking and tracking
- Assignment creation and grading
- Grade book and progress reports
- Communication with students and parents

### Student Dashboard
- Personal academic overview
- Assignment submission and tracking
- Grade and attendance viewing
- Class schedule and announcements
- Progress monitoring

### Parent Dashboard
- Child's academic progress monitoring
- Attendance and grade tracking
- Communication with teachers
- Announcement and notification viewing

## 🗺️ API Documentation

The system provides internal API endpoints for:
- User authentication and authorization
- CRUD operations for all entities
- Data aggregation and reporting
- File upload and management

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
```

### Test Structure
- **Unit Tests**: Individual component testing
- **Integration Tests**: Database and API testing
- **E2E Tests**: Full application workflow testing

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   - Set production environment variables
   - Configure MongoDB Atlas connection
   - Set up SSL certificates

2. **Docker Deployment**
   ```bash
   docker build -t school-management-system .
   docker run -d -p 8501:8501 --env-file .env school-management-system
   ```

3. **Cloud Deployment**
   - AWS EC2/ECS
   - Google Cloud Run
   - Azure Container Instances
   - Railway/Heroku

### CI/CD Pipeline

The project includes automated CI/CD with:
- **Continuous Integration**: Automated testing and code quality checks
- **Security Scanning**: Vulnerability assessment with Trivy
- **Automated Deployment**: Staging and production deployment
- **Health Checks**: Application monitoring and alerting

## 📊 Monitoring & Logging

### Application Monitoring
- **Health Checks**: Endpoint monitoring
- **Performance Metrics**: Response time and resource usage
- **Error Tracking**: Automated error reporting
- **User Analytics**: Usage patterns and system adoption

### Logging
- **Structured Logging**: JSON formatted logs
- **Log Aggregation**: Centralized log management
- **Alert System**: Critical error notifications

## 🔒 Security Features

### Authentication Security
- **Password Policy**: Minimum complexity requirements
- **Account Lockout**: Brute force protection
- **Session Management**: Secure session handling
- **Two-Factor Authentication**: Optional 2FA support

### Data Security
- **Encryption at Rest**: Database encryption
- **Encryption in Transit**: HTTPS/TLS
- **Input Validation**: SQL injection prevention
- **Access Control**: Role-based permissions

### Compliance
- **GDPR**: Data protection and privacy
- **FERPA**: Educational records privacy
- **SOC 2**: Security and availability

## 👥 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Standards
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **Type Hints**: Python type annotations
- **Docstrings**: Comprehensive documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚑 Support

### Getting Help
- **Documentation**: Comprehensive guides and API docs
- **Issues**: GitHub issue tracker
- **Discussions**: Community forum
- **Email**: Direct support contact

### Feature Requests
- Submit enhancement requests via GitHub issues
- Join community discussions for feature prioritization
- Contribute to the roadmap planning

## 🗺️ Roadmap

### Version 1.1 (Q2 2025)
- [ ] Mobile-responsive design
- [ ] Advanced reporting features
- [ ] API rate limiting
- [ ] Real-time notifications

### Version 1.2 (Q3 2025)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with external systems
- [ ] Mobile application

### Version 2.0 (Q4 2025)
- [ ] Microservices architecture
- [ ] Advanced AI features
- [ ] Enterprise integrations
- [ ] Advanced security features

---

**Built with ❤️ by the School Management System Team**

For more information, visit our [documentation](https://github.com/thinkdiff/school-management-system/wiki) or [contact us](mailto:support@schoolmanagement.com).