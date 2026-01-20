/**
 * Authentication Helper Functions
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

// Check if user is logged in
function checkAuth() {
    return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
}

// Get user from localStorage or sessionStorage
function getUser() {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Refresh user profile from server to ensure fresh data (like profile image)
async function refreshUserProfile() {
    const token = checkAuth();
    if (!token) return;

    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const userData = await response.json();
            // Update storage with fresh data
            if (localStorage.getItem('user')) {
                localStorage.setItem('user', JSON.stringify(userData));
            }
            if (sessionStorage.getItem('user')) {
                sessionStorage.setItem('user', JSON.stringify(userData));
            }
            // Update UI with new data
            updateAuthUI();
        }
    } catch (e) {
        console.error("Failed to refresh user profile", e);
    }
}

// Update UI based on auth state
function updateAuthUI() {
    const token = checkAuth();
    const guestNav = document.getElementById('guest-nav');
    const authNav = document.getElementById('auth-nav');

    if (token) {
        if (guestNav) guestNav.style.display = 'none';
        if (authNav) authNav.style.display = 'block';

        // Update user avatar if available
        const user = getUser();
        if (user) {
            // Update profile image
            let imgUrl = `https://i.pravatar.cc/40?u=${user.email || 'guest'}`; // Default

            if (user.profile_image) {
                // Check if it's an absolute URL
                if (user.profile_image.startsWith('http')) {
                    imgUrl = user.profile_image;
                } else {
                    // Safe URL construction for local uploads
                    const cleanPath = user.profile_image.replace(/\\/g, '/').replace(/^\/+/, '');
                    imgUrl = `${API_BASE_URL}/${cleanPath}`;
                }
                // Add timestamp to force refresh (cache busting)
                imgUrl += `?t=${Date.now()}`;
            }

            document.querySelectorAll('.user-avatar').forEach(img => {
                // Only update user avatar images, NOT the logo
                if (!img.src.includes('logo.jpeg')) {
                    img.src = imgUrl;
                    img.onerror = function () {
                        this.src = `https://i.pravatar.cc/40?u=${user.email || 'guest'}`;
                    };
                }
            });

            // Check for Admin Panel link visibility - HIDE from regular users
            const adminLinks = document.querySelectorAll('a[href*="admin_login.html"], a[href*="admin-dashboard.html"]');
            adminLinks.forEach(adminLink => {
                // Only show admin panel if user role is ADMIN
                if (user.role && user.role === 'ADMIN') {
                    if (adminLink.parentElement) adminLink.parentElement.style.display = 'block';
                    adminLink.style.display = 'block';
                    adminLink.href = 'admin/admin-dashboard.html';
                } else {
                    if (adminLink.parentElement) adminLink.parentElement.style.display = 'none';
                    adminLink.style.display = 'none';
                }
            });
        }
    } else {
        if (guestNav) guestNav.style.display = 'flex';
        if (authNav) authNav.style.display = 'none';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('user');

    // Check if we are in a subdirectory (like /admin/)
    if (window.location.pathname.includes('/admin/')) {
        window.location.href = '../login.html';
    } else {
        window.location.href = 'login.html';
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    refreshUserProfile(); // Fetch fresh data

    // Attach logout handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});
