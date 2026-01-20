// Admin Profile Loader - Shared across all admin pages
const ADMIN_API_BASE_URL = 'http://127.0.0.1:8000';

function loadAdminProfile() {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (!userStr) return;

    try {
        const user = JSON.parse(userStr);

        // Update sidebar admin image
        const sidebarImg = document.getElementById('sidebarAdminImg');
        if (sidebarImg) {
            if (user.profile_image) {
                const imgUrl = user.profile_image.startsWith('http')
                    ? user.profile_image
                    : ADMIN_API_BASE_URL + user.profile_image;
                sidebarImg.src = imgUrl;
            } else if (user.email) {
                sidebarImg.src = `https://i.pravatar.cc/40?u=${user.email}`;
            }
        }

        // Update sidebar admin name
        const sidebarName = document.getElementById('sidebarAdminName');
        if (sidebarName && user.first_name) {
            sidebarName.textContent = `${user.first_name} ${user.last_name || ''}`;
        }

        // Update header admin image
        const headerImg = document.getElementById('headerAdminImg');
        if (headerImg) {
            if (user.profile_image) {
                const imgUrl = user.profile_image.startsWith('http')
                    ? user.profile_image
                    : ADMIN_API_BASE_URL + user.profile_image;
                headerImg.src = imgUrl;
            } else if (user.email) {
                headerImg.src = `https://i.pravatar.cc/40?u=${user.email}`;
            }
        }

        // Update navbar user avatar images
        document.querySelectorAll('.user-avatar').forEach(img => {
            if (user.profile_image) {
                const imgUrl = user.profile_image.startsWith('http')
                    ? user.profile_image
                    : ADMIN_API_BASE_URL + user.profile_image;
                img.src = imgUrl;
            } else if (user.email) {
                img.src = `https://i.pravatar.cc/40?u=${user.email}`;
            }
        });
    } catch (e) {
        console.warn('Could not load admin profile:', e);
    }
}

// Reload admin profile - call this after updating profile
window.reloadAdminProfile = function() {
    loadAdminProfile();
};

// Auto-load on DOMContentLoaded and also after a small delay to ensure all elements are ready
document.addEventListener('DOMContentLoaded', function() {
    // Load immediately
    loadAdminProfile();
    
    // Also load after a small delay to ensure all elements are rendered
    setTimeout(loadAdminProfile, 100);
});
