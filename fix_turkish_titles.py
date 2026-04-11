#!/usr/bin/env python3
"""
Fix Turkish characters in petition page titles
"""

import os
import re
import glob

# Mapping of ASCII characters to Turkish characters
turkish_map = {
    'c': 'ç',
    'g': 'ğ',
    'i': 'ı',
    'o': 'ö',
    's': 'ş',
    'u': 'ü',
    'C': 'Ç',
    'G': 'Ğ',
    'I': 'İ',
    'O': 'Ö',
    'S': 'Ş',
    'U': 'Ü'
}

def fix_turkish_chars(text):
    """Fix Turkish characters in text based on context"""
    # Common replacements for petition titles
    replacements = {
        'Dilekce': 'Dilekçe',
        'Sikayet': 'Şikayet',
        'Bosanma': 'Boşanma',
        'Talebi': 'Talebi',
        'Davasi': 'Davası',
        'Takibi': 'Takibi',
        'Itiraz': 'İtiraz',
        'Iptali': 'İptali',
        'Iade': 'İade',
        'Icrasi': 'İcrası',
        'Is': 'İş',
        'Ihbar': 'İhbar',
        'Irtifak': 'İrtifak',
        'Ise': 'İşe',
        'Idari': 'İdari',
        'Imza': 'İmza',
        'Ikamet': 'İkamet',
        'Ikametgah': 'İkametgah',
        'Inceleme': 'İnceleme',
        'Ifade': 'İfade',
        'Iflas': 'İflas',
        'Ihale': 'İhale',
        'Ilan': 'İlan',
        'Ilamsiz': 'İlamsız',
        'Ilanli': 'İlanlı',
        'Isim': 'İsim',
        'Isteme': 'İsteme',
        'Istihkak': 'İstihkak',
        'Istinaf': 'İstinaf',
        'Ihtar': 'İhtar',
        'Ihtiyati': 'İhtiyati',
        'Ihtiyac': 'İhtiyaç',
        'Ihtarname': 'İhtarname',
        'Icra': 'İcra',
        'Icra-takibi': 'İcra Takibi',
        'Sirket': 'Şirket',
        'Sikayetci': 'Şikayetçi',
        'Sikayetli': 'Şikayetli',
        'Sahit': 'Şahit',
        'Senet': 'Senet',
        'Sartli': 'Şartlı',
        'Sofor': 'Şoför',
        'Sahsi': 'Şahsi',
        'Sekil': 'Şekil',
        'Sekli': 'Şekli',
        'Guvence': 'Güvence',
        'Gecici': 'Geçici',
        'Gecerlilik': 'Geçerlilik',
        'Gorus': 'Görüş',
        'Gorev': 'Görev',
        'Gonderme': 'Gönderme',
        'Gonderilen': 'Gönderilen',
        'Gozalti': 'Gözaltı',
        'Gozlemci': 'Gözlemci',
        'Gorevli': 'Görevli',
        'Gorevlendirme': 'Görevlendirme',
        'Ogrenme': 'Öğrenme',
        'Ogrenci': 'Öğrenci',
        'Odemeli': 'Ödemeli',
        'Odemekli': 'Ödemekli',
        'Odemesiz': 'Ödemesiz',
        'Odenek': 'Ödenek',
        'Odev': 'Ödev',
        'Ozel': 'Özel',
        'Ozgurluk': 'Özgürlük',
        'Ucret': 'Ücret',
        'Ucretli': 'Ücretli',
        'Ucretsiz': 'Ücretsiz',
        'Ucuncu': 'Üçüncü',
        'Ust': 'Üst',
        'Ustlenme': 'Üstlenme',
        'Ustlendirme': 'Üstlendirme',
        'Cevap': 'Cevap',
        'Cezasi': 'Cezası',
        'Cezali': 'Cezalı',
        'Cekismeli': 'Çekişmeli',
        'Cekisme': 'Çekişme',
        'Cocuk': 'Çocuk',
        'Calisma': 'Çalışma',
        'Calisan': 'Çalışan',
        'Cagri': 'Çağrı',
        'Cagrili': 'Çağrılı',
        'Cifte': 'Çifte',
        'Cikar': 'Çıkar',
        'Cikarma': 'Çıkarma',
        'Ciktisiz': 'Çıktısız',
    }
    
    # Apply replacements
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def fix_file_title(filepath):
    """Fix Turkish characters in h1 title of a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find h1 tag
    match = re.search(r'(<h1>)(.*?)(</h1>)', content)
    if not match:
        return
    
    original_title = match.group(2)
    fixed_title = fix_turkish_chars(original_title)
    
    if original_title != fixed_title:
        # Replace in content
        new_content = content.replace(f'<h1>{original_title}</h1>', f'<h1>{fixed_title}</h1>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Fixed: {filepath}")
        print(f"  '{original_title}' -> '{fixed_title}'")
        return True
    
    return False

def main():
    petition_files = glob.glob('dilekce-*.html')
    
    print(f"Found {len(petition_files)} petition files")
    print()
    
    fixed_count = 0
    for filepath in petition_files:
        try:
            if fix_file_title(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print()
    print(f"Fixed {fixed_count} files")
    print("Done!")

if __name__ == '__main__':
    main()
