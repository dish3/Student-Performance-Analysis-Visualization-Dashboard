-- Student Assessment & Test Management System Database Schema
-- Drop database if exists and create fresh
DROP DATABASE IF EXISTS student_assessment_system;
CREATE DATABASE student_assessment_system;
USE student_assessment_system;

-- Students Table (moodle_id as PRIMARY KEY)
CREATE TABLE students (
    moodle_id VARCHAR(20) PRIMARY KEY,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    moodle_email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Faculty Table
CREATE TABLE faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty') NOT NULL DEFAULT 'faculty'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tests Table
CREATE TABLE tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Test Questions Table
CREATE TABLE test_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    test_id INT NOT NULL,
    question_number INT NOT NULL,
    max_marks INT NOT NULL,
    FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
    UNIQUE KEY unique_test_question (test_id, question_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Student Test Marks Table (with attempt support)
CREATE TABLE student_test_marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    moodle_id VARCHAR(20) NOT NULL,
    test_id INT NOT NULL,
    attempt_no INT NOT NULL DEFAULT 1,
    question_id INT NOT NULL,
    obtained_marks INT NOT NULL DEFAULT 0,
    FOREIGN KEY (moodle_id) REFERENCES students(moodle_id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES test_questions(question_id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_test_attempt_question (moodle_id, test_id, attempt_no, question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Attendance Daily Table
CREATE TABLE attendance_daily (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    moodle_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (moodle_id) REFERENCES students(moodle_id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_date (moodle_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Attendance Percentage Table
CREATE TABLE attendance_percentage (
    moodle_id VARCHAR(20) PRIMARY KEY,
    attendance_percent FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY (moodle_id) REFERENCES students(moodle_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- No sample data - all data will be entered manually
