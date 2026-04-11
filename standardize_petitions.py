#!/usr/bin/env python3
"""
Standardize all petition files to a single template
"""

import os
import re
import glob

# Standard JS functions that work correctly
STANDARD_JS = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
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
            const lines = content.split('\\n');
            lines.forEach((line) => {
                if (line.trim()) {
                    elementsXml += '<paragraph><content startOffset="' + offset + '" length="' + line.length + '" /></paragraph>';
                    offset += line.length;
                }
                elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
                offset += 1;
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
    
    const contentXml = '<?xml version="1.0" encoding="UTF-8" ?>\\n<template format_id="1.8" >\\n<content><![CDATA[' + cleanText + ']]></content>\\n<properties><pageFormat mediaSizeName="1" leftMargin="70.8661413192749" rightMargin="70.8661413192749" topMargin="70.8661413192749" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" /></properties>\\n<elements resolver="hvl-default" >\\n' + elementsXml + '\\n</elements>\\n<styles><style name="hvl-default" family="Times New Roman" size="12" description="Gövde" /></styles>\\n</template>';
    
    const zip = new JSZip();
    zip.file("content.xml", contentXml);
    zip.file("documentproperties.xml", '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd"><properties><entry key="user.gercek"></entry></properties>');
    zip.file("sign.sgn", '<?xml version="1.0" encoding="UTF-8"?><signature-list/>');
    
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
    
    const blob = new Blob(['\\ufeff', fullText], {type: 'application/msword'});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = elementId + '.doc';
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
</script>'''

def extract_petition_data(content, filepath):
    """Extract petition content from existing file"""
    data = {
        'title': '',
        'description': '',
        'keywords': '',
        'page_title': '',
        'petition_html': '',
        'element_id': ''
    }
    
    # Extract title
    match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if match:
        data['page_title'] = match.group(1).strip()
    
    # Extract description
    match = re.search(r'<meta name="description" content="([^"]+)">', content, re.IGNORECASE)
    if match:
        data['description'] = match.group(1)
    
    # Extract keywords
    match = re.search(r'<meta name="keywords" content="([^"]+)">', content, re.IGNORECASE)
    if match:
        data['keywords'] = match.group(1)
    
    # Extract element ID from petition-preview or petition-document
    match = re.search(r'<div class="petition-preview"[^>]*id="([^"]+)"', content)
    if match:
        data['element_id'] = match.group(1)
    else:
        match = re.search(r'<div class="petition-document"[^>]*id="([^"]+)"', content)
        if match:
            data['element_id'] = match.group(1)
    
    # Extract petition content between petition-letter or petition-document divs
    match = re.search(r'class="petition-letter"[^>]*>(.*?)</div>\s*</div>\s*<div class="petition-actions"', content, re.DOTALL)
    if match:
        data['petition_html'] = match.group(1)
    else:
        match = re.search(r'class="petition-document"[^>]*>(.*?)</div>\s*</div>\s*<div class="petition-actions"', content, re.DOTALL)
        if match:
            data['petition_html'] = match.group(1)
    
    # Clean up the petition HTML
    if data['petition_html']:
        # Remove extra whitespace but keep structure
        data['petition_html'] = re.sub(r'\n\s*\n', '\n', data['petition_html'])
        data['petition_html'] = data['petition_html'].strip()
    
    return data

def create_standard_petition(data, filename):
    """Create standardized petition HTML"""
    
    element_id = data['element_id'] if data['element_id'] else 'petition-content'
    
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QYK959FEKW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-QYK959FEKW');
</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{data['description']}">
    <meta name="keywords" content="{data['keywords']}">
    <meta name="author" content="Özata Hukuk Bürosu">
    <title>{data['page_title']}</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="responsive.css">
</head>
<body>
    <header class="header">
        <nav class="nav-container">
            <div class="logo">
                <a href="index.html">
                    <img src="logo.svg" alt="Özata Hukuk Logo" width="75" height="48">
                </a>
            </div>
            <button class="mobile-menu-toggle" aria-label="Menü">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="index.html">Anasayfa</a></li>
                <li class="dropdown">
                    <a href="kurumsal.html">Kurumsal <span>▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="kurumsal.html">Hakkımızda</a></li>
                        <li><a href="ekibimiz.html">Ekibimiz</a></li>
                        <li><a href="sss.html">Sıkça Sorulan Sorular</a></li>
                    </ul>
                </li>
                <li><a href="calisma-alanlari.html">Çalışma Alanlarımız</a></li>
                <li><a href="hesaplamalar.html">Hesaplama Araçları</a></li>
                <li><a href="dilekce-ornekleri.html" class="active">Dilekçe Örnekleri</a></li>
                <li><a href="yayinlar.html">Yayınlar</a></li>
                <li><a href="iletisim.html">İletişim</a></li>
            </ul>
        </nav>
    </header>

    <section class="page-banner">
        <div class="container">
            <h1>{data['page_title'].split('|')[0].strip()}</h1>
        </div>
    </section>

    <section class="content-section">
        <div class="container">
            <div class="petition-preview" id="{element_id}">
                <div class="petition-letter" id="{element_id}-content">
{data['petition_html']}
                </div>
            </div>
            <div class="petition-actions">
                <button class="btn btn-secondary" onclick="copyPetition('{element_id}-content')">Kopyala</button>
                <button class="btn btn-primary" onclick="downloadUDF('{element_id}-content')">İndir (UDF)</button>
                <button class="btn btn-primary" onclick="downloadWord('{element_id}-content')">İndir (Word)</button>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>ÖZATA HUKUK</h4>
                    <p>Profesyonel avukatlık hizmetleri ile hukuki haklarınızı koruyoruz.</p>
                </div>
                <div class="footer-col">
                    <h4>Hızlı Bağlantılar</h4>
                    <ul>
                        <li><a href="index.html">Anasayfa</a></li>
                        <li><a href="dilekce-ornekleri.html">Dilekçe Örnekleri</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>İletişim</h4>
                    <ul>
                        <li><a href="iletisim.html">İletişim Formu</a></li>
                        <li><a href="tel:+905325273993">0 (532) 527 39 93</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Özata Hukuk. Tüm hakları saklıdır.</p>
            </div>
        </div>
    </footer>

{STANDARD_JS}

</body>
</html>'''
    
    return html

def standardize_petition_file(filepath):
    """Standardize a single petition file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract data
        data = extract_petition_data(content, filepath)
        
        if not data['petition_html']:
            print(f"Skipping {filepath} - could not extract petition content")
            return False
        
        # Create new standardized HTML
        new_html = create_standard_petition(data, filepath)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"Standardized: {filepath}")
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    petition_files = glob.glob('dilekce-*.html')
    petition_files = [f for f in petition_files if f != 'dilekce-ornekleri.html']
    
    print(f"Found {len(petition_files)} petition files to standardize")
    print()
    
    success_count = 0
    for filepath in petition_files:
        if standardize_petition_file(filepath):
            success_count += 1
    
    print()
    print(f"Successfully standardized {success_count}/{len(petition_files)} files")
    print("Done!")

if __name__ == '__main__':
    main()
