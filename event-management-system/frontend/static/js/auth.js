/**
 * Authentication Helper Functions
 */

// Check if user is logged in
function checkAuth() {
    return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
}

// Get user from localStorage or sessionStorage
function getUser() {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
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
            if (user.profile_image) {
                const imgUrl = user.profile_image.startsWith('http')
                    ? user.profile_image
                    : `http://127.0.0.1:8000${user.profile_image}`;

                document.querySelectorAll('.user-avatar').forEach(img => {
                    img.src = imgUrl;
                    // Add error handler fallback
                    img.onerror = function () {
                        this.src = 'https://i.pravatar.cc/40?img=12';
                    };
                });
            }

            // Check for Admin Panel link visibility - HIDE from regular users
            const adminLinks = document.querySelectorAll('a[href*="admin_login.html"], a[href*="admin-dashboard.html"]');
            adminLinks.forEach(adminLink => {
                // Only show admin panel if user role is ADMIN
                if (user.role && user.role === 'ADMIN') {
                    // Show parent list item
                    if (adminLink.parentElement) {
                        adminLink.parentElement.style.display = 'block';
                    }
                    // Ensure link itself is visible (in case style was on link)
                    adminLink.style.display = 'block';

                    // Update href to dashboard
                    adminLink.href = 'admin/admin-dashboard.html';
                } else {
                    // Hide admin panel from non-admin users
                    if (adminLink.parentElement) {
                        adminLink.parentElement.style.display = 'none';
                    }
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

    // Attach logout handler
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});
