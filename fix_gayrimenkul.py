#!/usr/bin/env python3
"""
Fix dilekce-gayrimenkul-satis.html to use standard petition format
"""

import re

# Read the file
with open('dilekce-gayrimenkul-satis.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the head content
head_match = re.search(r'(<head>.*?</head>)', content, re.DOTALL)
head_content = head_match.group(1) if head_match else ''

# Extract header nav
header_match = re.search(r'(<header class="header">.*?</header>)', content, re.DOTALL)
header_html = header_match.group(1) if header_match else ''

# Create the new body structure
new_body = '''<body>
''' + header_html + '''

    <section class="page-banner">
        <div class="container">
            <h1>Asliye Hukuk Mahkemesi Hakimliğine Gayrimenkul Satış Dilekçesi</h1>
        </div>
    </section>

    <section class="content-section">
        <div class="container">
            <div class="petition-preview" id="gayrimenkul-dilekcesi">
                <div class="petition-letter" id="gayrimenkul-dilekcesi-content">
                    <div class="petition-title"><h3>ASLİYE HUKUK MAHKEMESİ HAKİMLİĞİNE</h3></div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Konu :</span>
                        <div class="petition-content">Gayrimenkul satış dilekçesi</div>
                    </div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Satıcı :</span>
                        <div class="petition-content">
                            Adı Soyadı/Unvan: ..........<br>
                            T.C. Kimlik No/Vergi No: ..........<br>
                            Adres: ..........<br>
                            Tel: ..........
                        </div>
                    </div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Alıcı :</span>
                        <div class="petition-content">
                            Adı Soyadı/Unvan: ..........<br>
                            T.C. Kimlik No/Vergi No: ..........<br>
                            Adres: ..........<br>
                            Tel: ..........
                        </div>
                    </div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Gayrimenkul Bilgileri :</span>
                        <div class="petition-content">
                            İl/İlçe: ..........<br>
                            Mahalle: ..........<br>
                            Ada: .......... Parsel: ..........<br>
                            Yüzölçümü: .......... m²<br>
                            Niteliği: .......... (Arsa/Konut/Tarla vb.)<br>
                            Tapu Kaydı: ..........
                        </div>
                    </div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Satış Bedeli :</span>
                        <div class="petition-content">
                            Satış Bedeli: .......... TL<br>
                            Ödeme Şekli: Peşin / Taksitli<br>
                            Peşinat: .......... TL<br>
                            Kalan Tutar: .......... TL
                        </div>
                    </div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Açıklama :</span>
                        <div class="petition-content">
                            Yukarıda bilgileri yer alan gayrimenkulün satış işlemlerinin yapılmasını talep ederim.<br><br>
                            Tapu devri işlemlerinin hızlandırılması için gerekli tüm evraklar tarafımızdan hazırlanmış olup, vergi ve harç yükümlülüklerinin tarafımızca yerine getirileceğini beyan ederim.
                        </div>
                    </div>
                    
                    <div class="petition-section">
                        <span class="petition-label">Talep :</span>
                        <div class="petition-content">
                            1. Gayrimenkulün satış işlemlerinin yapılmasını,<br>
                            2. Tapu devrinin gerçekleştirilmesini,<br>
                            3. Satış bedelinin ödenmesini,<br>
                            4. Masraf ve giderlerin taraflarca karşılanmasını,<br><br>
                            talep ve arz ederim.
                        </div>
                    </div>
                    
                    <div class="petition-signature">
                        <p>.... / .... / 20....</p>
                        <p><strong>Satıcı veya Vekili</strong></p>
                        <p>Adı Soyadı: ..........</p>
                        <p>İmza: ..........</p>
                    </div>
                </div>
            </div>
            <div class="petition-actions">
                <button class="btn btn-secondary" onclick="copyPetition('gayrimenkul-dilekcesi-content')">Kopyala</button>
                <button class="btn btn-primary" onclick="downloadUDF('gayrimenkul-dilekcesi-content')">İndir (UDF)</button>
                <button class="btn btn-primary" onclick="downloadWord('gayrimenkul-dilekcesi-content')">İndir (Word)</button>
            </div>
        </div>
    </section>

    <!-- Bilgi Bölümü -->
    <section class="info-section">
        <div class="container">
            <h2>Gayrimenkul Satış Dilekçesi Hakkında Bilgilendirme</h2>
            <p class="section-description">Bu dilekçe örneği gayrimenkul satış işlemleri için hazırlanmış şablondur.</p>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>📋 Gerekli Evraklar</h3>
                    <ul>
                        <li>Nüfus cüzdanı fotokopisi</li>
                        <li>İkametgah belgesi</li>
                        <li>Tapu fotokopisi</li>
                        <li>Vergi levhası (tüzel kişiler için)</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>💰 Masraflar</h3>
                    <ul>
                        <li>Tapu harcı (%4 - satıcı/alıcı)</li>
                        <li>Döner sermaye ücreti</li>
                        <li>Ekspertiz ücreti</li>
                        <li>Tasdik ücreti</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>⏳ İşlem Süresi</h3>
                    <ul>
                        <li>Normal işlem: 1-3 gün</li>
                        <li>Ekspertiz süreci: 2-5 gün</li>
                        <li>Belediye onayı (varsa): 5-15 gün</li>
                        <li>Toplam süre: 1-4 hafta</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>✅ Önemli Notlar</h3>
                    <ul>
                        <li>İmar durumu kontrol edilmelidir</li>
                        <li>Şerh ve ipotekler sorgulanmalıdır</li>
                        <li>Kat mülkiyeti varsa yönetim onayı gerekir</li>
                        <li>Veraset ilamı varsa tüm mirasçılar katılmalıdır</li>
                    </ul>
                </div>
            </div>

            <div class="warning-box">
                <h4>⚠️ Önemli Uyarı</h4>
                <p>Bu dilekçe örneği genel bilgilendirme amaçlıdır. Gayrimenkul satışlarında ciddi hukuki ve mali riskler bulunabilir. Kesin ve güncel bilgi için mutlaka bir avukata danışmanızı öneririz.</p>
            </div>
        </div>
    </section>

    <!-- SSS Bölümü -->
    <section class="faq-section">
        <div class="container">
            <h2>Sıkça Sorulan Sorular</h2>
            
            <div class="faq-grid">
                <div class="faq-item">
                    <h3>Tapu harcı kim tarafından ödenir?</h3>
                    <p>Tapu harcı satıcı ve alıcı tarafından eşit olarak paylaşılır. Her bir taraf %2 oranında harç öder.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Gayrimenkul satışında vergi var mı?</h3>
                    <p>Evet, satıcı tarafından gayrimenkul sermaye iradı vergisi (GVK 70. md) ödenir. 5 yıldan eski konutlarda istisna uygulanır.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Noter onaylı vekaletle satış yapılabilir mi?</h3>
                    <p>Evet, noter onaylı vekaletnamelerle tapu satışı yapılabilir. Ancak vekaletnamede özel yetki olması gerekir.</p>
                </div>
                
                <div class="faq-item">
                    <h3>İpotekli gayrimenkul satılabilir mi?</h3>
                    <p>Evet, ancak satış bedeli öncelikle ipotekli alacaklıya ödenir veya alıcı ipoteği devralır.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Taşınmaz satış vaadi sözleşmesi nedir?</h3>
                    <p>Gelecekte gayrimenkul satışının yapılacağına dair ön anlaşmadır. Noterden tasdikli olması gerekir.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Kat irtifaklı arsa satılabilir mi?</h3>
                    <p>Evet, kat irtifaklı arsalar satılabilir. Ancak proje onayı ve yapı kullanma izni durumları kontrol edilmelidir.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Özata Hukuk Bürosu</h3>
                    <p>İzmir'in güvenilir hukuk partneri olarak profesyonel avukatlık hizmetleri sunuyoruz.</p>
                </div>
                <div class="footer-section">
                    <h3>Hızlı Bağlantılar</h3>
                    <ul>
                        <li><a href="index.html">Anasayfa</a></li>
                        <li><a href="kurumsal.html">Kurumsal</a></li>
                        <li><a href="calisma-alanlarimiz.html">Çalışma Alanlarımız</a></li>
                        <li><a href="dilekce-ornekleri.html">Dilekçe Örnekleri</a></li>
                        <li><a href="iletisim.html">İletişim</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>İletişim</h3>
                    <p>Email: info@ozatahukuk.av.tr</p>
                    <p>Tel: +90 232 000 00 00</p>
                    <p>Adres: İzmir, Türkiye</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Özata Hukuk. Tüm hakları saklıdır.</p>
            </div>
        </div>
    </footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script>
function downloadUDF(elementId) {
    const petitionContent = document.getElementById(elementId);
    if (!petitionContent) { alert('Dilekçe içeriği bulunamadı!'); return; }
    
    let cleanText = '';
    
    const title = petitionContent.querySelector('.petition-title');
    if (title) cleanText += title.innerText.toUpperCase() + '\\n\\n';
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        if (label) cleanText += label + ' ';
        if (content) cleanText += content + '\\n\\n';
    });
    
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) cleanText += '\\n' + signature.innerText + '\\n';
    
    let elementsXml = '';
    let offset = 0;
    
    const titleEl = petitionContent.querySelector('.petition-title');
    if (titleEl) {
        const titleText = titleEl.innerText.toUpperCase();
        elementsXml += '<paragraph Alignment="1"><content bold="true" startOffset="' + offset + '" length="' + titleText.length + '" /></paragraph>';
        offset += titleText.length;
        elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
        offset += 1;
    }
    
    elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
    offset += 1;
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        
        if (label) {
            elementsXml += '<paragraph><content bold="true" underline="true" startOffset="' + offset + '" length="' + label.length + '" /></paragraph>';
            offset += label.length;
            elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
            offset += 1;
        }
        
        if (content) {
            const contentLines = content.split('\\n');
            contentLines.forEach((line, idx) => {
                if (line.trim()) {
                    elementsXml += '<paragraph><content startOffset="' + offset + '" length="' + line.length + '" /></paragraph>';
                    offset += line.length;
                }
                if (idx < contentLines.length - 1 || label) {
                    elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
                    offset += 1;
                }
            });
        }
        
        elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
        offset += 1;
    });
    
    const sigEl = petitionContent.querySelector('.petition-signature');
    if (sigEl) {
        const sigText = sigEl.innerText;
        elementsXml += '<paragraph Alignment="2"><content startOffset="' + offset + '" length="' + sigText.length + '" /></paragraph>';
        offset += sigText.length;
    }
    
    const contentXml = '<?xml version="1.0" encoding="UTF-8" ?>\\n<template format_id="1.8" >\\n<content><![CDATA[' + cleanText + ']]></content>\\n<properties><pageFormat mediaSizeName="1.8" leftMargin="70.8661413192749" rightMargin="70.8661413192749" topMargin="70.8661413192749" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" /></properties>\\n<elements resolver="hvl-default" >\\n' + elementsXml + '\\n</elements>\\n<styles><style name="hvl-default" family="Times New Roman" size="12" description="Gövde" /></styles>\\n</template>';
    
    const zip = new JSZip();
    zip.file("content.xml", contentXml);
    zip.file("documentproperties.xml", '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd"><properties><entry key="user.gercek"></entry></properties>');
    zip.generateAsync({type: "blob"}).then(function(blob) {
        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = elementId + '.udf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
}

function downloadWord(elementId) {
    const petitionContent = document.getElementById(elementId);
    if (!petitionContent) { alert('Dilekçe içeriği bulunamadı!'); return; }
    
    let rtfBody = '';
    
    const title = petitionContent.querySelector('.petition-title');
    if (title) {
        const titleText = title.innerText.toUpperCase().replace(/[\\\\{}]/g, '\\\\\\\\$&');
        rtfBody += '\\\\pard\\\\qc\\\\b ' + titleText + '\\\\b0\\\\par\\\\par';
    }
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        
        if (label) {
            const labelText = label.replace(/[\\\\{}]/g, '\\\\\\\\$&');
            rtfBody += '\\\\b ' + labelText + '\\\\b0\\\\par';
        }
        
        if (content) {
            const lines = content.split('\\n');
            lines.forEach(line => {
                const lineText = line.replace(/[\\\\{}]/g, '\\\\\\\\$&').trim();
                if (lineText) {
                    rtfBody += lineText + '\\\\par';
                }
            });
        }
        
        rtfBody += '\\\\par';
    });
    
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) {
        rtfBody += '\\\\par';
        const sigLines = signature.innerText.split('\\n');
        rtfBody += '\\\\pard\\\\qr';
        sigLines.forEach(line => {
            const lineText = line.replace(/[\\\\{}]/g, '\\\\\\\\$&').trim();
            if (lineText) {
                rtfBody += lineText + '\\\\par';
            }
        });
        rtfBody += '\\\\pard';
    }
    
    const rtfContent = '{\\\\rtf1\\\\ansi\\\\ansicpg1254\\\\deff0\\\\nouicompat\\\\deflang1055\\\\deflangfe1055{\\\\fonttbl{\\\\f0\\\\fnil\\\\fcharset162 Times New Roman;}}{\\\\*\\\\generator Riched20 10.0.19041}\\\\viewkind4\\uc1 \\\\pard\\plain\\\\fs28\\\\lang1055 ' + rtfBody + '}';
    
    const blob = new Blob([rtfContent], {type: 'application/rtf'});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = elementId + '.rtf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function copyPetition(elementId) {
    const petitionContent = document.getElementById(elementId);
    if (!petitionContent) { alert('Dilekçe içeriği bulunamadı!'); return; }
    
    let fullText = '';
    
    const title = petitionContent.querySelector('.petition-title');
    if (title) fullText += title.innerText.toUpperCase() + '\\n\\n';
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        if (label) fullText += label + '\\n';
        if (content) fullText += content + '\\n\\n';
    });
    
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) fullText += '\\n' + signature.innerText + '\\n';
    
    navigator.clipboard.writeText(fullText).then(() => alert('Dilekçe kopyalandı!'));
}
</script>

</body>
</html>'''

# Extract everything before </head>
head_end = content.find('</head>') + 7
before_head = content[:head_end]

# Create the new complete HTML
new_html = before_head + new_body

# Write the fixed file
with open('dilekce-gayrimenkul-satis.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Fixed dilekce-gayrimenkul-satis.html")
