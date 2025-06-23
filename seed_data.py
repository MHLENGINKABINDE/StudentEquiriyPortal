#!/usr/bin/env python
"""
Seed Data Script for DUT Student Grievance Management System (SQLAlchemy)

This script populates the SQLite database with sample data:
- Admin users
- Student users
- Sample grievances in various states

This helps with testing and demonstration purposes.
"""

import os
import sys
import time
import random
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Sample data
DEPARTMENTS = [
    'Academic Administration',
    'Admissions Office',
    'Finance Department',
    'Student Housing',
    'Financial Aid',
    'Faculty of Accounting and Informatics',
    'Faculty of Applied Sciences',
    'Faculty of Arts and Design',
    'Faculty of Engineering and the Built Environment',
    'Faculty of Health Sciences',
    'Faculty of Management Sciences',
]

STATUSES = [
    'pending',
    'in_progress',
    'assigned',
    'under_review',
    'resolved',
    'closed'
]

GRIEVANCE_TITLES = [
    'Registration fee issue',
    'Missing exam results',
    'Course material not available',
    'Accommodation application delay',
    'Financial aid processing delay',
    'Lecturer attendance issues',
    'Library access card problem',
    'Student portal login issues',
    'Incorrect student details',
    'Course enrollment error',
    'Payment receipt not received',
    'Scholarship application status',
    'Parking access problems',
    'Cafeteria service complaint',
    'Computer lab equipment issue',
    'Noise complaints in residence',
    'Wi-Fi connectivity problems',
    'Textbook availability in bookstore',
    'Course schedule conflict',
    'Exam venue concerns'
]

GRIEVANCE_DESCRIPTIONS = [
    'I have been charged incorrectly for my registration fees. The invoice shows a higher amount than what was communicated earlier.',
    'I took my exams last semester but my results for Module X are still not showing on the student portal.',
    'The course materials for Module Y have not been uploaded to the learning platform, making it difficult to prepare for upcoming assessments.',
    'I applied for student housing three months ago but haven\'t received any response yet.',
    'I submitted all required documents for financial aid in January, but my application is still showing as "pending" in the system.',
    'The lecturer for Module Z has missed several classes without any prior notice, affecting our course completion.',
    'My library access card is not working, and I\'ve been unable to check out books for my research project.',
    'I\'ve been experiencing consistent login issues with the student portal and cannot access my academic information.',
    'My student details in the system show an incorrect home address and phone number, which I\'ve tried to update multiple times.',
    'I was enrolled in the wrong course despite selecting the correct one during registration.',
    'I made a payment for my tuition last week but haven\'t received a receipt confirmation yet.',
    'I applied for the University Merit Scholarship two months ago but haven\'t heard back about my application status.',
    'My student card no longer works for parking access, even though my fees are up to date.',
    'The quality of food in the main campus cafeteria has significantly declined, with several instances of undercooked meals.',
    'Several computers in Lab 3 have faulty keyboards and outdated software that hinders our practical work.',
    'The noise levels in Residence Block B are excessive even during examination periods, making it difficult to study.',
    'The Wi-Fi connection in the central library is consistently weak or unavailable, affecting my research capabilities.',
    'The recommended textbooks for Module A are consistently out of stock in the university bookstore.',
    'My new course schedule has two classes overlapping, making it impossible to attend both.',
    'The exam venue for my last assessment was overcrowded, hot, and had poor lighting, affecting my performance.'
]

