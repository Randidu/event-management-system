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
    } catch (e) {
        console.warn('Could not load admin profile:', e);
    }
}

// Auto-load on DOMContentLoaded
document.addEventListener('DOMContentLoaded', loadAdminProfile);
