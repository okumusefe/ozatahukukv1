#!/usr/bin/env python3
"""
Fix hero sections in calculation tools:
1. Center text in existing hero sections
2. Add hero sections to tools that don't have them
"""

import os
import glob
import re

def get_hero_html(title, subtitle):
    return f'''<section class="page-hero">
        <div class="hero-content">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    </section>'''

# Map of filenames to their proper titles
TITLE_MAP = {
    'trafik-kazasi-tazminati.html': ('Trafik Kazası Tazminatı Hesaplama', '2026 yılı güncel verileriyle trafik kazası tazminatı hesaplama aracı'),
    'is-kazasi-tazminati.html': ('İş Kazası Tazminatı Hesaplama', 'İş kazası tazminatı hesaplama aracı'),
    'kidem-tazminati.html': ('Kıdem Tazminatı Hesaplama', 'Kıdem tazminatı hesaplama aracı'),
    'ihbar-tazminati.html': ('İhbar Tazminatı Hesaplama', 'İhbar tazminatı hesaplama aracı'),
    'nafaka-hesaplama.html': ('Nafaka Hesaplama', 'Nafaka hesaplama aracı'),
    'vekalet-ucreti.html': ('Vekalet Ücreti Hesaplama', 'Vekalet ücreti hesaplama aracı'),
    'mahkeme-harci.html': ('Mahkeme Harcı Hesaplama', 'Mahkeme harcı hesaplama aracı'),
    'tapu-harci.html': ('Tapu Harcı Hesaplama', 'Tapu harcı hesaplama aracı'),
    'icra-harci.html': ('İcra Harcı Hesaplama', 'İcra harcı hesaplama aracı'),
    'arac-deger-kaybi.html': ('Araç Değer Kaybı Hesaplama', 'Araç değer kaybı hesaplama aracı'),
    'kira-artis.html': ('Kira Artışı Hesaplama', 'Kira artışı hesaplama aracı'),
    'kira-stopaj-hesaplama.html': ('Kira Stopaj Hesaplama', 'Kira stopaj hesaplama aracı'),
    'fazla-mesai.html': ('Fazla Mesai Hesaplama', 'Fazla mesai hesaplama aracı'),
    'gece-calismasi.html': ('Gece Çalışması Hesaplama', 'Gece çalışması hesaplama aracı'),
    'yillik-izin.html': ('Yıllık İzin Hesaplama', 'Yıllık izin hesaplama aracı'),
    'dogum-izni-hesaplama.html': ('Doğum İzni Hesaplama', 'Doğum izni hesaplama aracı'),
    'issizlik-maasi.html': ('İşsizlik Maaşı Hesaplama', 'İşsizlik maaşı hesaplama aracı'),
    'emekli-maasi-hesaplama.html': ('Emekli Maaşı Hesaplama', 'Emekli maaşı hesaplama aracı'),
    'netten-brute-maas.html': ('Netten Brüt Maaş Hesaplama', 'Netten brüt maaş hesaplama aracı'),
    'smm-hesaplama.html': ('SMM Hesaplama', 'Serbest meslek makbuzu hesaplama aracı'),
    'gunluk-yevmiye.html': ('Günlük Yevmiye Hesaplama', 'Günlük yevmiye hesaplama aracı'),
    'bayram-tatil-ucreti.html': ('Bayram Tatil Ücreti Hesaplama', 'Bayram tatil ücreti hesaplama aracı'),
    'ceza-zamanasimi.html': ('Ceza Zamanaşımı Hesaplama', 'Ceza zamanaşımı hesaplama aracı'),
    'hukumlu-infaz.html': ('Hükümlü İnfaz Hesaplama', 'Hükümlü infaz hesaplama aracı'),
    'askerlik-borclanmasi.html': ('Askerlik Borçlanması Hesaplama', 'Askerlik borçlanması hesaplama aracı'),
    'yurtdisi-borclanmasi.html': ('Yurtdışı Borçlanması Hesaplama', 'Yurtdışı borçlanması hesaplama aracı'),
    'tazminat.html': ('Tazminat Hesaplama', 'Tazminat hesaplama aracı'),
    'yayinlar.html': ('Yayınlar', 'Hukuki yayınlar ve makaleler'),
}

def fix_hero_section(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has page-hero
    if 'page-hero' in content:
        # Fix centering in existing hero
        content = re.sub(
            r'<section class="page-hero">\s*<div class="hero-content">',
            '<section class="page-hero" style="text-align: center;">\n        <div class="hero-content" style="text-align: center;">',
            content
        )
        print(f'Fixed centering: {filename}')
    else:
        # Add hero section after header
        title, subtitle = TITLE_MAP.get(filename, ('Hesaplama Aracı', 'Hesaplama aracı'))
        hero_html = get_hero_html(title, subtitle)
        
        # Find position after </header> and before <section class="calculator
        header_end = content.find('</header>')
        if header_end != -1:
            insert_pos = header_end + 9
            # Check if there's a calculator-section or main content after
            next_section = content.find('<section class="calculator', insert_pos)
            if next_section == -1:
                next_section = content.find('<main>', insert_pos)
            if next_section == -1:
                next_section = content.find('<div class="calculator', insert_pos)
            
            if next_section != -1:
                # Insert hero before the next section
                new_content = content[:next_section] + '\n    ' + hero_html + '\n\n    ' + content[next_section:]
                content = new_content
                print(f'Added hero: {filename}')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    files = glob.glob('hesaplamalar/*.html')
    
    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            fix_hero_section(filepath, filename)
        except Exception as e:
            print(f'Error {filename}: {e}')
    
    print('Done!')

if __name__ == '__main__':
    main()
