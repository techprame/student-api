"""Fill the database with demo data for a presentation.

Usage:  python seed.py
Safe to run more than once: existing records are skipped.
"""
from app import models
from app.database import Base, SessionLocal, engine
from app.utils.security import hash_password

DEMO_USER = ("demo@school.com", "demo12345")

STUDENTS = [
    ("Aarav Sharma", "aarav@school.com", 16, "Computer Science"),
    ("Diya Patel", "diya@school.com", 15, "Mathematics"),
    ("Kabir Singh", "kabir@school.com", 17, "Physics"),
    ("Ananya Gupta", "ananya@school.com", 16, "Biology"),
    ("Rohan Verma", "rohan@school.com", 15, "Computer Science"),
]

PRODUCTS = [
    ("Notebook", 50.0, 200),
    ("Geometry Box", 120.0, 75),
    ("School Bag", 899.0, 20),
    ("Calculator", 650.0, 35),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        email, password = DEMO_USER
        if not db.query(models.User).filter_by(email=email).first():
            db.add(models.User(email=email, hashed_password=hash_password(password)))

        for name, email, age, course in STUDENTS:
            if not db.query(models.Student).filter_by(email=email).first():
                db.add(models.Student(name=name, email=email, age=age, course=course))

        for name, price, stock in PRODUCTS:
            if not db.query(models.Product).filter_by(name=name).first():
                db.add(models.Product(name=name, price=price, stock=stock))

        db.commit()
    finally:
        db.close()

    print("Demo data ready.")
    print(f"Login with  email: {DEMO_USER[0]}  password: {DEMO_USER[1]}")


if __name__ == "__main__":
    seed()
