"""
Generate final templates and static files
"""

import os

os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

templates = {
    'add_attendance.html': '''{% extends "base.html" %}
{% block title %}Add Attendance{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Add Daily Attendance</h2>
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="moodle_id" class="form-label">Select Student</label>
                        <select class="form-select" id="moodle_id" name="moodle_id" required>
                            <option value="">-- Choose Student --</option>
                            {% for student in students %}
                            <option value="{{ student.moodle_id }}">{{ student.moodle_id }} - {{ student.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label">Date</label>
                        <input type="date" class="form-control" id="date" name="date" required>
                    </div>
                    <div class="mb-3">
                        <label for="status" class="form-label">Status</label>
                        <select class="form-select" id="status" name="status" required>
                            <option value="">-- Choose Status --</option>
                            <option value="Present">Present</option>
                            <option value="Absent">Absent</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Attendance</button>
                    <a href="{{ url_for('view_attendance') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'update_attendance_percentage.html': '''{% extends "base.html" %}
{% block title %}Update Attendance Percentage{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Update Attendance Percentage</h2>
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="moodle_id" class="form-label">Select Student</label>
                        <select class="form-select" id="moodle_id" name="moodle_id" required>
                            <option value="">-- Choose Student --</option>
                            {% for student in students %}
                            <option value="{{ student.moodle_id }}">
                                {{ student.moodle_id }} - {{ student.name }} 
                                (Current: {{ student.attendance_percent or 0 }}%)
                            </option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="attendance_percent" class="form-label">Attendance Percentage</label>
                        <input type="number" class="form-control" id="attendance_percent" name="attendance_percent" 
                               min="0" max="100" step="0.01" required>
                        <div class="form-text">Enter percentage between 0 and 100</div>
                    </div>
                    <button type="submit" class="btn btn-primary">Update Percentage</button>
                    <a href="{{ url_for('view_attendance') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'view_attendance.html': '''{% extends "base.html" %}
{% block title %}View Attendance{% endblock %}
{% block content %}
<h2 class="mb-4">Attendance Records</h2>

<ul class="nav nav-tabs mb-3" role="tablist">
    <li class="nav-item" role="presentation">
        <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#daily" type="button">Daily Attendance</button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#percentage" type="button">Attendance Percentage</button>
    </li>
</ul>

<div class="tab-content">
    <div class="tab-pane fade show active" id="daily">
        <div class="d-flex justify-content-between mb-3">
            <h4>Daily Attendance Records</h4>
            <a href="{{ url_for('add_attendance') }}" class="btn btn-primary">Add Attendance</a>
        </div>
        {% if daily_records %}
        <div class="card">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead class="table-dark">
                            <tr>
                                <th>Moodle ID</th>
                                <th>Roll No</th>
                                <th>Name</th>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for record in daily_records %}
                            <tr>
                                <td>{{ record.moodle_id }}</td>
                                <td>{{ record.roll_no }}</td>
                                <td>{{ record.name }}</td>
                                <td>{{ record.date.strftime('%Y-%m-%d') if record.date else 'N/A' }}</td>
                                <td>
                                    <span class="badge {% if record.status == 'Present' %}bg-success{% else %}bg-danger{% endif %}">
                                        {{ record.status }}
                                    </span>
                                </td>
                                <td>
                                    <a href="{{ url_for('delete_attendance', record_id=record.record_id) }}" 
                                       class="btn btn-sm btn-danger" 
                                       onclick="return confirm('Delete this record?')">Delete</a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info">No daily attendance records found.</div>
        {% endif %}
    </div>
    
    <div class="tab-pane fade" id="percentage">
        <div class="d-flex justify-content-between mb-3">
            <h4>Attendance Percentage</h4>
            <a href="{{ url_for('update_attendance_percentage') }}" class="btn btn-primary">Update Percentage</a>
        </div>
        {% if percentage_records %}
        <div class="card">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead class="table-dark">
                            <tr>
                                <th>Moodle ID</th>
                                <th>Roll No</th>
                                <th>Name</th>
                                <th>Attendance %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for record in percentage_records %}
                            <tr>
                                <td>{{ record.moodle_id }}</td>
                                <td>{{ record.roll_no }}</td>
                                <td>{{ record.name }}</td>
                                <td>
                                    <span class="badge {% if record.attendance_percent >= 75 %}bg-success{% elif record.attendance_percent >= 50 %}bg-warning{% else %}bg-danger{% endif %}">
                                        {{ record.attendance_percent or 0 }}%
                                    </span>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info">No attendance percentage records found.</div>
        {% endif %}
    </div>
