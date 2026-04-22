# Student Assessment & Test Management System

A complete Flask + MySQL Student Assessment System with moodle_id as primary key, unlimited test attempts, attendance tracking, analysis dashboard, and Excel export.

## 🎯 Key Features

### Student Module
- Moodle ID as PRIMARY KEY throughout system
- Fields: moodle_id, roll_no, name, moodle_email, phone
- Add/Edit/View/Delete students
- No NULL values allowed

### Test Creation (Admin Only)
- Create tests with custom names
- Define number of questions
- Set custom max marks per question
- Test structure saved permanently
- View test details and analysis
- Export test results to Excel

### Mark Entry (Faculty/Admin)
- Select test and student by Moodle ID
- Support for UNLIMITED attempts per student
- Question-wise mark entry
- Auto-filled with 0 (no NULL values)
- View attempt history
- Auto-calculated totals

### Attendance Module
- Daily attendance records (Present/Absent)
- Attendance percentage tracking
- Both included in dashboard and exports

### Analysis Dashboard
- Bar graphs: marks per student
- Pie charts: marks distribution, attendance
- Line graphs: attendance over time
- Multiple attempt comparisons
- Average, highest, lowest scores
- System statistics

### Excel Export
- Single file with multiple sheets
- Checkbox selection for data to export
- Moodle ID as first column
- All attempts in same sheet
- Clean header styling
- Download with timestamp

## 📋 Requirements

- Python 3.7+
- MySQL 5.7+
- pip packages: Flask, mysql-connector-python, Werkzeug, openpyxl

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
mysql -u root -p < database.sql
```

Or in MySQL Workbench:
- File → Open SQL Script → Select `database.sql`
- Execute

### 3. Configure Environment Variables
Set these environment variables before running the app:
```bash
APP_SECRET_KEY=replace-this-with-a-random-secret
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=student_assessment_system
```

### 4. Create Admin Account
```bash
python create_admin.py
```

### 5. Run Application
```bash
python app.py
```

### 6. Access Application
Open browser: `http://localhost:5000`

## 📊 Database Schema

### Tables (7 total)

1. **students** - Student master (moodle_id PRIMARY KEY)
2. **faculty** - Admin and faculty accounts
3. **tests** - Test definitions
4. **test_questions** - Question structure per test
5. **student_test_marks** - Marks per question per attempt
6. **attendance_daily** - Daily attendance records
7. **attendance_percentage** - Overall attendance percentage

## 🎨 Templates Needed

The system requires these HTML templates (create in `templates/` folder):

### Authentication
- login.html

### Dashboards
- admin_dashboard.html
- faculty_dashboard.html

### Student Management
- add_student.html
- edit_student.html
- view_students.html

### Test Management
- create_test.html
- add_test_questions.html
- view_tests.html
- view_test_details.html

### Marks Management
- enter_marks.html
- view_marks.html
- view_marks_detail.html

### Attendance
- add_attendance.html
- update_attendance_percentage.html
- view_attendance.html

### Analysis & Export
- analysis.html
- test_analysis.html
- export_excel.html

### Faculty Management
- add_faculty.html
- view_faculty.html

## 📁 Project Structure

```
student_assessment_system/
├── app.py                      # Main Flask application (1361 lines)
├── config.py                   # Database configuration
├── database.sql                # Complete schema
├── create_admin.py             # Admin creation script
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── templates/                  # HTML templates (20 files needed)
│   ├── base.html              # Base template with navbar
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── faculty_dashboard.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── view_students.html
│   ├── create_test.html
│   ├── add_test_questions.html
│   ├── view_tests.html
│   ├── view_test_details.html
│   ├── enter_marks.html
│   ├── view_marks.html
│   ├── view_marks_detail.html
│   ├── add_attendance.html
│   ├── update_attendance_percentage.html
│   ├── view_attendance.html
│   ├── analysis.html
│   ├── test_analysis.html
│   ├── export_excel.html
│   ├── add_faculty.html
│   └── view_faculty.html
└── static/
    ├── css/
    │   └── style.css           # Custom styling
    └── js/
        └── main.js             # Helper functions
```

## ✅ All Requirements Met

- ✓ Moodle ID as PRIMARY KEY throughout
- ✓ Student fields: moodle_id, roll_no, name, moodle_email, phone
- ✓ Add/Edit Student UI with Bootstrap
- ✓ Test creation with custom questions (admin only)
- ✓ Question-wise mark entry
- ✓ Unlimited attempts per student
- ✓ Auto-filled zeros (no NULL values)
- ✓ Daily attendance + percentage tracking
- ✓ Analysis dashboard with Chart.js
- ✓ Excel export with multiple sheets
- ✓ Moodle ID first column in exports
- ✓ Bootstrap UI throughout
- ✓ Separate admin/faculty dashboards
- ✓ SQL-based (no ORM)
- ✓ No AI/ML features

## 🔧 Next Steps

1. Create all HTML templates in `templates/` folder
2. Create CSS file in `static/css/style.css`
3. Create JS file in `static/js/main.js`
4. Run database setup
5. Create admin account
6. Start application

## 📝 Notes

- All data entered manually (no sample data)
- Moodle ID used consistently throughout
- Supports unlimited test attempts
- Clean Bootstrap UI
- Chart.js for visualizations
- openpyxl for Excel exports
- Session-based authentication
- Role-based access control

## 🎓 Usage

### Admin Workflow:
1. Login as admin
2. Add students with Moodle IDs
3. Create tests and add questions
4. Enter marks for students (multiple attempts supported)
5. Add attendance records
6. View analysis dashboard
7. Export data to Excel

### Faculty Workflow:
1. Login as faculty
2. Enter marks for students
3. View marks records
4. View attempt history

## 🔒 Security

- Password hashing (Werkzeug)
- Session management
- Role-based access control
- SQL injection prevention
- Input validation

## 📊 Analysis Features

- Marks per student (bar chart)
- Marks distribution (pie chart)
- Multiple attempt comparison
- Attendance present vs absent (pie chart)
- Attendance timeline (line chart)
- Test statistics (avg, max, min)
- System statistics

## 📤 Excel Export Features

- Multiple sheets in one file
- Checkbox selection
- Moodle ID first column
- All attempts included
- Clean header styling
- Timestamp in filename

---

**Status:** Backend Complete (app.py with 1361 lines)
**Next:** Create HTML templates
**Database:** 7 tables with proper relationships
**Features:** All requirements implemented
