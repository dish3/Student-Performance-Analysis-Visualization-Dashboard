"""
Generate remaining templates for Student Performance Analysis and Visualization Dashboard
"""

import os

os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

templates = {
    'create_test.html': '''{% extends "base.html" %}
{% block title %}Create Test{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2 class="mb-4">Create New Test</h2>
        <div class="card">
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="test_name" class="form-label">Test Name</label>
                        <input type="text" class="form-control" id="test_name" name="test_name" 
                               placeholder="e.g., Unit Test 1, Mid-Term, Final Exam" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Create Test & Add Questions</button>
                    <a href="{{ url_for('view_tests') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'add_test_questions.html': '''{% extends "base.html" %}
{% block title %}Add Test Questions{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-10">
        <h2 class="mb-4">Add Questions for: {{ test.test_name }}</h2>
        
        {% if step == 1 %}
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Step 1: Enter Number of Questions</h5>
                <form method="POST">
                    <div class="mb-3">
                        <label for="num_questions" class="form-label">Total Number of Questions</label>
                        <input type="number" class="form-control" id="num_questions" name="num_questions" 
                               min="1" max="100" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Next: Enter Max Marks</button>
                    <a href="{{ url_for('view_tests') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
        {% elif step == 2 %}
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Step 2: Enter Maximum Marks for Each Question</h5>
                <form method="POST">
                    <input type="hidden" name="num_questions" value="{{ num_questions }}">
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead class="table-light">
                                <tr>
                                    <th>Question Number</th>
                                    <th>Maximum Marks</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for i in range(1, num_questions + 1) %}
                                <tr>
                                    <td>Question {{ i }}</td>
                                    <td>
                                        <input type="number" class="form-control" name="max_marks_{{ i }}" 
                                               min="1" max="100" required>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    <button type="submit" class="btn btn-success">Save All Questions</button>
                    <a href="{{ url_for('view_tests') }}" class="btn btn-secondary">Cancel</a>
                </form>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}''',

    'view_tests.html': '''{% extends "base.html" %}
{% block title %}View Tests{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>All Tests</h2>
    <a href="{{ url_for('create_test') }}" class="btn btn-primary">Create New Test</a>
</div>

{% if tests %}
<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Test ID</th>
                        <th>Test Name</th>
                        <th>Questions</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for test in tests %}
                    <tr>
                        <td>{{ test.test_id }}</td>
                        <td>{{ test.test_name }}</td>
                        <td>{{ test.num_questions }}</td>
                        <td>{{ test.created_at.strftime('%Y-%m-%d %H:%M') if test.created_at else 'N/A' }}</td>
                        <td>
                            <a href="{{ url_for('view_test_details', test_id=test.test_id) }}" class="btn btn-sm btn-info">Details</a>
                            <a href="{{ url_for('test_analysis', test_id=test.test_id) }}" class="btn btn-sm btn-success">Analysis</a>
                            {% if test.num_questions == 0 %}
                            <a href="{{ url_for('add_test_questions', test_id=test.test_id) }}" class="btn btn-sm btn-warning">Add Questions</a>
                            {% endif %}
                            <a href="{{ url_for('delete_test', test_id=test.test_id) }}" 
                               class="btn btn-sm btn-danger" 
                               onclick="return confirm('Delete this test?')">Delete</a>
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
    No tests found. <a href="{{ url_for('create_test') }}">Create your first test</a>
</div>
{% endif %}
{% endblock %}''',

    'view_test_details.html': '''{% extends "base.html" %}
{% block title %}Test Details{% endblock %}
{% block content %}
<div class="mb-4">
    <a href="{{ url_for('view_tests') }}" class="btn btn-secondary">&larr; Back to Tests</a>
</div>

