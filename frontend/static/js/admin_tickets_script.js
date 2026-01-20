// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';
let currentPage = 1;
const itemsPerPage = 10;
let allBookings = [];

function getToken() {
    return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
}

// Show toast notification
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    toastMessage.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), duration);
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

// Get status badge
function getStatusBadge(status) {
    if (status === 'CANCELLED') {
        return `<span class="inline-flex items-center gap-1.5 rounded-full bg-red-500/20 px-2 py-1 text-xs font-medium text-red-300">
            <span class="w-1.5 h-1.5 rounded-full bg-red-400"></span>
            Cancelled
        </span>`;
    }
    if (status === 'CONFIRMED') {
        return `<span class="inline-flex items-center gap-1.5 rounded-full bg-green-500/20 px-2 py-1 text-xs font-medium text-green-300">
            <span class="w-1.5 h-1.5 rounded-full bg-green-400"></span>
            Confirmed
        </span>`;
    }
    return `<span class="inline-flex items-center gap-1.5 rounded-full bg-yellow-500/20 px-2 py-1 text-xs font-medium text-yellow-300">
        <span class="w-1.5 h-1.5 rounded-full bg-yellow-400"></span>
        Pending
    </span>`;
}

// Load bookings from API
async function loadBookings() {
    try {
        const token = getToken();
        if (!token) {
            window.location.href = 'admin_login.html';
            return;
        }

        const response = await fetch(`${API_BASE_URL}/bookings/all`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch bookings');
        }

        allBookings = await response.json();
        document.getElementById('totalBookings').textContent = allBookings.length;

        renderTable();
    } catch (error) {
        console.error('Error loading bookings:', error);
        showToast('Failed to load bookings.');
        document.getElementById('bookingsTableBody').innerHTML = `
            <tr>
                <td colspan="7" class="px-4 py-8 text-center">
                    <p class="text-red-400 text-sm">Failed to load bookings. Please try again.</p>
                </td>
            </tr>
        `;
    }
}

// Export all tickets to CSV
function exportAllTickets() {
    if (allBookings.length === 0) {
        showToast('No bookings to export');
        return;
    }

    // Create CSV content
    const headers = ['Booking ID', 'User Name', 'User Email', 'Event', 'Quantity', 'Total Price', 'Status', 'Payment Status', 'Booked At'];
    const csvRows = [headers.join(',')];

    allBookings.forEach(b => {
        const row = [
            b.id,
            `"${(b.user?.first_name || '') + ' ' + (b.user?.last_name || '')}"`,
            `"${b.user?.email || 'N/A'}"`,
            `"${b.event?.title || 'N/A'}"`,
            b.quantity,
            b.total_price || 0,
            b.status,
            b.payment_status || 'N/A',
            new Date(b.booked_at).toLocaleString()
        ];
        csvRows.push(row.join(','));
    });

    const csvContent = csvRows.join('\n');

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `tickets_export_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast(`Exported ${allBookings.length} bookings to CSV`);
}

// Toggle filters visibility (optional advanced filters)
let filtersExpanded = false;
function toggleFilters() {
    filtersExpanded = !filtersExpanded;
    showToast(filtersExpanded ? 'Advanced filters: Use the dropdowns to filter data' : 'Filters closed');
}

// Load events for filter dropdown
async function loadEventsFilter() {
    try {
        const response = await fetch(`${API_BASE_URL}/events/?limit=1000`);
        if (response.ok) {
            const events = await response.json();
            const eventFilter = document.getElementById('eventFilter');
            if (eventFilter) {
                events.forEach(event => {
                    const option = document.createElement('option');
                    option.value = event.id;
                    option.textContent = event.title;
                    eventFilter.appendChild(option);
                });
            }
        }
    } catch (e) {
        console.warn('Could not load events filter:', e);
    }
}

// Search and filter bookings
function searchBookings() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    const eventFilter = document.getElementById('eventFilter')?.value;
    const dateFilter = document.getElementById('dateFilter')?.value;

    let filtered = allBookings;

    // Status filter
    if (statusFilter) {
        filtered = filtered.filter(b => b.status === statusFilter);
    }

    // Event filter
    if (eventFilter) {
        filtered = filtered.filter(b => b.event?.id == eventFilter);
    }

    // Date filter
    if (dateFilter) {
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

        filtered = filtered.filter(b => {
            const bookingDate = new Date(b.booked_at);

            switch (dateFilter) {
                case 'today':
                    return bookingDate >= today;
                case 'week':
                    const weekAgo = new Date(today);
                    weekAgo.setDate(weekAgo.getDate() - 7);
                    return bookingDate >= weekAgo;
                case 'month':
                    const monthAgo = new Date(today);
                    monthAgo.setMonth(monthAgo.getMonth() - 1);
                    return bookingDate >= monthAgo;
                case 'year':
                    const yearAgo = new Date(today);
                    yearAgo.setFullYear(yearAgo.getFullYear() - 1);
                    return bookingDate >= yearAgo;
                default:
                    return true;
            }
        });
    }

    // Search term filter
    if (searchTerm) {
        filtered = filtered.filter(b =>
            (b.user?.first_name + ' ' + b.user?.last_name).toLowerCase().includes(searchTerm) ||
            b.event?.title?.toLowerCase().includes(searchTerm) ||
            b.id.toString().includes(searchTerm)
        );
    }

    currentPage = 1; // Reset to first page when filtering
    renderTable(filtered);
}

// Render table
function renderTable(bookings = allBookings) {
    const tbody = document.getElementById('bookingsTableBody');

    if (bookings.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="px-4 py-8 text-center">
                    <p class="text-white/60 text-sm">No bookings found.</p>
                </td>
            </tr>
        `;
        return;
    }

    // Pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedBookings = bookings.slice(startIndex, endIndex);

    tbody.innerHTML = paginatedBookings.map(b => {
        // Construct proper image URL
        let profileImageUrl = 'https://i.pravatar.cc/32?img=1';
        if (b.user?.profile_image) {
            profileImageUrl = b.user.profile_image.startsWith('http') 
                ? b.user.profile_image 
                : `${API_BASE_URL}${b.user.profile_image}`;
        } else if (b.user?.email) {
            profileImageUrl = `https://i.pravatar.cc/32?u=${b.user.email}`;
        }

        return `
        <tr class="hover:bg-white/5 transition">
            <td class="px-4 py-4 text-white text-sm">#${b.id}</td>
            <td class="px-4 py-4 text-white text-sm flex items-center gap-2">
                <img src="${profileImageUrl}" alt="User" class="w-6 h-6 rounded-full object-cover" onerror="this.src='https://i.pravatar.cc/32?img=1'">
                ${b.user?.first_name || 'N/A'} ${b.user?.last_name || ''}
            </td>
            <td class="px-4 py-4 text-white/80 text-sm">${b.event?.title || 'N/A'}</td>
            <td class="px-4 py-4 text-white/60 text-sm">${b.quantity}</td>
            <td class="px-4 py-4 text-white/80 text-sm">Rs ${b.total_price || b.amount_total}</td>
            <td class="px-4 py-4 text-sm">${getStatusBadge(b.status)}</td>
            <td class="px-4 py-4 text-white/60 text-sm flex items-center justify-between">
                <span>${formatDate(b.booked_at)}</span>
                <button onclick="deleteBooking(${b.id})" class="text-red-400 hover:text-red-300 transition" title="Delete booking">
                    <span class="material-symbols-outlined text-sm">delete</span>
                </button>
            </td>
        </tr>
    `;
    }).join('');

    renderPagination(bookings.length);
}

