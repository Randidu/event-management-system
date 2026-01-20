import sys
import os
import logging
from datetime import datetime, timedelta

# Add current directory to sys.path to ensure 'app' module is found
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.core.database import engine, Base, SessionLocal
# Import all models to ensure they are registered with Base.metadata
import app.models 
from app.models.user import User, UserRole
from app.models.event import Event, Category, EventStatus
from app.core.security import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    try:
        # Drop all tables
        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        # Create all tables
        logger.info("Creating all tables...")
        Base.metadata.create_all(bind=engine)
            
        logger.info("Database reset complete.")
        
        # Seed Data
        logger.info("Seeding data...")
        db = SessionLocal()
        try:
            # 1. Create Admin User
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                first_name="System",
                last_name="Admin",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            
            # 2. Create Demo User
            demo_user = User(
                email="user@example.com",
                hashed_password=get_password_hash("user123"),
                first_name="John",
                last_name="Doe",
                role=UserRole.CUSTOMER,
                is_active=True
            )
            db.add(demo_user)
            
            # Flush to get IDs
            db.flush() 
            
            # 3. Create Sample Events
            events = [
                Event(
                    title="Summer Music Festival",
                    description="The biggest summer music festival in the city featuring top artists.",
                    location="City Park Arena",
                    starts_at=datetime.utcnow() + timedelta(days=30),
                    ends_at=datetime.utcnow() + timedelta(days=31),
                    poster_url="https://images.unsplash.com/photo-1459749411177-8c275d8436cd?w=800&q=80",
                    organizer_id=admin_user.id, 
                    capacity=5000,
                    ga_ticket_price=150.0,
                    vip_ticket_price=300.0,
                    pa_ticket_price=500.0,
                    category=Category.CONCERT,
                    status=EventStatus.PUBLISHED
                ),
                Event(
                    title="Tech Conference 2026",
                    description="A gathering of tech enthusiasts and industry leaders.",
                    location="Convention Center",
                    starts_at=datetime.utcnow() + timedelta(days=60),
                    ends_at=datetime.utcnow() + timedelta(days=61),
                    poster_url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80",
                    organizer_id=admin_user.id,
                    capacity=1000,
                    ga_ticket_price=299.0,
                    vip_ticket_price=599.0,
                    category=Category.CONFERENCE,
                    status=EventStatus.PUBLISHED
                ),
                Event(
                    title="Yoga Workshop",
                    description="Morning yoga and meditation session.",
                    location="Zen Garden",
                    starts_at=datetime.utcnow() + timedelta(days=5),
                    ends_at=datetime.utcnow() + timedelta(days=5, hours=4),
                    poster_url="https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&q=80",
                    organizer_id=admin_user.id,
                    capacity=50,
                    ga_ticket_price=20.0,
                    category=Category.WORKSHOP,
                    status=EventStatus.PUBLISHED
                )
            ]
            
            for event in events:
                db.add(event)
            
            db.commit()
            logger.info("Seeding complete! Created Admin (admin@example.com/admin123), Demo User (user@example.com/user123), and 3 Events.")
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise

if __name__ == "__main__":
    reset_database()
