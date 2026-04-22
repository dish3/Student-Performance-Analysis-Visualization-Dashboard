"""
Script to create admin account for Student Performance Analysis and Visualization Dashboard
Run this after setting up the database
"""

from werkzeug.security import generate_password_hash
import mysql.connector
from config import DB_CONFIG

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
