// Publications data - Add new publications at the top of the array
const publicationsData = [
    {
        title: "2026 Trafik Hukuku Ansiklopedisi: APP Plaka, Radar ve Yeni Nesil İdari Yaptırımlara Karşı Kapsamlı Hukuki Savunma Rehberi",
        date: "23 Mart 2026",
        category: "Trafik Hukuku",
        url: "yayinlar.html#article4",
        shortTitle: "2026 Trafik Hukuku Ansiklopedisi"
    },
    {
        title: "Türk Ceza Hukukunda Göçmen Kaçakçılığı Suçu (TCK 79) Ve Hukuki Savunma Stratejileri",
        date: "9 Mart 2026",
        category: "Ceza Hukuku",
        url: "yayinlar.html#article3",
        shortTitle: "Göçmen Kaçakçılığı Suçu (TCK 79)"
    },
    {
        title: "Türk Ceza Hukukunda Nitelikli Dolandırıcılık Suçu (TCK 158) Ve Hukuki Boyutu",
        date: "7 Mart 2026",
        category: "Ceza Hukuku",
        url: "yayinlar.html#article2",
        shortTitle: "Nitelikli Dolandırıcılık Suçu (TCK 158)"
    },
    {
        title: "Türk Ceza Hukukunda Uyuşturucu Ticareti Suçu (TCK 188) Ve Kullanım Sınırı Tartışması",
        date: "5 Mart 2026",
        category: "Ceza Hukuku",
        url: "yayinlar.html#article1",
        shortTitle: "Uyuşturucu Ticareti Suçu (TCK 188)"
    }
];

// Function to render latest publications in footer
function renderLatestPublications() {
    const containers = document.querySelectorAll('.latest-publications-list');
    
    containers.forEach(container => {
        // Get 3 most recent publications
        const latestPubs = publicationsData.slice(0, 3);
        
        let html = '<ul style="list-style: none; padding: 0; margin: 0;">';
        
        latestPubs.forEach(pub => {
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

// Run when DOM is loaded
document.addEventListener('DOMContentLoaded', renderLatestPublications);
