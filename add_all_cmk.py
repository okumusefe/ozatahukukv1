#!/usr/bin/env python3
"""
Find missing CMK articles and add them to yayinlar.html
Based on user's complete list of 48 CMK articles
"""
import os, re

# Complete CMK list from user
CMK_TITLES = {
    '3-7': 'Görev',
    '8-11': 'Bağlantılı Davalar',
    '12-21': 'Yetki',
    '22-32': 'Hâkimin Davaya Bakamaması ve Reddi',
    '33-38': 'Kararlar, Açıklanması ve Tebliği',
    '39-42': 'Süreler ve Eski Hâle Getirme',
    '43-61': 'Tanıklık',
    '62-73': 'Bilirkişi İncelemesi',
    '74-89': 'Gözlem Altına Alınma, Muayene, Keşif ve Otopsi',
    '90-99': 'Yakalama ve Gözaltı',
    '100-108': 'Tutuklama',
    '109-115': 'Adlî Kontrol',
    '116-134': 'Arama ve Elkoyma',
    '135-138': 'Telekomünikasyon Yoluyla Yapılan İletişimin Denetlenmesi',
    '139-140': 'Gizli Soruşturmacı ve Teknik Araçlarla İzleme',
    '141-144': 'Koruma Tedbirleri Nedeniyle Tazminat',
    '145-146': 'İfade veya Sorgu İçin Çağrı',
    '147-148': 'İfade ve Sorgu Usulü',
    '149-156': 'Müdafi Seçimi, Görevlendirilmesi, Görev ve Yetkileri',
    '157-159': 'Soruşturmanın Gizliliği, Suçların İhbarı',
    '160-169': 'Soruşturma İşlemleri',
    '170-171': 'Kamu Davasının Açılması',
    '172-174': 'Kovuşturmaya Yer Olmadığına Dair Karar, İtiraz ve İddianamenin İadesi',
    '175-181': 'Duruşma Hazırlığı',
    '182-202': 'Duruşma',
    '203-205': 'Duruşmanın Düzen ve Disiplini',
    '206-218': 'Delillerin Ortaya Konulması ve Tartışılması',
    '219-222': 'Duruşma Tutanağı',
    '223-225': 'Duruşmanın Sona Ermesi ve Hüküm',
    '226-226': 'Suç Niteliğinde Değişiklik',
    '227-232': 'Karar ve Hüküm',
    '233-236': 'Suçun Mağduru ile Şikâyetçinin Hakları',
    '237-243': 'Kamu Davasına Katılma',
    '244-246': 'Gaiplerin Yargılanması',
    '247-248': 'Kaçakların Yargılanması',
    '249-249': 'Tüzel Kişilerin Soruşturmada ve Kovuşturmada Temsili',
    '250-252': 'Bazı Suçlara İlişkin Muhakeme',
    '253-255': 'Uzlaşma',
    '256-259': 'Müsadere Usulü',
    '260-266': 'Genel Hükümler',
    '267-271': 'İtiraz',
    '272-285': 'İstinaf',
    '286-307': 'Temyiz',
    '308-308': 'Cumhuriyet Başsavcısının İtiraz Yetkisi',
    '309-310': 'Kanun Yararına Bozma',
    '311-323': 'Yargılamanın Yenilenmesi',
    '324-330': 'Yargılama Giderleri',
    '331-335': 'Çeşitli Hükümler',
}

# Read current yayinlar.html
with open('yayinlar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find which CMK ranges are already in yayinlar.html
# Handle both formats: 226-226 and just 226
existing = set()
for match in re.findall(r'makale-cmk-(\d+)-(\d+)\.html', content):
    start, end = match
    existing.add(f"{start}-{end}")

print(f"CMK articles in yayinlar.html: {len(existing)}")
print(f"Expected CMK articles: {len(CMK_TITLES)}")

# Find missing
missing = []
for range_key, title in CMK_TITLES.items():
    if range_key not in existing:
        missing.append((range_key, title))

print(f"\nMissing CMK articles: {len(missing)}")
for range_key, title in missing:
    print(f"  - {range_key}: {title}")

# Generate missing articles HTML
if missing:
    missing_html = []
    for range_key, title in missing:
        parts = range_key.split('-')
        start, end = parts[0], parts[1]
        # Normalize display
        display = start if start == end else f"{start}-{end}"
        article = f'''                    <article class="article-card" data-category="cmk">
                        <div class="article-header">
                            <span class="article-category">CMK</span>
                            <span class="article-date">27 Mart 2026</span>
                        </div>
                        <h2 class="article-title">Ceza Muhakemesi Kanunu'nda {title}: (md. {display})</h2>
                        <div class="article-excerpt">
                            <p><strong>CMK md. {display}</strong> - {title}.</p>
                        </div>
                        <button class="article-read-more" onclick="window.location.href='makale-cmk-{start}-{end}.html'">Devamını Oku →</button>
                    </article>'''
        missing_html.append(article)
    
    # Find last CMK article and add after it
    pattern = r'(<article class="article-card" data-category="cmk">.*?makale-cmk-[\d-]+\.html.*?Devamını Oku →</button>\s*</article>)(\s*</div>\s*</div>\s*</section>)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        all_missing = '\n\n'.join(missing_html)
        new_content = content[:match.end(1)] + '\n\n' + all_missing + match.group(2)
        
        with open('yayinlar.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n✓ Added {len(missing)} CMK articles")
    else:
        print("\n✗ Could not find insertion point")
else:
    print("\n✓ All CMK articles already present")

# Final count
tck_count = len(re.findall(r'data-category="tck"', content))
cmk_count = len(re.findall(r'data-category="cmk"', content))
print(f"\nFinal count:")
print(f"  TCK: {tck_count}")
print(f"  CMK: {cmk_count}")
print(f"  Total: {tck_count + cmk_count}")
