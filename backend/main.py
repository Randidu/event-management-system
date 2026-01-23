from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.routes import events, auth, wishlist, support, admin, booking, ai
from app.routes import user_router as User
from app.core.database import Base, engine
from app.models.event import Event

app = FastAPI(
    title="EMS Backend",
    version="1.0.0",
    description="Event Management System API"
)

# CORS Middleware
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
        "http://localhost:5502",
        "http://127.0.0.1:5502",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
upload_dir = BASE_DIR / "uploads"
event_posters_dir = upload_dir / "event_posters"
event_posters_dir.mkdir(parents=True, exist_ok=True)


app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

@app.on_event("startup")
def startup_event():
    print("=" * 50)
    print("Starting EMS Backend..............")
    print("=" * 50)
    print("Creating database tables............")
    Base.metadata.create_all(bind=engine)
    print(" Database tables created successfully!")
    print(f"Upload directory: {event_posters_dir.absolute()}")
    print("=" * 50)


app.include_router(events.router)
app.include_router(User.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(wishlist.router)
app.include_router(support.router)
app.include_router(admin.router)
app.include_router(booking.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to EMS API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "upload_directory": str(event_posters_dir.absolute())
    }