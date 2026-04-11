#!/usr/bin/env python3
"""
Add info sections, warning boxes, and FAQ sections to petition files
"""

import os
import re
import glob

def get_info_section(title):
    """Generate info section HTML"""
    return f'''
    <!-- Bilgi Bölümü -->
    <section class="info-section">
        <div class="container">
            <h2>{title} Hakkında Bilgilendirme</h2>
            <p class="section-description">Bu dilekçe örneği hukuki başvurularınız için hazırlanmış şablondur.</p>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>📝 Dilekçe Nedir?</h3>
                    <ul>
                        <li>Resmi başvuru aracıdır</li>
                        <li>Hukuki hakların kullanılmasını sağlar</li>
                        <li>Usul kurallarına uygun hazırlanmalıdır</li>
                        <li>İmza ve tarih içermelidir</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>⚖️ Hukuki Dayanak</h3>
                    <ul>
                        <li>İlgili kanun maddeleri</li>
                        <li>Yönetmelik hükümleri</li>
                        <li>İçtihatlar</li>
                        <li>Genelge ve tebliğler</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>⏰ Önemli Süreler</h3>
                    <ul>
                        <li>Zaman aşımı süreleri</li>
                        <li>Hak düşürücü süreler</li>
                        <li>İtiraz süreleri</li>
                        <li>Kanuni süreler</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>✅ Dikkat Edilmesi Gerekenler</h3>
                    <ul>
                        <li>Kişisel bilgilerin doğruluğu</li>
                        <li>Hukuki dayanakların gösterilmesi</li>
                        <li>Eklerin tamamlanması</li>
                        <li>Yetkili merci kontrolü</li>
                    </ul>
                </div>
            </div>

            <div class="warning-box">
                <h4>⚠️ Önemli Uyarı</h4>
                <p>Bu dilekçe örneği genel bilgilendirme amaçlıdır. Her hukuki durum farklılık gösterebilir. Kesin ve güncel bilgi için mutlaka bir avukata danışmanızı öneririz. Yanlış veya eksik başvuru hakkınızın kaybına neden olabilir.</p>
            </div>
        </div>
    </section>
'''

def get_faq_section():
    """Generate FAQ section HTML"""
    return '''
    <!-- SSS Bölümü -->
    <section class="faq-section">
        <div class="container">
            <h2>Sıkça Sorulan Sorular</h2>
            
            <div class="faq-grid">
                <div class="faq-item">
                    <h3>Dilekçe ücretli mi?</h3>
                    <p>Dilekçelerin kendisi ücretsizdir. Ancak bazı başvurular harç ve masrafa tabidir. Harç miktarları ilgili tarifelerde belirtilir.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Dilekçeye cevap ne zaman verilir?</h3>
                    <p>Cevap süreleri başvuru türüne göre değişir. İdari başvurularda 30 gün, icra takiplerinde 7 gün, mahkeme dilekçelerinde genellikle 2 haftadır.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Dilekçe elden verilebilir mi?</h3>
                    <p>Evet, dilekçeler elden teslim edilebilir. Teslim edildiğinde kayıt numarası alınmalıdır. Posta veya elektronik ortamda da gönderilebilir.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Vekaletsiz dilekçe verilebilir mi?</h3>
                    <p>Kişiler kendi adlarına vekaletsiz başvuru yapabilir. Ancak tüzel kişiler veya başkası adına başvuru için vekaletname gerekir.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Yanlış dilekçe verilirse ne olur?</h3>
                    <p>Yanlış veya eksik dilekçeler usulden reddedilebilir veya iade edilebilir. Bu, zaman aşımı ve hak kaybına neden olabilir.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Hangi belgeler eklenmeli?</h3>
                    <p>Dilekçeye göre değişir. Genellikle kimlik fotokopisi, ikametgah belgesi, ilgili sözleşme/fatura ve diğer deliller eklenir.</p>
                </div>
            </div>
        </div>
    </section>
'''

def add_sections_to_file(filepath):
    """Add info and FAQ sections to a petition file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from page
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    title = title_match.group(1) if title_match else 'Dilekçe'
    
    # Check if already has info-section
    if 'class="info-section"' in content:
        print(f"Skipping {filepath} - already has info section")
        return
    
    # Find the position to insert (before footer)
    # Insert after </section> of content-section but before footer
    pattern = r'(</section>\s*)(<footer class="footer">)'
    
    info_section = get_info_section(title)
    faq_section = get_faq_section()
    
    replacement = r'\1' + info_section + faq_section + r'\2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        # Try alternative pattern
        pattern2 = r'(</div>\s*</section>\s*)(<footer)'
        replacement2 = r'\1' + info_section + faq_section + r'\2'
        new_content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added sections to: {filepath}")

def main():
    petition_files = glob.glob('dilekce-*.html')
    petition_files = [f for f in petition_files if f != 'dilekce-ornekleri.html']
    
    print(f"Found {len(petition_files)} petition files to process")
    print()
    
    for filepath in petition_files:
        try:
            add_sections_to_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print()
    print("Done!")

if __name__ == '__main__':
    main()
