const API_BASE_URL = 'http://127.0.0.1:8000';

async function loadDashboardStats() {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');

    if (!token) {
        window.location.href = 'admin_login.html';
        return;
    }

    // Get date range filter value
    const dateRange = document.getElementById('dateRangeFilter')?.value || '30';
    const daysParam = dateRange === 'all' ? 9999 : parseInt(dateRange);

    try {
        const response = await fetch(`${API_BASE_URL}/admin/dashboard-stats?days=${daysParam}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            if (response.status === 403 || response.status === 401) {
                alert('Access denied. Admin privileges required.');
                window.location.href = '../index.html';
                return;
            }
            throw new Error('Failed to fetch stats');
        }

        const stats = await response.json();
        updateDashboard(stats);

    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Failed to load dashboard data');
    }
}

function updateDashboard(stats) {
    // 1. Stats Cards
    const totalRev = stats.total_revenue || 0;
    document.getElementById('totalRevenue').textContent = `Rs ${totalRev.toLocaleString()}`;
    document.getElementById('activeUsers').textContent = stats.active_users.toLocaleString();
    document.getElementById('openTickets').textContent = stats.open_tickets.toLocaleString();
    document.getElementById('upcomingEventsCount').textContent = stats.upcoming_events_count.toLocaleString();

    // 2. Recent Signups
    displayRecentSignups(stats.recent_signups);

    // 3. Upcoming Events List
    displayUpcomingEvents(stats.upcoming_events);
}

function displayRecentSignups(users) {
    const tbody = document.getElementById('recentSignupsBody');
    if (!tbody) return;

    if (!users || users.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center py-4 text-white/50">No recent signups.</td></tr>`;
        return;
    }

    tbody.innerHTML = users.map(user => `
        <tr class="border-b border-[#4d3168]/50 hover:bg-primary/10 transition">
            <td class="py-3 px-3 text-sm text-white flex items-center gap-2">
                <img src="${user.profile_image ? (user.profile_image.startsWith('http') ? user.profile_image : API_BASE_URL + user.profile_image) : `https://i.pravatar.cc/32?u=${user.email}`}" 
                     alt="${user.first_name}" class="w-8 h-8 rounded-full object-cover">
                ${user.first_name} ${user.last_name}
            </td>
            <td class="py-3 px-3 text-sm text-white/80">${user.email}</td>
            <td class="py-3 px-3 text-sm text-white/80">${formatDate(user.created_at)}</td>
            <td class="py-3 px-3 text-sm">
                <span class="bg-green-500/20 text-green-400 py-1 px-2 rounded-full text-xs">${user.is_active ? 'Verified' : 'Pending'}</span>
            </td>
        </tr>
    `).join('');
}

function displayUpcomingEvents(events) {
    const container = document.getElementById('upcomingEventsList');
    if (!container) return;

    if (!events || events.length === 0) {
        container.innerHTML = `<p class="text-center text-white/50">No upcoming events.</p>`;
        return;
    }

    container.innerHTML = events.map(event => `
        <div class="flex items-center gap-4 p-2 rounded-lg hover:bg-white/5 transition">
            <img src="${event.poster_url ? (event.poster_url.startsWith('http') ? event.poster_url : API_BASE_URL + event.poster_url) : 'https://placehold.co/80x80?text=Event'}" 
                 alt="${event.title}" class="w-16 h-16 rounded-lg object-cover">
            <div class="flex-1">
                <p class="font-medium text-white">${event.title}</p>
                <p class="text-sm text-white/70">${formatDate(event.starts_at)} | ${event.location}</p>
            </div>
            <a href="edit-event.html?id=${event.id}" class="text-primary hover:text-white transition" title="Edit Event">
                <span class="material-symbols-outlined">edit</span>
            </a>
        </div>
    `).join('');
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function showError(message) {
    // Basic alert fallback or existing toast logic
    alert(message);
}

// Load admin profile from stored user data
function loadAdminProfile() {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (!userStr) return;

    try {
        const user = JSON.parse(userStr);

        // Update sidebar admin image
        const sidebarImg = document.getElementById('sidebarAdminImg');
        if (sidebarImg && user.profile_image) {
            const imgUrl = user.profile_image.startsWith('http')
                ? user.profile_image
                : API_BASE_URL + user.profile_image;
            sidebarImg.src = imgUrl;
        } else if (sidebarImg && user.email) {
            sidebarImg.src = `https://i.pravatar.cc/40?u=${user.email}`;
        }

        // Update sidebar admin name
        const sidebarName = document.getElementById('sidebarAdminName');
        if (sidebarName && user.first_name) {
            sidebarName.textContent = `${user.first_name} ${user.last_name || ''}`;
        }

        // Update header admin image
        const headerImg = document.getElementById('headerAdminImg');
        if (headerImg && user.profile_image) {
            const imgUrl = user.profile_image.startsWith('http')
                ? user.profile_image
                : API_BASE_URL + user.profile_image;
            headerImg.src = imgUrl;
        } else if (headerImg && user.email) {
            headerImg.src = `https://i.pravatar.cc/40?u=${user.email}`;
        }
    } catch (e) {
        console.warn('Could not load admin profile:', e);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadAdminProfile();
    loadDashboardStats();

    // Add date range filter listener
    const dateFilter = document.getElementById('dateRangeFilter');
    if (dateFilter) {
        dateFilter.addEventListener('change', loadDashboardStats);
    }
});