def create_app():
    """Create a Flask application for database setup"""
    app = Flask(__name__)
    db_path = os.path.abspath(os.path.join('instance', 'app.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from application.models.models import db, Department
    db.init_app(app)
    return app, db, Department

def main():
    print("\n" + "="*70)
    print("WARNING: You are about to seed the database with sample data.")
    print("This will create multiple users and grievances in the system.")
    print("This is intended for testing purposes only.")
    print("="*70)
    confirm = input("\nDo you want to continue? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Database seeding cancelled.")
        sys.exit(0)

    app, db, Department = create_app()
    with app.app_context():
        from application.models.db_utils import create_user, create_grievance, update_grievance_status, get_user_by_email
        from application.models.models import User, Grievance

        # Create admin users
        admin_users = [
            {
                'email': 'admin@dut.ac.za',
                'password': 'Admin@123456',
                'name': 'System Administrator',
                'role': 'admin'
            },
            {
                'email': 'manager@dut.ac.za',
                'password': 'Manager@123456',
                'name': 'Department Manager',
                'role': 'admin'
            }
        ]

        # Create student users
        student_users = [
            {
                'email': 'student1@dut.ac.za',
                'password': 'Student1@123456',
                'name': 'John Smith',
                'role': 'student'
            },
            {
                'email': 'student2@dut.ac.za',
                'password': 'Student2@123456',
                'name': 'Sarah Johnson',
                'role': 'student'
            },
            {
                'email': 'student3@dut.ac.za',
                'password': 'Student3@123456',
                'name': 'Michael Williams',
                'role': 'student'
            },
            {
                'email': 'student4@dut.ac.za',
                'password': 'Student4@123456',
                'name': 'Jessica Brown',
                'role': 'student'
            },
            {
                'email': 'student5@dut.ac.za',
                'password': 'Student5@123456',
                'name': 'David Lee',
                'role': 'student'
            }
        ]

        created_users = {}

        print("\nCreating admin users:")
        for admin in admin_users:
            try:
                user = get_user_by_email(admin['email'])
                if not user:
                    user_id = create_user(admin['email'], admin['password'], admin['name'], admin['role'])
                    created_users[admin['email']] = user_id
                    print(f"  ✅ {admin['name']} ({admin['email']}) created successfully")
                else:
                    created_users[admin['email']] = user.id
                    print(f"  ✓ {admin['name']} ({admin['email']}) already exists")
            except Exception as e:
                print(f"  ❌ Error creating {admin['email']}: {e}")

        print("\nCreating student users:")
        for student in student_users:
            try:
                user = get_user_by_email(student['email'])
                if not user:
                    user_id = create_user(student['email'], student['password'], student['name'], student['role'])
                    created_users[student['email']] = user_id
                    print(f"  ✅ {student['name']} ({student['email']}) created successfully")
                else:
                    created_users[student['email']] = user.id
                    print(f"  ✓ {student['name']} ({student['email']}) already exists")
            except Exception as e:
                print(f"  ❌ Error creating {student['email']}: {e}")

        # Get all departments from the DB
        all_departments = Department.query.all()
        dept_name_to_id = {dept.name: dept.id for dept in all_departments}

        # Create grievances for each student
        print("\nCreating sample grievances:")
        for student in student_users:
            if student['email'] not in created_users:
                continue
            student_id = created_users[student['email']]
            num_grievances = random.randint(2, 5)
            for _ in range(num_grievances):
                title = random.choice(GRIEVANCE_TITLES)
                description = random.choice(GRIEVANCE_DESCRIPTIONS)
                department_name = random.choice(DEPARTMENTS)
                department_id = dept_name_to_id.get(department_name)
                if not department_id:
                    print(f"  ⚠️ Department '{department_name}' not found in DB, skipping grievance.")
                    continue
                try:
                    grievance_id = create_grievance(student_id, title, description, department_id, query_category="General")
                    print(f"  ✅ Grievance '{title}' created for {student['name']}")
                    # Randomly update status for some grievances
                    if random.random() > 0.3:
                        status = random.choice(STATUSES)
                        update_grievance_status(grievance_id, status, note=f"Status updated to {status} (test data)")
                        print(f"    ↪ Status updated to '{status}'")
                except Exception as e:
                    print(f"  ❌ Error creating grievance for {student['email']}: {e}")

        print("\n✅ Database seeding complete!")
        print("\nAdmin credentials:")
        for admin in admin_users:
            print(f"  Email: {admin['email']}")
            print(f"  Password: {admin['password']}")
            print(f"  Role: {admin['role']}")
            print("")
        print("Student credentials:")
        for student in student_users:
            print(f"  Email: {student['email']}")
            print(f"  Password: {student['password']}")
            print("")

if __name__ == "__main__":
    main() 