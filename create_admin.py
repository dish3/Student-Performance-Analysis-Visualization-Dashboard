"""
Script to create admin account for Student Performance Analysis and Visualization Dashboard
Run this after setting up the database
"""

from werkzeug.security import generate_password_hash
import os
import mysql.connector


def get_env(*names, default=None):
    """Return the first non-empty environment variable from names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


DB_CONFIG = {
    'host': get_env('DB_HOST', 'MYSQL_HOST', default='localhost'),
    'port': int(get_env('DB_PORT', 'MYSQL_PORT', default='3306')),
    'user': get_env('DB_USER', 'MYSQL_USER', default='root'),
    'password': get_env('DB_PASSWORD', 'MYSQL_PASSWORD', default='root'),
    'database': get_env(
        'DB_NAME', 'MYSQL_DATABASE', 'MYSQL_DB',
        default='student_assessment_system'
    )
}

def create_admin():
    print("=== Create Admin Account ===\n")
    
    username = input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
    
    password = input("Enter admin password: ").strip()
    if not password:
        print("Password cannot be empty!")
        return
    
    try:
        # Connect to database
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT username FROM faculty WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"\nError: Username '{username}' already exists!")
            cursor.close()
            db.close()
            return
        
        # Hash password and insert admin
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO faculty (username, password, role) VALUES (%s, %s, 'admin')",
            (username, hashed_password)
        )
        db.commit()
        
        print(f"\n✓ Admin account created successfully!")
        print(f"Username: {username}")
        print(f"You can now login with these credentials.")
        
        cursor.close()
        db.close()
        
    except mysql.connector.Error as e:
        print(f"\nDatabase error: {e}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == '__main__':
    create_admin()
