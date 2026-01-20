"""
Create tables and seed admin user
Run with: python init_db.py
"""
from app.core.database import Base, engine, SessionLocal
from app.models.user import User, UserRole
from app.models.event import Event
from app.models.booking import Booking
from app.models.wishlist import WishlistItem
from app.models.ticket import Ticket, TicketComment
from app.core.security import get_password_hash
from datetime import datetime

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")

db = SessionLocal()

try:
    # Check if admin exists
    existing = db.query(User).filter(User.email == "admin@demo.com").first()
    if existing:
        print("\n✅ Admin user already exists!")
    else:
        # Create admin
        admin = User(
            email="admin@demo.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        
        # Create demo users
        for i, (fname, lname) in enumerate([("John", "Doe"), ("Jane", "Smith"), ("Bob", "Johnson")], 1):
            user = User(
                email=f"user{i}@demo.com",
                hashed_password=get_password_hash("user123"),
                first_name=fname,
                last_name=lname,
                role=UserRole.CUSTOMER,
                is_active=True
            )
            db.add(user)
        
        db.commit()
        print("\n✅ Users created successfully!")
    
    print("\n" + "=" * 50)
    print("Demo Credentials:")
    print("=" * 50)
    print("Admin: admin@demo.com / admin123")
    print("User1: user1@demo.com / user123")
    print("User2: user2@demo.com / user123")
    print("User3: user3@demo.com / user123")
    print("=" * 50)
    print("\n🎉 Database is ready! You can now login.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
