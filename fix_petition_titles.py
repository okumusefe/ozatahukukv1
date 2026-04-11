#!/usr/bin/env python3
"""
Fix petition titles with proper legal Turkish terminology
Based on standard Turkish legal practice and proper court/prosecutor naming conventions
"""

import os
import re
import glob

# Proper legal petition titles based on petition type
# Format: filename pattern -> (h1_title, petition_title_in_letter)
PETITION_TITLES = {
    'dilekce-savcilik-sikayet.html': ('Cumhuriyet Savcılığına Şikayet Dilekçesi', '...SAVCILIĞINA (SULH CEZA HAKİMLİĞİNE)'),
    'dilekce-alacak-davasi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Alacak Davası Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-icra-takibi.html': ('İcra Dairesi Müdürlüğüne İcra Takibi Dilekçesi', 'İCRA DAİRESİ MÜDÜRLÜĞÜNE'),
    'dilekce-icra-takibi-yazili.html': ('İcra Dairesi Müdürlüğüne Yazılı İcra Takibi Dilekçesi', 'İCRA DAİRESİ MÜDÜRLÜĞÜNE'),
    'dilekce-icra-itiraz.html': ('İcra Dairesi Müdürlüğüne İtiraz Dilekçesi', 'İCRA DAİRESİ MÜDÜRLÜĞÜNE'),
    'dilekce-haciz-kaldirma.html': ('İcra Dairesi Müdürlüğüne Haciz Kaldırma Dilekçesi', 'İCRA DAİRESİ MÜDÜRLÜĞÜNE'),
    'dilekce-nafaka-talebi.html': ('Aile Mahkemesi Hakimliğine Nafaka Talebi Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-nafaka-artirimi.html': ('Aile Mahkemesi Hakimliğine Nafaka Artırımı Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-nafaka-icrasi.html': ('İcra Dairesi Müdürlüğüne Nafaka İcrası Dilekçesi', 'İCRA DAİRESİ MÜDÜRLÜĞÜNE'),
    'dilekce-yoksulluk-nafakasi-iptali.html': ('Aile Mahkemesi Hakimliğine Yoksulluk Nafakası İptali Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-tedbir-nafakasi.html': ('Aile Mahkemesi Hakimliğine Tedbir Nafakası Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-anlasmali-bosanma.html': ('Aile Mahkemesi Hakimliğine Anlaşmalı Boşanma Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-cekismeli-bosanma.html': ('Aile Mahkemesi Hakimliğine Çekişmeli Boşanma Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-bosanma-protokolu.html': ('Aile Mahkemesi Hakimliğine Boşanma Protokolü Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-ailenin-korunmasi.html': ('Aile Mahkemesi Hakimliğine Ailenin Korunması Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-velayet-degistirme.html': ('Aile Mahkemesi Hakimliğine Velayet Değiştirme Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-esya-ayriligi.html': ('Aile Mahkemesi Hakimliğine Eşya Ayrılığı Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-babalik-davasi.html': ('Aile Mahkemesi Hakimliğine Babalık Davası Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-evliligin-butlani.html': ('Aile Mahkemesi Hakimliğine Evliliğin Butlanı Dilekçesi', 'AİLE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-miras-tenfiz.html': ('Sulh Hukuk Mahkemesi Hakimliğine Miras Tenfiz Dilekçesi', 'SULH HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-veraset-ilami.html': ('Sulh Hukuk Mahkemesi Hakimliğine Veraset İlamı Dilekçesi', 'SULH HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-mal-rejimi-tasfiyesi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Mal Rejimi Tasfiyesi Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-ise-iade.html': ('İş Mahkemesi Hakimliğine İşe İade Dilekçesi', 'İŞ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-kidem-tazminati.html': ('İş Mahkemesi Hakimliğine Kıdem Tazminatı Dilekçesi', 'İŞ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-ihbar-tazminati.html': ('İş Mahkemesi Hakimliğine İhbar Tazminatı Dilekçesi', 'İŞ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-fazla-mesai.html': ('İş Mahkemesi Hakimliğine Fazla Mesai Dilekçesi', 'İŞ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-is-kazasi.html': ('İş Mahkemesi Hakimliğine İş Kazası Dilekçesi', 'İŞ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-cep-tazminat.html': ('İş Mahkemesi Hakimliğine Cep Tazminatı Dilekçesi', 'İŞ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-is-kurtulus.html': ('Asliye Ticaret Mahkemesi Hakimliğine İş Kurtuluşu (Konkordato) Dilekçesi', 'ASLİYE TİCARET MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-ticari-alacak.html': ('Asliye Ticaret Mahkemesi Hakimliğine Ticari Alacak Dilekçesi', 'ASLİYE TİCARET MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-sirket-kurulus.html': ('Ticaret Sicili Müdürlüğüne Şirket Kuruluş Dilekçesi', 'TİCARET SİCİLİ MÜDÜRLÜĞÜNE'),
    'dilekce-satis-vaadi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Satış Vaadi Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-konut-satisi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Konut Satışı Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-gayrimenkul-satis.html': ('Asliye Hukuk Mahkemesi Hakimliğine Gayrimenkul Satış Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-kira-artisi-tufe.html': ('Asliye Hukuk Mahkemesi Hakimliğine Kira Artışı (TÜFE) Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-kiraci-tahliyesi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Kiracı Tahliyesi Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-kiraya-veren-haklari.html': ('Asliye Hukuk Mahkemesi Hakimliğine Kiraya Veren Hakları Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-tasinmaz-kirasi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Taşınmaz Kirası Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-tapu-iptali.html': ('Asliye Hukuk Mahkemesi Hakimliğine Tapu İptali Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-irtifak-hakki.html': ('Asliye Hukuk Mahkemesi Hakimliğine İrtifak Hakkı Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-kamulastirmasiz-el-atma.html': ('Asliye Hukuk Mahkemesi Hakimliğine Kamulaştırmasız El Atma Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-mudahalenin-meni.html': ('Asliye Hukuk Mahkemesi Hakimliğine Müdahalenin Meni Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-menfi-tespit.html': ('Asliye Hukuk Mahkemesi Hakimliğine Menfi Tespit Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-haksiz-fiil.html': ('Asliye Hukuk Mahkemesi Hakimliğine Haksız Fiil Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-idari-iptal.html': ('İdare Mahkemesi Hakimliğine İptal Dava Dilekçesi', 'İDARE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-idari-para-cezasi.html': ('İdare Mahkemesi Hakimliğine İdari Para Cezası Dilekçesi', 'İDARE MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-bank-kredi-iptali.html': ('Tüketici Mahkemesi Hakimliğine Banka Kredi İptali Dilekçesi', 'TÜKETİCİ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-tuketici-iptali.html': ('Tüketici Mahkemesi Hakimliğine Tüketici İptali Dilekçesi', 'TÜKETİCİ MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-tuketici-hakem.html': ('Hakem Heyetine Tüketici Başvurusu Dilekçesi', 'HAKEM HEYETİ BAŞKANLIĞINA'),
    'dilekce-senet-protesto.html': ('Asliye Ticaret Mahkemesi Hakimliğine Senet Protestosu Dilekçesi', 'ASLİYE TİCARET MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-davaya-cevap.html': ('Asliye Hukuk Mahkemesi Hakimliğine Cevap Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-davadan-feragat.html': ('Asliye Hukuk Mahkemesi Hakimliğine Feragat Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-yapilandirma-basvuru.html': ('Vergi Dairesi Müdürlüğüne Yapılandırma Başvuru Dilekçesi', 'VERGİ DAİRESİ MÜDÜRLÜĞÜNE'),
    'dilekce-sgk-iptali.html': ('SGK İl Müdürlüğüne İptal Dilekçesi', 'SOSYAL GÜVENLİK KURUMU İL MÜDÜRLÜĞÜNE'),
    'dilekce-mesleki-yeterlilik.html': ('Mesleki Yeterlilik Kurumuna Başvuru Dilekçesi', 'MESLEKİ YETERLİLİK KURUMU BAŞKANLIĞINA'),
    'dilekce-marka-tescil.html': ('Türk Patent ve Marka Kurumuna Tescil Dilekçesi', 'TÜRK PATENT VE MARKA KURUMU BAŞKANLIĞINA'),
    'dilekce-patent-basvuru.html': ('Türk Patent ve Marka Kurumuna Patent Başvuru Dilekçesi', 'TÜRK PATENT VE MARKA KURUMU BAŞKANLIĞINA'),
    'dilekce-avukat-vekil-name.html': ('Baro Başkanlığına Vekilname Dilekçesi', 'BARO BAŞKANLIĞINA'),
    'dilekce-yillik-izin-icrasi.html': ('Asliye Hukuk Mahkemesi Hakimliğine Yıllık İzin İcrası Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
    'dilekce-red Ve-ihtiyati-tedbir.html': ('Asliye Hukuk Mahkemesi Hakimliğine Red ve İhtiyati Tedbir Dilekçesi', 'ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE'),
}

def fix_petition_file(filepath):
    """Fix titles in a petition file"""
    filename = os.path.basename(filepath)
    
    if filename not in PETITION_TITLES:
        print(f"Skipping {filename} - no mapping found")
        return False
    
    h1_title, letter_title = PETITION_TITLES[filename]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix h1 title
    content = re.sub(r'(<h1>)(.*?)(</h1>)', f'\\g<1>{h1_title}\\g<3>', content, count=1)
    
    # Fix petition letter title (petition-title div)
    # Look for patterns like: <div class="petition-title">...MAHKEMESİNE/DAİRESİNE...</div>
    old_title_match = re.search(r'<div class="petition-title">(.*?)</div>', content, re.DOTALL)
    if old_title_match:
        old_title_content = old_title_match.group(1)
        # Replace with proper title, keeping any h3 tags if present
        if '<h3>' in old_title_content:
            new_title = f'<h3>{letter_title}</h3>'
        else:
            new_title = letter_title
        content = content.replace(old_title_match.group(0), f'<div class="petition-title">{new_title}</div>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {filename}")
    print(f"  Page title: {h1_title}")
    print(f"  Letter title: {letter_title}")
    return True

def main():
    petition_files = glob.glob('dilekce-*.html')
    petition_files = [f for f in petition_files if f != 'dilekce-ornekleri.html']
    
    print(f"Found {len(petition_files)} petition files")
    print(f"Have mappings for {len(PETITION_TITLES)} files")
    print()
    
    fixed_count = 0
    for filepath in petition_files:
        try:
            if fix_petition_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print(f"Fixed {fixed_count} files")
    print("Done!")

if __name__ == '__main__':
    main()