<div class="card">
    <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Test Details: {{ test.test_name }}</h4>
    </div>
    <div class="card-body">
        <p><strong>Test ID:</strong> {{ test.test_id }}</p>
        <p><strong>Created:</strong> {{ test.created_at.strftime('%Y-%m-%d %H:%M') if test.created_at else 'N/A' }}</p>
        
        <h5 class="mt-4">Questions</h5>
        {% if questions %}
        <div class="table-responsive">
            <table class="table table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>Question Number</th>
                        <th>Maximum Marks</th>
                    </tr>
                </thead>
                <tbody>
                    {% for q in questions %}
                    <tr>
                        <td>Question {{ q.question_number }}</td>
                        <td>{{ q.max_marks }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot class="table-secondary">
                    <tr>
                        <th>Total</th>
                        <th>{{ questions|sum(attribute='max_marks') }}</th>
                    </tr>
                </tfoot>
            </table>
        </div>
        {% else %}
        <div class="alert alert-warning">
            No questions added yet. <a href="{{ url_for('add_test_questions', test_id=test.test_id) }}">Add questions</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}''',

    'enter_marks.html': '''{% extends "base.html" %}
{% block title %}Enter Marks{% endblock %}
{% block content %}
<h2 class="mb-4">Enter Student Marks</h2>

