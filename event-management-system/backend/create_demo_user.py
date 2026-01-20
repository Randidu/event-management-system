#!/usr/bin/env python3
"""
Script to create a demo user in the database
"""
import sys
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_demo_user():
    """Create a demo user for testing"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if demo user already exists
        demo_user = db.query(User).filter(User.email == "demo@example.com").first()
        
        if demo_user:
            print("✓ Demo user already exists!")
            print(f"  Email: {demo_user.email}")
            print(f"  Name: {demo_user.first_name} {demo_user.last_name}")
            print(f"  Role: {demo_user.role}")
            return
        
        # Create demo user with CUSTOMER role
        hashed_password = get_password_hash("demo1234")
        new_user = User(
            email="demo@example.com",
            first_name="Demo",
            last_name="User",
            role=UserRole.CUSTOMER,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✓ Demo user created successfully!")
        print(f"  Email: demo@example.com")
        print(f"  Password: demo1234")
        print(f"  Name: Demo User")
        print(f"  Role: {new_user.role}")
        
    except Exception as e:
        print(f"✗ Error creating demo user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

def create_admin_user():
    """Create an admin user for testing"""
    
    db: Session = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        
        if admin_user:
            print("✓ Admin user already exists!")
            print(f"  Email: {admin_user.email}")
            print(f"  Name: {admin_user.first_name} {admin_user.last_name}")
            print(f"  Role: {admin_user.role}")
            return
        
        # Create admin user
        hashed_password = get_password_hash("admin1234")
        new_user = User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✓ Admin user created successfully!")
        print(f"  Email: admin@example.com")
        print(f"  Password: admin1234")
        print(f"  Name: Admin User")
        print(f"  Role: {new_user.role}")
        
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Creating Demo Users for EMS")
    print("=" * 60)
    create_demo_user()
    print()
    create_admin_user()
    print("=" * 60)
