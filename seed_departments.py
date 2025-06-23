import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DUT Departments organized by faculty
DUT_DEPARTMENTS = {
    "Faculty of Accounting and Informatics": [
        {
            "name": "Department of Information Technology",
            "description": "Offers programs in Software Development, Networks, and Information Systems"
        },
        {
            "name": "Department of Financial Accounting",
            "description": "Provides education in accounting, taxation, and financial management"
        }
    ],
    "Faculty of Applied Sciences": [
        {
            "name": "Department of Biotechnology and Food Technology",
            "description": "Focuses on biotechnology, food processing, and related research"
        },
        {
            "name": "Department of Chemistry",
            "description": "Offers programs in analytical, organic, and industrial chemistry"
        }
    ],
    "Faculty of Arts and Design": [
        {
            "name": "Department of Visual Communication Design",
            "description": "Covers graphic design, multimedia, and visual arts"
        },
        {
            "name": "Department of Fashion and Textiles",
            "description": "Focuses on fashion design, textile technology, and clothing management"
        }
    ],
    "Faculty of Engineering": [
        {
            "name": "Department of Mechanical Engineering",
            "description": "Offers programs in mechanical, industrial, and mechatronic engineering"
        },
        {
            "name": "Department of Civil Engineering",
            "description": "Focuses on structural, environmental, and construction engineering"
        }
    ],
    "Faculty of Health Sciences": [
        {
            "name": "Department of Nursing",
            "description": "Provides education in nursing and healthcare management"
        },
        {
            "name": "Department of Emergency Medical Care",
            "description": "Focuses on emergency medical services and paramedic training"
        }
    ],
    "Faculty of Management Sciences": [
        {
            "name": "Department of Public Management",
            "description": "Offers programs in public administration and governance"
        },
        {
            "name": "Department of Marketing and Retail",
            "description": "Focuses on marketing, retail management, and business strategy"
        }
    ],
    "Support Services": [
        {
            "name": "Student Housing",
            "description": "Manages student accommodation and residential life"
        },
        {
            "name": "Student Counselling",
            "description": "Provides mental health support and counselling services"
        },
        {
            "name": "Financial Aid Office",
            "description": "Handles student financial aid, bursaries, and scholarships"
        },
        {
            "name": "Academic Administration",
            "description": "Manages student records, registration, and academic processes"
        },
        {
            "name": "Library Services",
            "description": "Provides access to academic resources and research materials"
        }
    ]
}

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
    print("DUT Department Seeding Script (SQLAlchemy)")
    print("="*70)
    app, db, Department = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        total_added = 0
        for faculty, departments in DUT_DEPARTMENTS.items():
            print(f"\nSeeding departments for {faculty}:")
            for dept in departments:
                # Check if department already exists
                existing = Department.query.filter_by(name=dept["name"]).first()
                if existing:
                    print(f"  ✓ {dept['name']} (already exists)")
                    continue
                new_dept = Department(name=dept["name"], description=dept["description"])
                db.session.add(new_dept)
                print(f"  + {dept['name']}")
                total_added += 1
        db.session.commit()
        print(f"\nSeeding complete! Added {total_added} new departments.")

if __name__ == "__main__":
    main() 