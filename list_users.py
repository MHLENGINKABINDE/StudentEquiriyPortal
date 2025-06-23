#!/usr/bin/env python
"""
List Users Script for DUT Student Grievance Management System

This script prints all users in the database with their details.
"""

import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    """Create a Flask application for database access"""
    app = Flask(__name__)
    os.makedirs('instance', exist_ok=True)
    db_path = os.path.abspath(os.path.join('instance', 'app.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from application.models.models import db
    db.init_app(app)
    return app, db

def main():
    print("\n" + "="*70)
    print("DUT Student Grievance Management System - List Users")
    print("="*70)
    app, db = create_app()
    with app.app_context():
        try:
            from application.models.db_utils import get_all_users
        except ImportError as e:
            print(f"Error importing required modules: {e}")
            print("Make sure you're running this script from the project root directory.")
            sys.exit(1)
        users = get_all_users()
        if not users:
            print("No users found in the database.")
            return
        print(f"\n{'ID':<5} {'Email':<30} {'Display Name':<25} {'Role':<10} {'Created At'}")
        print("-"*90)
        for user in users:
            print(f"{user.id:<5} {user.email:<30} {user.display_name:<25} {user.role:<10} {user.created_at}")
        print(f"\nTotal users: {len(users)}")

if __name__ == "__main__":
    main() 