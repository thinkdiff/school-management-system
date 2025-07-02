// Initialize MongoDB with default admin user
db = db.getSiblingDB('school_management');

// Create default admin user
db.users.insertOne({
  _id: ObjectId(),
  username: 'admin',
  email: 'admin@school.com',
  password: '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3P0L9v4g0C', // password: admin123
  role: 'admin',
  full_name: 'System Administrator',
  created_at: new Date(),
  updated_at: new Date(),
  is_active: true,
  profile: {
    phone: '+1234567890',
    address: 'School Address',
    date_of_birth: null,
    gender: null
  }
});

// Create indexes
db.users.createIndex({ 'username': 1 }, { unique: true });
db.users.createIndex({ 'email': 1 }, { unique: true });
db.students.createIndex({ 'student_id': 1 }, { unique: true });
db.teachers.createIndex({ 'teacher_id': 1 }, { unique: true });
db.classes.createIndex({ 'class_code': 1 }, { unique: true });
db.attendance.createIndex({ 'student_id': 1, 'date': 1 });
db.assignments.createIndex({ 'class_id': 1, 'due_date': 1 });
db.grades.createIndex({ 'student_id': 1, 'subject_id': 1 });

print('Database initialized successfully!');