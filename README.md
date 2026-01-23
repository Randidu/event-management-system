# 🎉 Infinity Events - Event Management System

<div align="center">

![Event Management System](https://img.shields.io/badge/Event-Management-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**A modern, full-featured Event Management System with AI-powered features**

[Features](#-features) • [Installation](#-installation--setup) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Default Credentials](#-default-credentials)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🌟 Overview

**Infinity Events** is a comprehensive Event Management System designed to streamline event discovery, booking, and management. Built with modern web technologies, it offers a seamless experience for both users and administrators with AI-powered features for enhanced productivity.

### Key Highlights

✨ **AI-Powered Features** - Smart search, automated content generation, and intelligent chatbot  
🎨 **Modern UI/UX** - Beautiful, responsive design with smooth animations  
🔐 **Secure Authentication** - OAuth2 with JWT tokens and social login support  
💳 **Payment Integration** - Secure payment processing with receipt generation  
📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile devices  
🌐 **Multi-language Support** - Internationalization ready  

---

## ✨ Features

### 👤 User Features

#### Authentication & Profile
- **Secure Sign Up/Login** - Email-based authentication with password hashing
- **Social Login** - Google and Facebook OAuth integration
- **Password Recovery** - Forgot password with email verification
- **Profile Management** - Update personal information, profile picture, and password
- **Session Management** - Secure JWT-based authentication

#### Event Discovery & Booking
- **Event Browsing** - Browse all available events with advanced filtering
- **Smart Search** - AI-powered natural language search (e.g., "Music events in Colombo tomorrow")
- **Event Details** - Comprehensive event information with image galleries
- **Ticket Booking** - Multiple ticket types (General Admission, VIP, Platinum)
- **Wishlist** - Save favorite events for later
- **Payment Processing** - Secure checkout with multiple payment methods
- **E-Tickets** - Digital tickets with QR codes
- **Booking History** - View all past and upcoming bookings

#### Support & Communication
- **Support Tickets** - Submit and track support requests
- **Live Chat** - AI-powered chatbot for instant assistance
- **Email Notifications** - Booking confirmations and event reminders
- **Ticket Replies** - Two-way communication with support team

### 👨‍💼 Admin Features

#### Dashboard & Analytics
- **Admin Dashboard** - Real-time statistics and insights
- **User Management** - View, edit, and manage user accounts
- **Event Analytics** - Track event performance and bookings
- **Revenue Reports** - Financial overview and transaction history

#### Event Management
- **Create Events** - Rich event creation with AI assistance
  - AI-powered description generation
  - Automatic poster generation
  - Image prompt suggestions
  - Title improvement recommendations
- **Edit Events** - Update event details and settings
- **Delete Events** - Remove events with confirmation
- **Event Categories** - Conference, Workshop, Seminar, Meetup, Music, etc.
- **Capacity Management** - Track available seats and sold tickets

#### AI-Powered Tools
- **AI Description Generator** - Create compelling event descriptions
- **AI Title Improver** - Generate catchy event titles
- **AI Poster Generator** - Automatically create event posters
- **AI Image Prompts** - Get AI image generation prompts
- **Content Moderation** - Automated comment filtering
- **Smart Search** - Intelligent event discovery

#### Support Management
- **Ticket System** - View and respond to user support tickets
- **Priority Management** - Categorize and prioritize tickets
- **Status Tracking** - Monitor ticket resolution progress

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: OAuth2 with JWT (JSON Web Tokens)
- **AI Integration**: 
  - OpenAI GPT-3.5-turbo
  - LangChain for AI workflows
- **Image Processing**: Pillow (PIL)
- **Email**: SMTP integration
- **Validation**: Pydantic v2
- **CORS**: FastAPI CORS middleware

### Frontend
- **Structure**: HTML5 with semantic markup
- **Styling**: Vanilla CSS with modern design patterns
  - CSS Grid & Flexbox
  - CSS Animations & Transitions
  - Custom properties (CSS Variables)
  - Responsive design (Mobile-first)
- **JavaScript**: Vanilla ES6+
  - Async/Await for API calls
  - Fetch API for HTTP requests
  - Local Storage for state management
- **UI Components**: 
  - Bootstrap 5.3.2
  - Bootstrap Icons
  - AOS (Animate On Scroll)
  - Custom cursor effects
  - Interactive animations

### Database Schema
- **Users** - User accounts and authentication
- **Events** - Event information and metadata
- **Bookings** - Ticket purchases and reservations
- **Tickets** - Individual ticket records with QR codes
- **Wishlists** - User saved events
- **Support Tickets** - Customer support system
- **Ticket Replies** - Support conversation threads

---

## 📦 Prerequisites

Before running the project, ensure you have:

- **Python** 3.8 or higher
- **PostgreSQL** 12 or higher (running instance)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **OpenAI API Key** (for AI features)
- **Email SMTP credentials** (for email notifications)

### Optional
- **VS Code** with Live Server extension (for frontend development)
- **Postman** or similar tool (for API testing)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MY-EMS/event-management-system-my
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ems_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration (for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Email Configuration (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret

# Application Settings
FRONTEND_URL=http://localhost:5500
BACKEND_URL=http://localhost:8000
```

**Important Notes:**
- Replace all placeholder values with your actual credentials
- For Gmail SMTP, use an [App Password](https://support.google.com/accounts/answer/185833)
- Keep your `.env` file secure and never commit it to version control

### 3. Database Setup

#### Create PostgreSQL Database
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ems_db;

# Exit PostgreSQL
\q
```

#### Initialize Database Tables
The application will automatically create tables on first run. Start the backend:

```bash
uvicorn main:app --reload
```

Look for the message: `✅ Database tables created successfully!`

#### Seed Demo Data (Optional)

To populate the database with sample data:

```bash
python seed_data.py
```

This will create:
- Default admin user (admin@example.com / admin123)
- Sample events
- Test users

### 4. Frontend Setup

The frontend uses static HTML/CSS/JS files and can be served in multiple ways:

#### Option 1: VS Code Live Server (Recommended)
1. Install the "Live Server" extension in VS Code
2. Right-click on `frontend/templates/index.html`
3. Select "Open with Live Server"
4. The site will open at `http://localhost:5500`

#### Option 2: Python HTTP Server
```bash
cd frontend
python -m http.server 5500
```

#### Option 3: Direct File Access
Simply open `frontend/templates/index.html` in your browser (Note: Some features may not work due to CORS)

#### Configure API Base URL

If your backend runs on a different port, update the API base URL in frontend files:

**File**: `frontend/static/js/auth.js` (and other JS files)
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';  // Update if needed
```

---

## 🎯 Running the Application

### Start Backend Server
```bash
cd backend
uvicorn main:app --reload
```
- API runs at: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Start Frontend
```bash
# Using Live Server (VS Code)
Right-click index.html → Open with Live Server

# Or using Python
cd frontend
python -m http.server 5500
```
- Frontend runs at: `http://localhost:5500`

### Access the Application
- **Homepage**: http://localhost:5500/templates/index.html
- **Admin Panel**: http://localhost:5500/templates/admin/admin_dashboard.html
- **API Documentation**: http://127.0.0.1:8000/docs

---

## 📁 Project Structure

```
event-management-system-my/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── core/                     # Core configurations
│   │   │   ├── database.py          # Database connection & session
│   │   │   ├── security.py          # Authentication & OAuth
│   │   │   └── config.py            # App configuration
│   │   │
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── user.py              # User model
│   │   │   ├── event.py             # Event model
│   │   │   ├── booking.py           # Booking model
│   │   │   ├── ticket.py            # Ticket model
│   │   │   ├── wishlist.py          # Wishlist model
│   │   │   └── support_ticket.py    # Support ticket model
│   │   │
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── user.py              # User schemas
│   │   │   ├── event.py             # Event schemas
│   │   │   ├── booking.py           # Booking schemas
│   │   │   └── ...
│   │   │
│   │   ├── crud/                     # Database Operations
│   │   │   ├── user_crud.py         # User CRUD operations
│   │   │   ├── event_crud.py        # Event CRUD operations
│   │   │   ├── booking_crud.py      # Booking CRUD operations
│   │   │   └── ...
│   │   │
│   │   └── routes/                   # API Endpoints
│   │       ├── auth.py              # Authentication routes
│   │       ├── events.py            # Event routes
│   │       ├── bookings.py          # Booking routes
│   │       ├── admin.py             # Admin routes
│   │       ├── ai.py                # AI-powered features
│   │       └── support.py           # Support ticket routes
│   │
│   ├── uploads/                      # File uploads
│   │   ├── event_posters/           # Event poster images
│   │   ├── profile_pictures/        # User profile pictures
│   │   └── tickets/                 # Generated ticket PDFs
│   │
│   ├── main.py                       # Application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (create this)
│   └── seed_data.py                  # Database seeding script
│
└── frontend/                         # HTML/CSS/JS Frontend
    ├── static/
    │   ├── css/
    │   │   ├── style.css            # Main stylesheet
    │   │   ├── admin.css            # Admin panel styles
    │   │   └── responsive.css       # Responsive design
    │   │
    │   ├── js/
    │   │   ├── auth.js              # Authentication logic
    │   │   ├── api.js               # API client
    │   │   ├── chatbot.js           # Chatbot functionality
    │   │   ├── translations.js      # i18n support
    │   │   └── admin_profile.js     # Admin profile management
    │   │
    │   └── img/                      # Static images
    │       ├── logo.png
    │       ├── hero-bg.jpg
    │       └── ...
    │
    └── templates/                    # HTML Pages
        ├── index.html               # Homepage
        ├── login.html               # Login page
        ├── signup.html              # Registration page
        ├── event_list.html          # Events listing
        ├── event_details.html       # Event details
        ├── payment.html             # Payment checkout
        ├── payment_success.html     # Payment confirmation
        ├── profile.html             # User profile
        ├── wishlist.html            # User wishlist
        ├── ticket_list.html         # User tickets
        ├── support.html             # Support tickets
        ├── about.html               # About page
        ├── contact.html             # Contact page
        │
        └── admin/                    # Admin Panel
            ├── admin_dashboard.html  # Admin dashboard
            ├── create_events.html    # Event creation
            ├── admin_events.html     # Event management
            ├── admin_users.html      # User management
            ├── admin_bookings.html   # Booking management
            └── admin_support.html    # Support management
```

---

## 📚 API Documentation

### Interactive API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `POST /auth/google` - Google OAuth login
- `POST /auth/facebook` - Facebook OAuth login
- `POST /auth/forgot-password` - Request password reset
- `GET /auth/me` - Get current user

#### Events
- `GET /events/` - List all events (with filters)
- `GET /events/{id}` - Get event details
- `POST /events/` - Create event (Admin)
- `PUT /events/{id}` - Update event (Admin)
- `DELETE /events/{id}` - Delete event (Admin)

#### Bookings
- `POST /bookings/` - Create booking
- `GET /bookings/user/{user_id}` - Get user bookings
- `GET /bookings/{id}` - Get booking details
- `DELETE /bookings/{id}` - Cancel booking

#### Wishlist
- `POST /wishlist/` - Add to wishlist
- `GET /wishlist/user/{user_id}` - Get user wishlist
- `DELETE /wishlist/{id}` - Remove from wishlist

#### AI Features
- `POST /ai/chat` - Chatbot conversation
- `POST /ai/generate-description` - Generate event description
- `POST /ai/improve-title` - Improve event title
- `POST /ai/generate-poster` - Generate event poster
- `POST /ai/generate-image-prompt` - Get image generation prompts
- `POST /ai/smart-search` - Natural language search
- `POST /ai/moderate-comment` - Content moderation

#### Support
- `POST /support/tickets` - Create support ticket
- `GET /support/tickets/user/{user_id}` - Get user tickets
- `POST /support/tickets/{id}/reply` - Reply to ticket

#### Admin
- `GET /admin/dashboard` - Dashboard statistics
- `GET /admin/users` - List all users
- `GET /admin/bookings` - List all bookings
- `PUT /admin/users/{id}` - Update user
- `DELETE /admin/users/{id}` - Delete user

---

## 🔑 Default Credentials

### Admin Account
- **Email**: admin@example.com
- **Password**: admin123

### Test User Account
- **Email**: user@example.com
- **Password**: user123

**⚠️ Important**: Change these credentials in production!

---

## 📸 Screenshots

### User Interface

#### Homepage
Beautiful landing page with featured events and smooth animations.

#### Event Listing
Advanced filtering and search capabilities with AI-powered smart search.

#### Event Details
Comprehensive event information with image gallery and booking options.

#### Payment Checkout
Secure payment processing with multiple ticket types.

### Admin Panel

#### Dashboard
Real-time statistics and analytics overview.

#### Event Management
Create and manage events with AI-powered tools.

#### User Management
View and manage all registered users.

---

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution**: Ensure PostgreSQL is running and credentials in `.env` are correct.

#### CORS Error in Browser
```
Access to fetch has been blocked by CORS policy
```
**Solution**: Ensure backend CORS is configured correctly in `main.py` and frontend is served via HTTP server (not file://).

#### AI Features Not Working
```
OpenAI API Key not configured
```
**Solution**: Add your OpenAI API key to `.env` file.

#### Import Errors
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Activate virtual environment and run `pip install -r requirements.txt`.

#### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution**: Kill the process using the port or use a different port:
```bash
uvicorn main:app --reload --port 8001
```

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review backend logs in the terminal
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
5. Ensure all dependencies are installed

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

---

## 📄 License

This project is for **educational and demonstration purposes**.

### Third-Party Libraries
This project uses several open-source libraries. See `requirements.txt` for a complete list.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework for building APIs
- **Bootstrap** - Frontend component library
- **OpenAI** - AI-powered features
- **PostgreSQL** - Robust database system
- **LangChain** - AI workflow orchestration

---

## 📞 Contact & Support

For questions, suggestions, or support:
- **Email**: support@infinityevents.com
- **GitHub Issues**: [Create an issue](https://github.com/your-repo/issues)

---

<div align="center">

**Made with ❤️ by the Infinity Events Team**

⭐ Star this repository if you find it helpful!

</div>
