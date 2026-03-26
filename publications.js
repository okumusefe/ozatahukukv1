// Dynamic Publications Loader - Fetches latest publications from yayinlar.html
// This script automatically extracts the 3 most recent publications from yayinlar.html

// Parse Turkish date format (e.g., "27 Mart 2026") to Date object
function parseTurkishDate(dateStr) {
    const monthMap = {
        'Ocak': 0, 'Şubat': 1, 'Mart': 2, 'Nisan': 3, 'Mayıs': 4, 'Haziran': 5,
        'Temmuz': 6, 'Ağustos': 7, 'Eylül': 8, 'Ekim': 9, 'Kasım': 10, 'Aralık': 11
    };
    
    const parts = dateStr.trim().split(' ');
    if (parts.length === 3) {
        const day = parseInt(parts[0], 10);
        const month = monthMap[parts[1]];
        const year = parseInt(parts[2], 10);
        
        if (!isNaN(day) && month !== undefined && !isNaN(year)) {
            return new Date(year, month, day);
        }
    }
    return new Date(0); // Return epoch if parsing fails
}

async function fetchAndParsePublications() {
    try {
        // Fetch yayinlar.html
        const response = await fetch('yayinlar.html');
        if (!response.ok) {
            throw new Error('Failed to fetch yayinlar.html');
        }
        
        const html = await response.text();
        
        // Parse the HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Find all article cards
        const articles = doc.querySelectorAll('.article-card');
        
        // Extract data from all articles
        const publications = [];
        
        articles.forEach((article) => {
            const titleEl = article.querySelector('.article-title');
            const dateEl = article.querySelector('.article-date');
            const categoryEl = article.querySelector('.article-category');
            const readMoreBtn = article.querySelector('.article-read-more');
            
            if (titleEl && dateEl) {
                // Get the article ID from onclick attribute
                let articleId = '';
                if (readMoreBtn) {
                    const onclickStr = readMoreBtn.getAttribute('onclick') || '';
                    const match = onclickStr.match(/toggleArticle\(['"]([^'"]+)['"]\)/);
                    if (match) {
                        articleId = match[1];
                    }
                }
                
                // Create short title (max 50 chars)
                let fullTitle = titleEl.textContent.trim();
                let shortTitle = fullTitle.length > 50 ? fullTitle.substring(0, 50) + '...' : fullTitle;
                
                const dateStr = dateEl.textContent.trim();
                
                publications.push({
                    title: fullTitle,
                    shortTitle: shortTitle,
                    date: dateStr,
                    dateObj: parseTurkishDate(dateStr),
                    category: categoryEl ? categoryEl.textContent.trim() : 'Yayınlar',
                    url: articleId ? `yayinlar.html#${articleId}` : 'yayinlar.html'
                });
            }
        });
        
        // Sort by date (newest first)
        publications.sort((a, b) => b.dateObj - a.dateObj);
        
        // Return only the 3 most recent
        return publications.slice(0, 3);
    } catch (error) {
        console.error('Error fetching publications:', error);
        return [];
    }
}

// Function to render latest publications in footer
async function renderLatestPublications() {
    const containers = document.querySelectorAll('.latest-publications-list');
    
    if (containers.length === 0) return;
    
    // Fetch publications dynamically
    const publications = await fetchAndParsePublications();
    
    // Fallback to static data if fetch fails
    const displayPubs = publications.length > 0 ? publications : getFallbackPublications();
    
    containers.forEach(container => {
        let html = '<ul style="list-style: none; padding: 0; margin: 0;">';
        
        displayPubs.forEach(pub => {
            html += `
                <li style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <a href="${pub.url}" style="color: white; text-decoration: none; font-size: 0.9rem; display: block; transition: color 0.3s ease;">
                        <strong style="display: block; margin-bottom: 4px;">${pub.shortTitle}</strong>
                        <span style="font-size: 0.8rem; opacity: 0.8;">${pub.date} | ${pub.category}</span>
                    </a>
                </li>
            `;
        });
        
        html += '</ul>';
        html += '<a href="yayinlar.html" style="display: inline-block; margin-top: 15px; color: var(--accent-color); text-decoration: none; font-size: 0.85rem; font-weight: 600;">Tüm Yayınlar →</a>';
        
        container.innerHTML = html;
    });
}

// Fallback data in case fetch fails
function getFallbackPublications() {
    return [
        {
            title: "Kasten Öldürme Suçunda İnfaz ve Haksız Tahrik: Yargıtay'ın Güncel İçtihatları",
            shortTitle: "Kasten Öldürme - İnfaz ve Haksız Tahrik",
            date: "27 Mart 2026",
            category: "Ceza Hukuku - Kasten Öldürme",
            url: "yayinlar.html#article-kasten-oldurme"
        },
        {
            title: "Nitelikli Yaralama Suçunda Hayati Tehlike ve İnfaz: Yargıtay Emsal Kararları",
            shortTitle: "Nitelikli Yaralama - Hayati Tehlike",
            date: "27 Mart 2026",
            category: "Ceza Hukuku - Nitelikli Yaralama",
            url: "yayinlar.html#article-yaralama"
        },
        {
            title: "Cinsel Dokunulmazlığa Karşı Suçlarda İnfaz ve Mağdur Psikolojisi: Yargıtay ve AİHM İçtihatları",
            shortTitle: "Cinsel Suçlarda İnfaz ve Mağdur Psikolojisi",
            date: "27 Mart 2026",
            category: "Ceza Hukuku - Cinsel Suçlar",
            url: "yayinlar.html#article-cinsel"
        }
    ];
}

// Run when DOM is loaded
document.addEventListener('DOMContentLoaded', renderLatestPublications);
