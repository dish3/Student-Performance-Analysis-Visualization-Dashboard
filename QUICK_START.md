# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
Run in MySQL:
```bash
mysql -u root -p < database.sql
```

### Step 3: Configure Database
Edit `config.py` - change password:
```python
'password': 'YOUR_MYSQL_PASSWORD'
```

### Step 4: Create Admin Account
```bash
python create_admin.py
```
Enter username and password when prompted.

### Step 5: Run Application
```bash
python app.py
```

### Step 6: Open Browser
Go to: `http://localhost:5000`

---

## 📋 Quick Workflow

### Admin Workflow:
1. Login as admin
2. Create a test (Tests → Create Test)
3. Add questions with max marks
4. Add students (Students → Add Student)
5. Add faculty (Faculty → Add Faculty)

### Faculty Workflow:
1. Login as faculty
2. Enter Marks → Select test and student
3. Enter obtained marks for each question
4. View Marks → See all results

---

## ✅ Verify Setup

Check database:
```sql
USE student_test_evaluation;
SHOW TABLES;
```

Should show: `faculty`, `students`, `tests`, `test_questions`, `student_test_marks`

---

## 🔧 Common Issues

| Problem | Solution |
|---------|----------|
| Can't connect to database | Check MySQL is running + correct password in config.py |
| Login failed | Run create_admin.py or create_faculty.py first |
| Port 5000 in use | Change port in app.py: app.run(port=5001) |

---

## 📝 Default Credentials

No default credentials - you must create accounts using:
- `python create_admin.py` for admin
- `python create_faculty.py` for faculty

Or create faculty from admin panel after logging in as admin.
