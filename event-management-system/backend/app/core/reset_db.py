from app.core.database import Base, engine
from app.models.user import User
from app.models.event import Event

def reset_database():
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() == 'yes':
        print("🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("📦 Creating all tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database reset complete!")
    else:
        print("❌ Cancelled")

if __name__ == "__main__":
    reset_database()