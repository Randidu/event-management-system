const translations = {
    "en": {
        "nav_home": "Home",
        "nav_events": "Events",
        "nav_tickets": "My Tickets",
        "nav_wishlist": "Wishlist",
        "nav_support": "Support",
        "nav_login": "Login",
        "nav_signup": "Sign Up",
        "nav_profile": "My Profile",
        "nav_logout": "Logout",
        "nav_admin": "Admin Panel",

        "hero_title_1": "Discover",
        "hero_title_2": "Events",
        "hero_subtitle_1": "Find your perfect musical experience from thousands of live events",
        "hero_subtitle_2": "Connecting artists and fans",
        "hero_cta_explore": "Explore Events",
        "hero_cta_create": "Create Event",

        "search_placeholder": "Search events, artists, or venues...",
        "search_btn": "Search",

        "section_featured": "Featured Events",
        "section_upcoming": "Upcoming Events",
        "section_categories": "Browse Categories",

        "btn_book": "Book Now",
        "btn_details": "View Details",
        "btn_more": "Load More",

        "footer_about": "About Us",
        "footer_contact": "Contact",
        "footer_rights": "All rights reserved.",

        "ai_search_label": "AI Smart Search",
        "ai_search_placeholder": "Ask AI to find events (e.g. 'Upcoming music festivals in Colombo under 5000')",
        "ai_search_btn": "AI Search",
        "ai_search_hint": "Try natural language queries to find exactly what you want.",

        "filter_date": "Date",
        "filter_category": "Category",
        "filter_location": "Location",
        "filter_reset": "Reset Filters",

        "chat_header": "EMS Assistant",
        "chat_greeting": "Hello! I'm your EMS AI Assistant. I can help you find events, answer payment questions, or guide you through booking. How can I help today?",
        "chat_placeholder": "Type a message...",
        "chat_offline": "Offline mode: Unable to connect to AI server.",
        "chat_error": "Sorry, I encountered an error."
    },
    "si": {
        "nav_home": "මුල් පිටුව",
        "nav_events": "සිදුවීම්",
        "nav_tickets": "මගේ ටිකට්",
        "nav_wishlist": "සුරැකුම්",
        "nav_support": "සහය",
        "nav_login": "පිවිසෙන්න",
        "nav_signup": "ලියාපදිංචි වන්න",
        "nav_profile": "මගේ ගිණුම",
        "nav_logout": "ඉවත් වන්න",
        "nav_admin": "පරිපාලක පැනලය",

        "hero_title_1": "සොයාගන්න",
        "hero_title_2": "සිදුවීම්",
        "hero_subtitle_1": "ඔබට ගැළපෙන හොඳම සංගීතමය අත්දැකීම් දහස් ගණනක් අතරින් සොයාගන්න",
        "hero_subtitle_2": "කලාකරුවන් සහ රසිකයින් යා කරන තැන",
        "hero_cta_explore": "සිදුවීම් සොයන්න",
        "hero_cta_create": "සිදුවීමක් එක් කරන්න",

        "search_placeholder": "සිදුවීම්, කලාකරුවන් හෝ ස්ථාන සොයන්න...",
        "search_btn": "සොයන්න",

        "section_featured": "විශේෂාංග සිදුවීම්",
        "section_upcoming": "ඉදිරි සිදුවීම්",
        "section_categories": "වර්ගීකරණයන්",

        "btn_book": "වෙන්කරවා ගන්න",
        "btn_details": "විස්තර බලන්න",
        "btn_more": "තව පෙන්වන්න",

        "footer_about": "අප ගැන",
        "footer_contact": "සම්බන්ධ වීමට",
        "footer_rights": "සියලුම හිමිකම් ඇවිරිණි.",

        "ai_search_label": "AI ස්මාර්ට් සෙවුම",
        "ai_search_placeholder": "AI හරහා සොයන්න (උදා: 'කොළඹ රු.5000 ට අඩු සංගීත සංදර්ශන')",
        "ai_search_btn": "AI සෙවුම",
        "ai_search_hint": "ඔබට අවශ්‍ය දේ හරියටම සොයා ගැනීමට ස්වාභාවික බසින් විමසන්න.",

        "filter_date": "දිනය",
        "filter_category": "වර්ගය",
        "filter_location": "ස්ථානය",
        "filter_reset": "පෙරහන් ඉවත් කරන්න",

        "chat_header": "EMS සහයක",
        "chat_greeting": "ආයුබෝවන්! මම ඔබගේ EMS AI සහයකයා. ඔබට සිදුවීම් සොයා ගැනීමට, ගෙවීම් ගැටළු විසඳීමට හෝ වෙන්කරවා ගැනීම සඳහා උදව් කිරීමට මට පුළුවන්. ඔබට කෙසේද උදව් කළ හැක්කේ?",
        "chat_placeholder": "ඔබේ පණිවිඩය ටයිප් කරන්න...",
        "chat_offline": "නොබැඳි මාදිලිය: AI සේවාදායකය හා සම්බන්ධ විය නොහැක.",
        "chat_error": "සමාවන්න, දෝෂයක් ඇති විය."
    }
};

function setLanguage(lang) {
    if (!translations[lang]) return;

    localStorage.setItem('preferredLanguage', lang);
    document.documentElement.lang = lang;

    // Update active state in switcher if exists
    const switcher = document.getElementById('languageSwitcher');
    if (switcher) {
        switcher.innerHTML = lang === 'si' ? 'සිංහල' : 'English';
    }

    updateContent();
}

function updateContent() {
    const lang = localStorage.getItem('preferredLanguage') || 'en';
    const elements = document.querySelectorAll('[data-i18n]');

    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            if (element.tagName === 'INPUT' && element.getAttribute('placeholder')) {
                element.placeholder = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });

    // Update dynamic content like dates if needed specially, but for now text replacement is enough
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLanguage') || 'en';
    setLanguage(savedLang);
});

// Helper to toggle language
function toggleLanguage(lang) {
    setLanguage(lang);
}
