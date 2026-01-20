"""
Debug script to reproduce login 500 error - EXACT FLOW
"""
from app.core.database import SessionLocal
from app.crud.user_crud import get_user_by_email
from app.core.security import verify_password, create_access_token
from datetime import timedelta
import traceback
import sys

# Force output to utf-8 to avoid encoding errors in windows terminal
sys.stdout.reconfigure(encoding='utf-8')

def log(msg):
    print(msg)
    with open("debug_crash.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def test_login_crash():
    log("--- Starting Debug ---")
    db = SessionLocal()
    try:
        # 1. Get User
        log("1. Fetching user...")
        user = get_user_by_email(db, "admin@demo.com")
        if not user:
            log("❌ User not found")
            return
        log(f"✅ User found: {user.email}")
        log(f"   Hashed Password in DB: {user.hashed_password}")

        # 2. Verify Password
        log("2. Verifying password 'admin123'...")
        is_valid = verify_password("admin123", user.hashed_password)
        log(f"✅ Verification result: {is_valid}")

        # 3. Create Token
        log("3. Creating access token...")
        access_token_expires = timedelta(minutes=30)
        token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        log(f"✅ Token created: {token}")

    except Exception:
        log("\n❌ CRASH DETECTED:")
        log(traceback.format_exc())
    finally:
        db.close()

if __name__ == "__main__":
    test_login_crash()
