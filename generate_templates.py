"""
Template Generator for Student Performance Analysis and Visualization Dashboard
Run this script to automatically generate all HTML templates
"""

import os

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

templates = {
    'login.html': '''{% extends "base.html" %}

{% block title %}Login - Student Performance Analysis and Visualization Dashboard{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-5">
        <div class="card shadow">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Login</h2>
                <form method="POST">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'admin_dashboard.html': '''{% extends "base.html" %}

{% block title %}Admin Dashboard{% endblock %}

{% block content %}
<h2 class="mb-4">Admin Dashboard</h2>

<div class="row">
    <div class="col-md-3 mb-3">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <h5 class="card-title">Total Students</h5>
                <h2>{{ total_students }}</h2>
                <a href="{{ url_for('view_students') }}" class="btn btn-light btn-sm">View All</a>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card text-white bg-success">
            <div class="card-body">
                <h5 class="card-title">Total Tests</h5>
                <h2>{{ total_tests }}</h2>
                <a href="{{ url_for('view_tests') }}" class="btn btn-light btn-sm">View All</a>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card text-white bg-info">
            <div class="card-body">
                <h5 class="card-title">Total Attempts</h5>
                <h2>{{ total_attempts }}</h2>
                <a href="{{ url_for('view_marks') }}" class="btn btn-light btn-sm">View All</a>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-3">
        <div class="card text-white bg-warning">
            <div class="card-body">
                <h5 class="card-title">Attendance Records</h5>
                <h2>{{ total_attendance }}</h2>
                <a href="{{ url_for('view_attendance') }}" class="btn btn-light btn-sm">View All</a>
            </div>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                Quick Actions
            </div>
            <div class="list-group list-group-flush">
                <a href="{{ url_for('add_student') }}" class="list-group-item list-group-item-action">Add New Student</a>
                <a href="{{ url_for('create_test') }}" class="list-group-item list-group-item-action">Create New Test</a>
                <a href="{{ url_for('enter_marks') }}" class="list-group-item list-group-item-action">Enter Student Marks</a>
                <a href="{{ url_for('add_attendance') }}" class="list-group-item list-group-item-action">Add Attendance</a>
                <a href="{{ url_for('analysis') }}" class="list-group-item list-group-item-action">View Analysis Dashboard</a>
                <a href="{{ url_for('export_excel') }}" class="list-group-item list-group-item-action">Export to Excel</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'faculty_dashboard.html': '''{% extends "base.html" %}

{% block title %}Faculty Dashboard{% endblock %}

{% block content %}
<h2 class="mb-4">Faculty Dashboard</h2>

<div class="row">
    <div class="col-md-4 mb-3">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <h5 class="card-title">Total Students</h5>
                <h2>{{ total_students }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="card text-white bg-success">
            <div class="card-body">
                <h5 class="card-title">Total Tests</h5>
                <h2>{{ total_tests }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="card text-white bg-info">
            <div class="card-body">
                <h5 class="card-title">Total Attempts</h5>
                <h2>{{ total_attempts }}</h2>
            </div>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                Quick Actions
            </div>
            <div class="list-group list-group-flush">
                <a href="{{ url_for('enter_marks') }}" class="list-group-item list-group-item-action">Enter Student Marks</a>
                <a href="{{ url_for('view_marks') }}" class="list-group-item list-group-item-action">View All Marks</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'add_student.html': '''{% extends "base.html" %}

{% block title %}Add Student{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Add New Student</h2>
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="moodle_id" class="form-label">Moodle ID</label>
                        <input type="text" class="form-control" id="moodle_id" name="moodle_id" required>
                        <div class="form-text">Primary identifier for the student</div>
                    </div>
                    <div class="mb-3">
                        <label for="roll_no" class="form-label">Roll Number</label>
                        <input type="text" class="form-control" id="roll_no" name="roll_no" required>
                    </div>
                    <div class="mb-3">
                        <label for="name" class="form-label">Student Name</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="moodle_email" class="form-label">Moodle Email</label>
                        <input type="email" class="form-control" id="moodle_email" name="moodle_email" required>
                    </div>
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone</label>
                        <input type="text" class="form-control" id="phone" name="phone" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Student</button>
                    <a href="{{ url_for('view_students') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'edit_student.html': '''{% extends "base.html" %}

{% block title %}Edit Student{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Edit Student: {{ student.moodle_id }}</h2>
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Moodle ID</label>
                        <input type="text" class="form-control" value="{{ student.moodle_id }}" disabled>
                        <div class="form-text">Moodle ID cannot be changed</div>
                    </div>
                    <div class="mb-3">
                        <label for="roll_no" class="form-label">Roll Number</label>
                        <input type="text" class="form-control" id="roll_no" name="roll_no" value="{{ student.roll_no }}" required>
                    </div>
                    <div class="mb-3">
                        <label for="name" class="form-label">Student Name</label>
                        <input type="text" class="form-control" id="name" name="name" value="{{ student.name }}" required>
                    </div>
                    <div class="mb-3">
                        <label for="moodle_email" class="form-label">Moodle Email</label>
                        <input type="email" class="form-control" id="moodle_email" name="moodle_email" value="{{ student.moodle_email }}" required>
                    </div>
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone</label>
                        <input type="text" class="form-control" id="phone" name="phone" value="{{ student.phone }}" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Update Student</button>
                    <a href="{{ url_for('view_students') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'view_students.html': '''{% extends "base.html" %}

{% block title %}View Students{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>All Students</h2>
    <a href="{{ url_for('add_student') }}" class="btn btn-primary">Add New Student</a>
</div>

{% if students %}
<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Moodle ID</th>
                        <th>Roll No</th>
                        <th>Name</th>
                        <th>Moodle Email</th>
                        <th>Phone</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student.moodle_id }}</td>
                        <td>{{ student.roll_no }}</td>
                        <td>{{ student.name }}</td>
                        <td>{{ student.moodle_email }}</td>
                        <td>{{ student.phone }}</td>
                        <td>
                            <a href="{{ url_for('edit_student', moodle_id=student.moodle_id) }}" class="btn btn-sm btn-warning">Edit</a>
                            <a href="{{ url_for('delete_student', moodle_id=student.moodle_id) }}" 
                               class="btn btn-sm btn-danger" 
                               onclick="return confirm('Are you sure you want to delete this student?')">Delete</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% else %}
<div class="alert alert-info">
    No students found. <a href="{{ url_for('add_student') }}">Add your first student</a>
</div>
{% endif %}
{% endblock %}'''
}

print("Generating templates...")
count = 0

for filename, content in templates.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f"✓ Created {filename}")

print(f"\n✅ Successfully generated {count} templates!")
print("\nRun this script again to generate more templates, or run the app now!")
