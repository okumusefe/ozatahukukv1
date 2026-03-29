#!/usr/bin/env python3
"""
Update all article files to match makale-tck-35-36.html style
"""
import os
import re
from datetime import datetime

# Style template based on makale-tck-35-36.html
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - Özata Hukuk">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    <link rel="shortcut icon" href="favicon.ico">
    <title>{title} - Özata Hukuk</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="responsive.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="index.html" class="logo">
                <img src="logo.png" alt="Özata Hukuk Logo" width="186" height="70">
            </a>
            <button class="mobile-menu-toggle" aria-label="Menüyü Aç/Kapat">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="index.html">Ana Sayfa</a></li>
                <li><a href="hakkimizda.html">Hakkımızda</a></li>
                <li class="dropdown">
                    <a href="calisma-alanlari.html">Çalışma Alanlarımız</a>
                    <ul class="dropdown-menu">
                        <li><a href="ceza-hukuku.html">Ceza Hukuku</a></li>
                        <li><a href="aile-hukuku.html">Aile Hukuku</a></li>
                        <li><a href="is-hukuku.html">İş Hukuku</a></li>
                        <li><a href="gayrimenkul-hukuku.html">Gayrimenkul Hukuku</a></li>
                    </ul>
                </li>
                <li><a href="ekibimiz.html">Ekibimiz</a></li>
                <li><a href="yayinlar.html">Yayınlar</a></li>
                <li><a href="iletisim.html">İletişim</a></li>
            </ul>
        </div>
    </nav>

    <section class="page-hero">
        <div class="container">
            <h1>{h1_title}</h1>
            <p>{h1_subtitle}</p>
        </div>
    </section>

    <section class="articles-section">
        <div class="container">
            <div class="article-card full-article">
                <div class="article-header">
                    <span class="article-category">{category}</span>
                    <span class="article-date">{date}</span>
                </div>
                <h2 class="article-title">{h2_title}</h2>
                
                <div class="article-content">
{content}
                </div>
                
                <div class="article-author"><p><strong>Yazar:</strong><br>Avukat Ege Özata<br>Özata Hukuk Bürosu<br><em>{date}</em></p></div>
                
                <div class="back-to-articles">
                    <a href="yayinlar.html" class="btn">← Tüm Yayınlara Dön</a>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-about">
                    <h4>Özata Hukuk Bürosu</h4>
                    <p>Profesyonel ve deneyimli kadromuzla, hukuki konularda çözüm odaklı hizmet sunuyoruz.</p>
                </div>
                <div class="footer-contact">
                    <h4>İletişim</h4>
                    <p>Email: info@ozatahukuk.com<br>Telefon: +90 555 123 45 67</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Özata Hukuk. Tüm hakları saklıdır.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''

# Content templates for different article types
TCK_CONTENT_TEMPLATES = {
    '20-23': '''                    <p>Ceza hukukunun temel taşı, her bireyin yalnızca kendi fiillerinden sorumlu tutulması ilkesidir. Türk Ceza Kanunu'nun 20. maddesi bu hakikati veciz bir dille ifade eder: kimse başkasının suçundan ötürü cezalandırılamaz. Ancak hayatın akışı içinde bu kuralın istisnaları da doğal olarak belirir. Örneğin, bir işveren çalışanının hukuka aykırı fiilinden, bir ebeveyn ise küçük çocuğunun yarattığı zarardan sorumlu tutulabilir. Bu sorumluluk türü, kusursuz sorumluluk olarak nitelendirilir ve özel yükümlülüklerin ihlali halinde devreye girer.</p>
                    
                    <p>Suçun oluşabilmesi için failin kastı gerekir. Kast, kişinin fiilin hukuki anlam ve sonuçlarını bildiği hâlde bu fiili isteyerek gerçekleştirmesi demektir. Yargıtay içtihatlarında sıkça vurgulandığı üzere, kastın varlığı somut olayın tüm özelliklerine göre değerlendirilmelidir. Kimi zaman fail doğrudan bir neticeyi ister; örneğin bir cinayet planının tatbik edilmesi. Kimi zaman ise netice istenmez, ancak meydana gelmesine razı olunur; tıpkı bir yangın çıkarırken binada insanların olabileceğini öngörüp buna aldırmamak gibi. İşte bu ikinci durum, ceza hukukunda olası kast olarak kabul edilir ve aynı hukuki sonuçları doğurur.</p>
                    
                    <p>Taksir ise farklı bir hikaye anlatır. Burada fail, suçun oluşmasını istemez; öngörülebilir bir neticenin gerçekleşmesini önlemek için gerekli özeni göstermemesi sonucu hukuka aykırı sonuç meydana gelir. Bir trafik kazası, bir iş kazası veya bir tıbbi müdahalede ihmal; tüm bunlar taksirin tipik örnekleri arasında yer alır. Hukuk sistemimiz, taksirli suçlarda cezayı indirimli olarak tayin eder; kasten işlenen suçun cezasının yarısından az olmayacak şekilde. Ancak bu indirim, taksirin hafif bir kusur olmadığını gösterir; yalnızca cezanın bireyselleştirilmesi ilkesinin bir yansımasıdır.</p>
                    
                    <p>Kasten işlenen fiillerde bazen beklenmedik neticeler ortaya çıkabilir. Bir yaralama olayında mağdurun ölümü gerçekleşebilir; bir kundaklama eyleminde yangın daha geniş alana yayılabilir. İşte bu gibi durumlarda TCK'nın 23. maddesi devreye girer ve ceza yarıya kadar artırılabilir. Bu artırım, failin fiilin riskini üstlenmiş olmasından kaynaklanır; tam olarak istediği netice gerçekleşmese bile, fiilin tipik tehlikesini göze almıştır.</p>
                    
                    <p>Bu üç kavramın - kast, taksir ve neticenin ağırlaşması - ceza hukukundaki yeri, bir insan davranışının hukuki değerlendirmesinin ne denli incelikli olduğunu gösterir. Her somut olay, kendi içinde barındırdığı özgün hikaye ile değerlendirilmeyi hak eder. Yargıtay'ın zaman içinde oluşturduğu içtihatlar da bu bireyselleştirme çabasının bir yansımasıdır.</p>''',
}

def update_article(filename, title, h1_title, h1_subtitle, h2_title, category, content):
    """Update a single article file with new content"""
    date = "29 Mart 2026"
    
    new_html = HTML_TEMPLATE.format(
        title=title,
        h1_title=h1_title,
        h1_subtitle=h1_subtitle,
        h2_title=h2_title,
        category=category,
        date=date,
        content=content
    )
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Updated: {filename}")

# Get all article files
tck_files = sorted([f for f in os.listdir('.') if f.startswith('makale-tck-') and f.endswith('.html')])
cmk_files = sorted([f for f in os.listdir('.') if f.startswith('makale-cmk-') and f.endswith('.html')])

print(f"Found {len(tck_files)} TCK files and {len(cmk_files)} CMK files")
print("Starting update process...")

# First few files are already done, let's check remaining
for f in tck_files[:3]:
    print(f"  {f}")