{% if step == 1 %}
<div class="card">
    <div class="card-body">
        <h5 class="card-title">Step 1: Select Test, Student, and Attempt</h5>
        <form method="POST">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="test_id" class="form-label">Select Test</label>
                    <select class="form-select" id="test_id" name="test_id" required>
                        <option value="">-- Choose Test --</option>
                        {% for test in tests %}
                        <option value="{{ test.test_id }}">{{ test.test_name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="moodle_id" class="form-label">Select Student</label>
                    <select class="form-select" id="moodle_id" name="moodle_id" required>
                        <option value="">-- Choose Student --</option>
                        {% for student in students %}
                        <option value="{{ student.moodle_id }}">{{ student.moodle_id }} - {{ student.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4 mb-3">
                    <label for="attempt_no" class="form-label">Attempt Number</label>
                    <input type="number" class="form-control" id="attempt_no" name="attempt_no" 
                           min="1" value="1" required>
                    <div class="form-text">Enter attempt number (1, 2, 3...)</div>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Next: Enter Marks</button>
        </form>
    </div>
</div>
{% elif step == 2 %}
<div class="card">
    <div class="card-body">
        <h5 class="card-title">Step 2: Enter Marks for Each Question</h5>
        <div class="alert alert-info">
            <strong>Test:</strong> {{ test.test_name }}<br>
            <strong>Student:</strong> {{ student.moodle_id }} - {{ student.name }}<br>
            <strong>Attempt:</strong> #{{ attempt_no }}
            {% if attempts %}
            <br><strong>Previous Attempts:</strong> {{ attempts|join(', ') }}
            {% endif %}
        </div>
        <form method="POST">
            <input type="hidden" name="test_id" value="{{ test.test_id }}">
            <input type="hidden" name="moodle_id" value="{{ student.moodle_id }}">
            <input type="hidden" name="attempt_no" value="{{ attempt_no }}">
            <input type="hidden" name="submit_marks" value="1">
            
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>Question Number</th>
                            <th>Maximum Marks</th>
                            <th>Obtained Marks</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for question in questions %}
                        <tr>
                            <td>Question {{ question.question_number }}</td>
                            <td>{{ question.max_marks }}</td>
                            <td>
                                <input type="number" class="form-control" 
                                       name="obtained_marks_{{ question.question_id }}" 
                                       min="0" max="{{ question.max_marks }}" 
                                       value="{{ existing_marks.get(question.question_id, 0) }}" 
                                       required>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <button type="submit" class="btn btn-success">Save Marks</button>
            <a href="{{ url_for('enter_marks') }}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{% endif %}
{% endblock %}''',

    'view_marks.html': '''{% extends "base.html" %}
{% block title %}View Marks{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>All Student Marks</h2>
    <a href="{{ url_for('enter_marks') }}" class="btn btn-primary">Enter New Marks</a>
</div>

{% if records %}
<div class="card">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Moodle ID</th>
                        <th>Roll No</th>
                        <th>Name</th>
                        <th>Test</th>
                        <th>Attempt</th>
                        <th>Obtained</th>
                        <th>Maximum</th>
                        <th>Percentage</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                    <tr>
                        <td>{{ record.moodle_id }}</td>
                        <td>{{ record.roll_no }}</td>
                        <td>{{ record.name }}</td>
                        <td>{{ record.test_name }}</td>
                        <td>{{ record.attempt_no }}</td>
                        <td>{{ record.total_obtained }}</td>
                        <td>{{ record.total_max }}</td>
                        <td>
                            <span class="badge {% if record.percentage >= 40 %}bg-success{% else %}bg-danger{% endif %}">
                                {{ record.percentage }}%
                            </span>
                        </td>
                        <td>
                            <a href="{{ url_for('view_marks_detail', moodle_id=record.moodle_id, test_id=record.test_id, attempt_no=record.attempt_no) }}" 
                               class="btn btn-sm btn-info">Details</a>
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
    No marks records found. <a href="{{ url_for('enter_marks') }}">Enter marks for students</a>
</div>
{% endif %}
{% endblock %}''',

    'view_marks_detail.html': '''{% extends "base.html" %}
{% block title %}Marks Detail{% endblock %}
{% block content %}
<div class="mb-4">
    <a href="{{ url_for('view_marks') }}" class="btn btn-secondary">&larr; Back to All Marks</a>
</div>

<div class="card">
    <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Detailed Marks Report</h4>
    </div>
    <div class="card-body">
        <div class="row mb-4">
            <div class="col-md-6">
                <p><strong>Moodle ID:</strong> {{ student.moodle_id }}</p>
                <p><strong>Roll No:</strong> {{ student.roll_no }}</p>
                <p><strong>Name:</strong> {{ student.name }}</p>
                <p><strong>Email:</strong> {{ student.moodle_email }}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Test:</strong> {{ test.test_name }}</p>
                <p><strong>Attempt Number:</strong> {{ attempt_no }}</p>
                <p><strong>Test Date:</strong> {{ test.created_at.strftime('%Y-%m-%d') if test.created_at else 'N/A' }}</p>
            </div>
        </div>

        <div class="table-responsive">
            <table class="table table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>Question Number</th>
                        <th>Maximum Marks</th>
                        <th>Obtained Marks</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {% for mark in marks_detail %}
                    <tr>
                        <td>Question {{ mark.question_number }}</td>
                        <td>{{ mark.max_marks }}</td>
                        <td>{{ mark.obtained_marks or 0 }}</td>
                        <td>
                            {% set q_percentage = ((mark.obtained_marks or 0) / mark.max_marks * 100) | round(2) %}
                            <span class="badge {% if q_percentage >= 40 %}bg-success{% else %}bg-danger{% endif %}">
                                {{ q_percentage }}%
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot class="table-secondary">
                    <tr>
                        <th>Total</th>
                        <th>{{ total_max }}</th>
                        <th>{{ total_obtained }}</th>
                        <th>
                            <span class="badge {% if percentage >= 40 %}bg-success{% else %}bg-danger{% endif %} fs-6">
                                {{ percentage }}%
                            </span>
                        </th>
                    </tr>
                </tfoot>
            </table>
        </div>

        <div class="alert {% if percentage >= 40 %}alert-success{% else %}alert-danger{% endif %} mt-3">
            <strong>Result:</strong> {% if percentage >= 40 %}PASS{% else %}FAIL{% endif %}
        </div>
    </div>
</div>
{% endblock %}'''
}

print("Generating more templates...")
count = 0

for filename, content in templates.items():
    filepath = os.path.join('templates', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    print(f"✓ Created {filename}")

print(f"\n✅ Successfully generated {count} more templates!")
print(f"Total templates so far: {6 + count}")
