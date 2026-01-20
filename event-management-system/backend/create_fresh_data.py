#!/usr/bin/env python3
"""
Script to recreate database with fresh data including demo users and sample events
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.event import Event, EventStatus, Category
from app.core.security import get_password_hash

def drop_all_tables():
    """Drop all tables"""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("[OK] All tables dropped")

def create_all_tables():
    """Create all tables"""
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] All tables created")

def create_demo_users(db: Session):
    """Create demo users"""
    print("\n" + "="*60)
    print("Creating Demo Users")
    print("="*60)
    
    # Demo Customer User
    demo_user = User(
        email="demo@example.com",
        first_name="Demo",
        last_name="User",
        role=UserRole.CUSTOMER,
        hashed_password=get_password_hash("demo1234"),
        is_active=True
    )
    db.add(demo_user)
    db.commit()
    print("[OK] Demo User: demo@example.com / demo1234 (CUSTOMER)")
    
    # Admin User
    admin_user = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        role=UserRole.ADMIN,
        hashed_password=get_password_hash("admin1234"),
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    print("[OK] Admin User: admin@example.com / admin1234 (ADMIN)")

def create_sample_events(db: Session):
    """Create sample events for testing"""
    print("\n" + "="*60)
    print("Creating Sample Events")
    print("="*60)
    
    # Get the organizer (admin user)
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    
    events_data = [
        {
            "title": "Rock Music Festival 2026",
            "description": "Join us for an amazing rock music festival featuring international and local bands. A full day of non-stop rock music with food stalls and entertainment.",
            "category": Category.CONCERT,
            "location": "Central Park, New York",
            "starts_at": datetime.now() + timedelta(days=15, hours=10),
            "ends_at": datetime.now() + timedelta(days=15, hours=22),
            "capacity": 5000,
            "ga_ticket_price": 50.00,
            "vip_ticket_price": 150.00,
            "pa_ticket_price": 100.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "Jazz Night Concert",
            "description": "Experience smooth jazz music from renowned jazz artists. An intimate evening of live jazz performances in our concert hall.",
            "category": Category.CONCERT,
            "location": "Jazz Hall, Los Angeles",
            "starts_at": datetime.now() + timedelta(days=8, hours=19),
            "ends_at": datetime.now() + timedelta(days=8, hours=23),
            "capacity": 500,
            "ga_ticket_price": 35.00,
            "vip_ticket_price": 85.00,
            "pa_ticket_price": 60.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "EDM Dance Party",
            "description": "High energy electronic dance music event with top DJs. Dance the night away with thousands of music lovers!",
            "category": Category.CONCERT,
            "location": "Downtown Venue, Miami",
            "starts_at": datetime.now() + timedelta(days=5, hours=21),
            "ends_at": datetime.now() + timedelta(days=6, hours=6),
            "capacity": 3000,
            "ga_ticket_price": 45.00,
            "vip_ticket_price": 120.00,
            "pa_ticket_price": 80.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "Classical Symphony Orchestra",
            "description": "The world-renowned symphony orchestra performs Beethoven and Mozart classics. A night of elegant classical music.",
            "category": Category.CONCERT,
            "location": "Concert Hall, Boston",
            "starts_at": datetime.now() + timedelta(days=10, hours=19),
            "ends_at": datetime.now() + timedelta(days=10, hours=21, minutes=30),
            "capacity": 1200,
            "ga_ticket_price": 40.00,
            "vip_ticket_price": 95.00,
            "pa_ticket_price": 70.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "Pop Star Live Performance",
            "description": "See your favorite pop star perform live with all the latest hits. A spectacular show with amazing visuals and performances.",
            "category": Category.CONCERT,
            "location": "Madison Square Garden, New York",
            "starts_at": datetime.now() + timedelta(days=20, hours=18),
            "ends_at": datetime.now() + timedelta(days=20, hours=21),
            "capacity": 20000,
            "ga_ticket_price": 75.00,
            "vip_ticket_price": 200.00,
            "pa_ticket_price": 150.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "Country Music Festival",
            "description": "Multi-day country music festival with top country artists. Experience authentic country music and southern hospitality.",
            "category": Category.CONCERT,
            "location": "Nashville, Tennessee",
            "starts_at": datetime.now() + timedelta(days=25, hours=15),
            "ends_at": datetime.now() + timedelta(days=27, hours=22),
            "capacity": 10000,
            "ga_ticket_price": 60.00,
            "vip_ticket_price": 180.00,
            "pa_ticket_price": 120.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "Hip-Hop Showcase",
            "description": "Showcase of emerging and established hip-hop artists. Discover new talents and enjoy performances from hip-hop legends.",
            "category": Category.CONCERT,
            "location": "Staples Center, Los Angeles",
            "starts_at": datetime.now() + timedelta(days=12, hours=20),
            "ends_at": datetime.now() + timedelta(days=13, hours=2),
            "capacity": 2000,
            "ga_ticket_price": 55.00,
            "vip_ticket_price": 140.00,
            "pa_ticket_price": 95.00,
            "status": EventStatus.PUBLISHED
        },
        {
            "title": "Indie Bands Battle",
            "description": "Battle of the bands featuring local indie artists. Discover incredible indie music from upcoming artists in your area.",
            "category": Category.CONCERT,
            "location": "Local Theater, Chicago",
            "starts_at": datetime.now() + timedelta(days=7, hours=19),
            "ends_at": datetime.now() + timedelta(days=7, hours=23),
            "capacity": 800,
            "ga_ticket_price": 25.00,
            "vip_ticket_price": 60.00,
            "pa_ticket_price": 45.00,
            "status": EventStatus.PUBLISHED
        },
    ]
    
    for idx, event_data in enumerate(events_data, 1):
        event = Event(
            **event_data,
            organizer_id=admin.id
        )
        db.add(event)
        db.commit()
        print(f"[OK] Event {idx}: {event.title}")
    
    print(f"\nTotal events created: {len(events_data)}")

def main():
    """Main function"""
    print("=" * 60)
    print("EMS Database Fresh Setup")
    print("=" * 60)
    
    try:
        # Drop existing tables
        drop_all_tables()
        
        # Create fresh tables
        create_all_tables()
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Create demo users
            create_demo_users(db)
            
            # Create sample events
            create_sample_events(db)
            
            print("\n" + "=" * 60)
            print("[OK] DATABASE SETUP COMPLETE!")
            print("=" * 60)
            print("\nDemo Credentials:")
            print("   Customer: demo@example.com / demo1234")
            print("   Admin: admin@example.com / admin1234")
            print("\nDatabase Contents:")
            print(f"   - Users: 2")
            print(f"   - Events: 8 (ready for testing)")
            print("\n" + "=" * 60)
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
