# Event Management System - Demo Credentials

## Login Test Accounts

### Demo User (CUSTOMER)
- **Email:** demo@example.com
- **Password:** demo1234
- **Role:** CUSTOMER
- **Access:** Can view events, book tickets, manage wishlist

### Admin User (ADMIN)
- **Email:** admin@example.com
- **Password:** admin1234
- **Role:** ADMIN
- **Access:** Admin dashboard and administrative features

## Getting Started

### Backend Setup

1. Navigate to backend directory:
```bash
cd event-management-system/backend
```

2. Create demo users (if not already created):
```bash
python create_demo_user.py
```

3. Start the FastAPI server:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at: `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to frontend templates directory:
```bash
cd event-management-system/frontend
```

2. Open `templates/index.html` in a web browser or serve with Live Server

### Testing the Application

1. Open the frontend in your browser
2. Click "Login" in the navigation bar
3. Use one of the demo credentials above
4. After login:
   - **For CUSTOMER user:** You will see regular user features (events, wishlist, tickets)
   - **For ADMIN user:** You will see the "Admin Panel" button in the dropdown menu

## Key Features Implemented

✅ **Authentication System**
- User registration with role assignment
- Login with JWT tokens
- User role stored in localStorage/sessionStorage
- Token-based API authentication

✅ **Role-Based Access Control**
- Admin panel button only shows for ADMIN users
- Regular users see only relevant options
- Protected routes redirect to login

✅ **User Management**
- New users created with CUSTOMER role by default
- Admin users have additional privileges
- Profile information stored and returned on login

✅ **Wishlist Management**
- Authenticated users can manage their wishlist
- Wishlist page properly checks authentication
- No redirect loops after login

## API Endpoints

### Authentication
- `POST /auth/token` - Login with email and password

### Users
- `GET /users/me` - Get current user info (requires auth)
- `POST /users/` - Create new user (signup)

### Events
- `GET /events/` - Get all events
- `GET /events/{id}` - Get event details

### Wishlist
- `GET /wishlist/` - Get user's wishlist (requires auth)
- `POST /wishlist/` - Add item to wishlist (requires auth)
- `DELETE /wishlist/{event_id}` - Remove from wishlist (requires auth)

## Fixed Issues

1. ✅ **Login Problem** - User role now stored with authentication token
2. ✅ **Admin Panel Visibility** - Only shown to ADMIN users on all pages
3. ✅ **Wishlist Authentication** - Proper auth check without redirect loops
4. ✅ **User Role Assignment** - Default CUSTOMER role for new users
5. ✅ **Demo User Credentials** - Test accounts provided for development

## Troubleshooting

### "Incorrect username or password" error
- Ensure you're using the correct demo credentials
- Check that the backend server is running
- Verify the database has demo users by running: `python create_demo_user.py`

### Admin panel not showing
- Make sure you're logged in with the admin account
- Clear browser cache and localStorage
- Check that `auth.js` is loaded on the page

### CORS errors
- Backend CORS is configured to allow localhost
- Make sure frontend and backend are on the same network

## Database

The application uses PostgreSQL. Make sure:
1. PostgreSQL is running
2. Database connection is configured in `app/core/config.py`
3. Tables are created on first backend startup
