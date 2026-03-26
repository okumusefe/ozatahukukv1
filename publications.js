// Dynamic Publications Loader - Fetches latest publications from yayinlar.html
// This script automatically extracts the 3 most recent publications from yayinlar.html

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
        
        // Extract data from the 3 most recent articles
        const publications = [];
        
        articles.forEach((article, index) => {
            if (index >= 3) return; // Only get first 3
            
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
                
                publications.push({
                    title: fullTitle,
                    shortTitle: shortTitle,
                    date: dateEl.textContent.trim(),
                    category: categoryEl ? categoryEl.textContent.trim() : 'Yayınlar',
                    url: articleId ? `yayinlar.html#${articleId}` : 'yayinlar.html'
                });
            }
        });
        
        return publications;
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
            title: "Yargıtay 12. Hukuk Dairesi: İş Merkezi Bina Görevlisi Komşu Olarak Değerlendirilemeyeceğinden Tebligat Usulsüzdür",
            shortTitle: "Tebligat Usulsüzlüğü - Bina Görevlisi",
            date: "25 Mart 2026",
            category: "İcra İflas Hukuku",
            url: "yayinlar.html#article-yargitay"
        },
        {
            title: "KVKK İlke Kararı: Açık Rıza Metni ile Aydınlatma Metninin Ayrı Ayrı Düzenlenmesi",
            shortTitle: "KVKK Açık Rıza ve Aydınlatma Kararı",
            date: "24 Mart 2026",
            category: "Kişisel Verilerin Korunması",
            url: "yayinlar.html#article-kvkk"
        },
        {
            title: "7576 Sayılı Milli Parklar Kanunu ve Bazı Kanunlarda Değişiklik Yapılmasına Dair Kanun",
            shortTitle: "7576 Sayılı Milli Parklar Kanunu",
            date: "23 Mart 2026",
            category: "Mevzuat",
            url: "yayinlar.html#article-milli-park"
        }
    ];
}

// Run when DOM is loaded
document.addEventListener('DOMContentLoaded', renderLatestPublications);