// Render pagination
function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const container = document.getElementById('paginationContainer');

    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    let html = `
        <button onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''} 
            class="flex w-10 h-10 items-center justify-center text-white/60 hover:text-white transition disabled:opacity-30">
            <span class="material-symbols-outlined">chevron_left</span>
        </button>
    `;

    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            html += `
                <button onclick="changePage(${i})" 
                    class="flex w-10 h-10 items-center justify-center rounded-full text-sm transition
                    ${i === currentPage ? 'bg-primary/30 text-white font-bold' : 'text-white/60 hover:bg-white/10'}">
                    ${i}
                </button>
            `;
        } else if (i === currentPage - 2 || i === currentPage + 2) {
            html += `<span class="flex w-10 h-10 items-center justify-center text-white/60 text-sm">...</span>`;
        }
    }

    html += `
        <button onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''} 
            class="flex w-10 h-10 items-center justify-center text-white/60 hover:text-white transition disabled:opacity-30">
            <span class="material-symbols-outlined">chevron_right</span>
        </button>
    `;

    container.innerHTML = html;
}

// Change page
function changePage(page) {
    const totalPages = Math.ceil(allBookings.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTable();
}

// Delete booking function
async function deleteBooking(bookingId) {
    if (!confirm('Are you sure you want to delete this booking? This action cannot be undone.')) {
        return;
    }

    try {
        const token = getToken();
        if (!token) {
            showToast('Authentication required');
            window.location.href = 'admin_login.html';
            return;
        }

        const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            try {
                const errorData = JSON.parse(errorText);
                throw new Error(errorData.detail || `Failed to delete booking: ${response.status}`);
            } catch {
                throw new Error(`Failed to delete booking: ${response.status} ${response.statusText}`);
            }
        }

        showToast('Booking deleted successfully');
        
        // Remove from local array and re-render
        allBookings = allBookings.filter(b => b.id !== bookingId);
        document.getElementById('totalBookings').textContent = allBookings.length;
        renderTable();
    } catch (error) {
        console.error('Error deleting booking:', error);
        showToast(`Error: ${error.message}`);
    }
}

document.getElementById('searchInput').addEventListener('input', searchBookings);
document.getElementById('statusFilter').addEventListener('change', searchBookings);

// Add listeners for new filters if they exist
const eventFilterEl = document.getElementById('eventFilter');
if (eventFilterEl) eventFilterEl.addEventListener('change', searchBookings);

const dateFilterEl = document.getElementById('dateFilter');
if (dateFilterEl) dateFilterEl.addEventListener('change', searchBookings);

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '../login.html';
});

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    loadEventsFilter();
    loadBookings();
});
