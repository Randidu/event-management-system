# Event Management System (MY-EMS)

A full-featured Event Management System built with **FastAPI** (Backend) and **Vanilla HTML/CSS/JS** (Frontend). This application allows users to browse events, book tickets, manage their profiles, and interact with a support system. It also includes a comprehensive Admin Dashboard for managing events, users, and system data.

## Features

### User Features
- **Authentication**: Secure Login, Sign Up, and Password Reset functionality.
- **Event Discovery**: Browse events, search, and view detailed event information.
- **Booking System**: Purchase tickets with a secure checkout flow (Demo Payment).
- **Wishlist**: Save events to a personal wishlist for later.
- **User Dashboard**: 
  - Manage personal profile and password.
  - View booking history and download tickets.
- **Support System**: Submit support tickets and communicate with admins via a reply system.

### Admin Features
- **Dashboard**: Overview of system statistics (Users, Events, Bookings).
- **Event Management**: Create, update, and delete events.
- **User Management**: View and manage registered users.
- **Support Management**: View and reply to user support tickets.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Authentication**: OAuth2 with JWT (JSON Web Tokens)
- **Validation**: Pydantic

### Frontend
- **Structure**: HTML5
- **Styling**: Vanilla CSS (Custom Responsive Design)
- **Logic**: Vanilla JavaScript
- **Icons**: FontAwesome / Ionicons

### Database
- **Primary**: PostgreSQL (via `psycopg2-binary`)

## Prerequisites

Before running the project, ensure you have the following installed:
- **Python** (3.8 or higher)
- **PostgreSQL** (Active local instance)
- **Git**

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd MY-EMS/event-management-system-my
```

### 2. Backend Setup
Navigate to the backend directory and set up the Python environment.

```bash
cd backend
```

**Create a virtual environment:**
```bash
python -m venv venv
```

**Activate the virtual environment:**
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Environment Configuration:**
Create a `.env` file in the `backend/` directory or ensure the `database.py` is configured to point to your local PostgreSQL instance.

Example `.env` (if applicable):
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
*Note: If no `.env` is used, check `app/core/database.py` for connection strings.*

### 3. Database Setup
The application uses SQLAlchemy to automatically create tables on startup.
Ensure your PostgreSQL server is running and you have created a database (e.g., `ems_db`).

Run the backend to initialize tables:
```bash
uvicorn main:app --reload
```
*Check the console output for "Database tables created successfully!".*

### 4. Frontend Setup
The frontend is built with static HTML/JS files.
- You can run it using **Live Server** (VS Code Extension) or simply open `frontend/templates/index.html` in your browser.
- For the best experience (API calls), serving via a local server (like Live Server running on port 5500 or 5501) is recommended to avoid CORS issues if not configured for file protocol.

**Update API Base URL:**
If your backend runs on a different port than `8000`, check `frontend/static/js/` files (like `auth.js` or `api.js`) to ensure the `API_BASE_URL` points to the correct backend URL (default: `http://localhost:8000`).

## Running the Application

1.  **Start the Backend:**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    The API will run at `http://127.0.0.1:8000`.

2.  **Start the Frontend:**
    Open `frontend/templates/index.html` via Live Server.

3.  **Access API Documentation:**
    Go to `http://127.0.0.1:8000/docs` to see the interactive Swagger UI for testing API endpoints.

## Project Structure

```
event-management-system-my/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── core/           # Config & Database setup
│   │   ├── crud/           # Database operations
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── routes/         # API Endpoints
│   │   └── schemas/        # Pydantic Schemas
│   ├── uploads/            # Static file uploads (Images)
│   ├── main.py             # Application Entry Point
│   └── requirements.txt    # Python Dependencies
│
└── frontend/               # HTML/CSS/JS Frontend
    ├── static/
    │   ├── css/            # Stylesheets
    │   ├── js/             # Client-side Logic
    │   └── images/         # Assets
    └── templates/          # HTML Pages (Admin & User)
```

## 📜 License
This project is for educational and demonstration purposes.

---
**Happy Coding!** 
