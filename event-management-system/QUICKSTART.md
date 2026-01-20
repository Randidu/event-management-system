# Quick Start Guide

## 🚀 Getting Started with EMS

### Backend Setup (One Time)

```bash
# Navigate to backend directory
cd event-management-system/backend

# Create demo users (first time only)
python create_demo_user.py

# Start the server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: **http://127.0.0.1:8000**

### Frontend Setup

```bash
# Navigate to frontend
cd event-management-system/frontend

# Open index.html in browser
# You can use Live Server extension in VS Code
# Or open directly: file:///path/to/frontend/templates/index.html
```

---

## 📝 Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Customer | demo@example.com | demo1234 |
| Admin | admin@example.com | admin1234 |

---

## ✅ What to Test

### 1. **Customer Login Test**
```
1. Click "Login"
2. Enter: demo@example.com / demo1234
3. Click "Sign In"
✓ Should redirect to home page
✓ User dropdown should appear
✓ "Admin Panel" should NOT be visible
✓ Can click "My Wishlist" and view empty wishlist
```

### 2. **Admin Login Test**
```
1. Click "Login"
2. Enter: admin@example.com / admin1234
3. Click "Sign In"
✓ Should redirect to home page
✓ User dropdown should appear
✓ "Admin Panel" SHOULD be visible in dropdown
```

### 3. **Wishlist Test**
```
1. Login as demo user
2. Click on any event
3. Add to wishlist (if button exists)
4. Go to Wishlist page
✓ Should show wishlist items
✓ Should NOT redirect to login
```

### 4. **Logout Test**
```
1. Click on user avatar in top right
2. Click "Logout"
✓ Should redirect to home page
✓ User dropdown should disappear
✓ Login/Signup buttons should reappear
```

---

## 🔧 Common Issues & Solutions

### "Incorrect username or password"
- ✓ Check spelling of email
- ✓ Ensure backend is running
- ✓ Try creating users: `python create_demo_user.py`

### Admin panel not showing for admin user
- ✓ Clear browser cache (Ctrl+Shift+Delete)
- ✓ Clear localStorage in console: `localStorage.clear()`
- ✓ Refresh page (Ctrl+F5)

### Wishlist redirects to login
- ✓ Make sure you're logged in first
- ✓ Check browser console for errors
- ✓ Verify token is stored: Open console → `localStorage.getItem('access_token')`

### Backend not starting
- ✓ Check PostgreSQL is running
- ✓ Check port 8000 is not in use
- ✓ Install missing packages: `pip install -r requirements.txt`

---

## 📱 Frontend Pages

| Page | URL | Auth Required |
|------|-----|---|
| Home | index.html | No |
| Events | event_list.html | No |
| Event Details | event_details.html | No |
| My Tickets | ticket_list.html | Yes |
| Wishlist | wishlist.html | Yes |
| Profile | profile.html | Yes |
| Login | login.html | No |
| Signup | signup.html | No |

---

## 🔑 Key Files to Know

### Backend
- `main.py` - FastAPI entry point
- `app/routes/auth.py` - Login/token endpoints
- `app/core/security.py` - JWT and password handling
- `create_demo_user.py` - Create test users

### Frontend
- `static/js/auth.js` - Authentication logic
- `templates/login.html` - Login form
- `templates/index.html` - Home page

---

## 📊 API Quick Reference

### Login
```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo1234"
```

### Get Current User
```bash
curl -X GET http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Wishlist
```bash
curl -X GET http://127.0.0.1:8000/wishlist/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 💡 Tips

- Keep backend terminal open to see live logs
- Use browser DevTools Console to debug
- Check Network tab to see API requests/responses
- Use `localStorage.getItem('access_token')` to check token
- Use `localStorage.getItem('user')` to check user data

---

**Ready to go! Start with the Backend Setup above.** 🎉