</div>
{% endblock %}''',

    'analysis.html': '''{% extends "base.html" %}
{% block title %}Analysis Dashboard{% endblock %}
{% block content %}
<h2 class="mb-4">Analysis Dashboard</h2>

<div class="row mb-4">
    <div class="col-md-3">
        <div class="card text-white bg-primary">
            <div class="card-body text-center">
                <h5>Total Students</h5>
                <h2>{{ total_students }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-success">
            <div class="card-body text-center">
                <h5>Total Tests</h5>
                <h2>{{ total_tests }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-info">
            <div class="card-body text-center">
                <h5>Total Attempts</h5>
                <h2>{{ total_attempts }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-warning">
            <div class="card-body text-center">
                <h5>Attendance Entries</h5>
                <h2>{{ total_attendance_entries }}</h2>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">Marks Per Student</div>
            <div class="card-body">
                <canvas id="marksChart"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">Attendance Distribution</div>
            <div class="card-body">
                <canvas id="attendanceChart"></canvas>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">Attendance Over Time</div>
            <div class="card-body">
                <canvas id="attendanceTimelineChart"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">Attendance Percentages</div>
            <div class="card-body">
                <canvas id="attendancePercentChart"></canvas>
            </div>
        </div>
    </div>
</div>

<script>
// Marks Chart
const marksData = {{ marks_data|tojson }};
const marksLabels = marksData.map(d => d.name + ' (Attempt ' + d.attempt_no + ')');
const marksValues = marksData.map(d => (d.total_obtained / d.total_max * 100).toFixed(2));

new Chart(document.getElementById('marksChart'), {
    type: 'bar',
    data: {
        labels: marksLabels,
        datasets: [{
            label: 'Percentage',
            data: marksValues,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});

// Attendance Pie Chart
const attendanceSummary = {{ attendance_summary|tojson }};
const attendanceLabels = attendanceSummary.map(d => d.status);
const attendanceCounts = attendanceSummary.map(d => d.count);

new Chart(document.getElementById('attendanceChart'), {
    type: 'pie',
    data: {
        labels: attendanceLabels,
        datasets: [{
            data: attendanceCounts,
            backgroundColor: ['rgba(75, 192, 192, 0.5)', 'rgba(255, 99, 132, 0.5)']
        }]
    }
});

// Attendance Timeline
const timeline = {{ attendance_timeline|tojson }};
const timelineLabels = timeline.map(d => d.date);
const presentData = timeline.map(d => d.present_count);
const absentData = timeline.map(d => d.absent_count);

new Chart(document.getElementById('attendanceTimelineChart'), {
    type: 'line',
    data: {
        labels: timelineLabels,
        datasets: [{
            label: 'Present',
            data: presentData,
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }, {
            label: 'Absent',
            data: absentData,
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }]
    }
});

// Attendance Percentage Chart
const percentages = {{ attendance_percentages|tojson }};
const percentLabels = percentages.map(d => d.name);
const percentValues = percentages.map(d => d.attendance_percent);

new Chart(document.getElementById('attendancePercentChart'), {
    type: 'bar',
    data: {
        labels: percentLabels,
        datasets: [{
            label: 'Attendance %',
            data: percentValues,
            backgroundColor: 'rgba(153, 102, 255, 0.5)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
</script>
{% endblock %}''',

    'test_analysis.html': '''{% extends "base.html" %}
{% block title %}Test Analysis{% endblock %}
{% block content %}
<div class="mb-4">
    <a href="{{ url_for('view_tests') }}" class="btn btn-secondary">&larr; Back to Tests</a>
</div>

<h2 class="mb-4">Analysis: {{ test.test_name }}</h2>

<div class="row mb-4">
    <div class="col-md-3">
        <div class="card">
            <div class="card-body text-center">
                <h6>Total Attempts</h6>
                <h3>{{ stats.total_attempts or 0 }}</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body text-center">
                <h6>Average Marks</h6>
                <h3>{{ "%.2f"|format(stats.avg_marks or 0) }}</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body text-center">
                <h6>Highest Score</h6>
                <h3>{{ stats.max_marks or 0 }}</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body text-center">
                <h6>Lowest Score</h6>
                <h3>{{ stats.min_marks or 0 }}</h3>
            </div>
        </div>
    </div>
</div>

<div class="card">
    <div class="card-header">Student Performance</div>
    <div class="card-body">
        <canvas id="testMarksChart"></canvas>
    </div>
</div>

<script>
const marksData = {{ marks_data|tojson }};
const labels = marksData.map(d => d.name + ' (Attempt ' + d.attempt_no + ')');
const values = marksData.map(d => (d.total_obtained / d.total_max * 100).toFixed(2));

new Chart(document.getElementById('testMarksChart'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Percentage',
            data: values,
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
</script>
{% endblock %}''',

    'export_excel.html': '''{% extends "base.html" %}
{% block title %}Export to Excel{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Export Data to Excel</h2>
        <div class="card">
            <div class="card-body">
                <p>Select the data you want to export. All selected data will be exported to a single Excel file with multiple sheets.</p>
                <form method="POST">
                    <div class="mb-3">
                        <h5>Select Data to Export:</h5>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="students" id="students" checked>
                            <label class="form-check-label" for="students">
                                Students (Moodle ID, Roll No, Name, Email, Phone)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="tests" id="tests" checked>
                            <label class="form-check-label" for="tests">
                                Tests (Test ID, Test Name, Created At)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="test_questions" id="test_questions" checked>
                            <label class="form-check-label" for="test_questions">
                                Test Questions (Question ID, Test Name, Question Number, Max Marks)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="marks" id="marks" checked>
                            <label class="form-check-label" for="marks">
                                Student Test Marks (All attempts in same sheet)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="attendance_daily" id="attendance_daily" checked>
                            <label class="form-check-label" for="attendance_daily">
                                Attendance Daily (Moodle ID, Date, Status)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="attendance_percent" id="attendance_percent" checked>
                            <label class="form-check-label" for="attendance_percent">
                                Attendance Percentage (Moodle ID, Percentage)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="faculty" id="faculty">
                            <label class="form-check-label" for="faculty">
                                Faculty (Faculty ID, Username, Role)
                            </label>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success">
                        <i class="bi bi-download"></i> Download Excel File
                    </button>
                    <a href="{{ url_for('admin_dashboard') }}" class="btn btn-secondary">Cancel</a>
                </form>
                <div class="alert alert-info mt-3">
                    <strong>Note:</strong> Moodle ID will be the first column in all sheets. The file will be downloaded with a timestamp in the filename.
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'add_faculty.html': '''{% extends "base.html" %}
{% block title %}Add Faculty{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Add New Faculty</h2>
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Faculty</button>
                    <a href="{{ url_for('view_faculty') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'view_faculty.html': '''{% extends "base.html" %}
{% block title %}View Faculty{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>All Faculty</h2>
    <a href="{{ url_for('add_faculty') }}" class="btn btn-primary">Add New Faculty</a>
</div>

{% if faculty_list %}
<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Faculty ID</th>
                        <th>Username</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for faculty in faculty_list %}
                    <tr>
                        <td>{{ faculty.faculty_id }}</td>
                        <td>{{ faculty.username }}</td>
                        <td>
                            <a href="{{ url_for('delete_faculty', faculty_id=faculty.faculty_id) }}" 
                               class="btn btn-sm btn-danger" 
                               onclick="return confirm('Delete this faculty?')">Delete</a>
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
    No faculty found. <a href="{{ url_for('add_faculty') }}">Add your first faculty</a>
</div>
{% endif %}
{% endblock %}'''
}

# Create static files
css_content = '''/* Custom Styles for Student Performance Analysis and Visualization Dashboard */

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
    font-size: 1.3rem;
}

.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border: none;
    margin-bottom: 1.5rem;
}

.card-header {
    font-weight: 600;
}

.table {
    margin-bottom: 0;
}

.btn {
    border-radius: 0.25rem;
}

.alert {
    border-radius: 0.25rem;
}

.card.text-white h2 {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

.card.text-white .card-title {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.form-label {
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.form-control:focus,
.form-select:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.table-hover tbody tr:hover {
    background-color: rgba(0, 0, 0, 0.03);
}

.badge {
    padding: 0.5em 0.75em;
}

@media (max-width: 768px) {
    .card.text-white h2 {
        font-size: 2rem;
    }
    
    .table-responsive {
        font-size: 0.9rem;
    }
}'''

js_content = '''// Main JavaScript for Student Performance Analysis and Visualization Dashboard

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Form validation helper
function validateMarks(input, maxMarks) {
    const value = parseInt(input.value);
    if (value < 0) {
        input.value = 0;
    } else if (value > maxMarks) {
        input.value = maxMarks;
    }
}'''

print("Generating final templates and static files...")
count = 0

for filename, content in templates.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f"✓ Created {filename}")

# Create CSS file
with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)
print("✓ Created static/css/style.css")

# Create JS file
with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("✓ Created static/js/main.js")

print(f"\n✅ Successfully generated {count} templates + 2 static files!")
print(f"Total templates: 20 (all complete!)")
print("\n🎉 System is now COMPLETE and ready to run!")
print("\nNext steps:")
print("1. mysql -u root -p < database.sql")
print("2. python create_admin.py")
print("3. python app.py")
print("4. Open http://localhost:5000")
