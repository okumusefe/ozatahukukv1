#!/usr/bin/env python3
"""
Standardize all petition files to have identical CSS and JS structure
"""

import glob
import re

def standardize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from h1
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    title = title_match.group(1) if title_match else 'Dilekçe'
    
    # Extract content ID
    id_match = re.search(r'id="([\w-]+-content)"', content)
    content_id = id_match.group(1) if id_match else 'dilekce-content'
    base_id = content_id.replace('-content', '')
    
    # Extract petition letter content
    letter_match = re.search(r'<div class="petition-letter"[^>]*>(.*?)</div>\s*</div>\s*<div class="petition-actions">', content, re.DOTALL)
    if letter_match:
        letter_content = letter_match.group(1)
    else:
        letter_content = '<div class="petition-title"><h3>DİLEKÇE</h3></div><div class="petition-section"><span class="petition-label">Konu :</span><div class="petition-content">Dilekçe konusu</div></div>'
    
    # Build standardized HTML
    std_html = f'''<!DOCTYPE html>
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
<title>{title} | Özata Hukuk Bürosu</title>
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
<a href="kurumsal.html">Kurumsal</a>
</li>
<li class="dropdown">
<a href="calisma-alanlarimiz.html">Çalışma Alanlarımız</a>
</li>
<li><a href="dilekce-ornekleri.html">Dilekçe Örnekleri</a></li>
<li><a href="iletisim.html">İletişim</a></li>
</ul>
</nav>
</header>

<section class="page-banner">
<div class="container">
<h1>{title}</h1>
</div>
</section>

<section class="content-section">
<div class="container">
<div class="petition-preview" id="{base_id}">
<div class="petition-letter" id="{content_id}">
{letter_content}
</div>
</div>
<div class="petition-actions">
<button class="btn btn-secondary" onclick="copyPetition('{content_id}')">Kopyala</button>
<button class="btn btn-primary" onclick="downloadUDF('{content_id}')">İndir (UDF)</button>
<button class="btn btn-primary" onclick="downloadWord('{content_id}')">İndir (Word)</button>
</div>
</div>
</section>

<section class="info-section">
<div class="container">
<h2>{title} Hakkında Bilgilendirme</h2>
<div class="info-grid">
<div class="info-card">
<h3>Dilekçe Nedir?</h3>
<ul>
<li>Resmi başvuru aracıdır</li>
<li>Hukuki hakların kullanılmasını sağlar</li>
</ul>
</div>
</div>
</div>
</section>

<footer class="footer">
<div class="container">
<p>&copy; 2026 Özata Hukuk. Tüm hakları saklıdır.</p>
</div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script>
function downloadUDF(elementId) {{
    const petitionContent = document.getElementById(elementId);
    if (!petitionContent) {{ alert('Dilekçe içeriği bulunamadı!'); return; }}
    
    let cleanText = '';
    
    const title = petitionContent.querySelector('.petition-title');
    if (title) cleanText += title.innerText.toUpperCase() + '\n\n';
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {{
        const label = section.querySelector('.petition-label').innerText;
        const content = section.querySelector('.petition-content').innerText;
        if (label) cleanText += label + ' ';
        if (content) cleanText += content + '\n\n';
    }});
    
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) cleanText += '\n' + signature.innerText + '\n';
    
    let elementsXml = '';
    let offset = 0;
    
    const titleEl = petitionContent.querySelector('.petition-title');
    if (titleEl) {{
        const titleText = titleEl.innerText.toUpperCase();
        elementsXml += '<paragraph Alignment="1"><content bold="true" startOffset="' + offset + '" length="' + titleText.length + '" /></paragraph>';
        offset += titleText.length;
        elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
        offset += 1;
    }}
    
    elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
    offset += 1;
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {{
        const label = section.querySelector('.petition-label').innerText;
        const content = section.querySelector('.petition-content').innerText;
        
        if (label) {{
            elementsXml += '<paragraph><content bold="true" underline="true" startOffset="' + offset + '" length="' + label.length + '" /></paragraph>';
            offset += label.length;
            elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
            offset += 1;
        }}
        
        if (content) {{
            const lines = content.split('\n');
            lines.forEach((line) => {{
                if (line.trim()) {{
                    elementsXml += '<paragraph><content startOffset="' + offset + '" length="' + line.length + '" /></paragraph>';
                    offset += line.length;
                }}
                elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
                offset += 1;
            }});
        }}
        
        elementsXml += '<paragraph><content startOffset="' + offset + '" length="1" /></paragraph>';
        offset += 1;
    }});
    
    const sigEl = petitionContent.querySelector('.petition-signature');
    if (sigEl) {{
        const sigText = sigEl.innerText;
        elementsXml += '<paragraph Alignment="2"><content startOffset="' + offset + '" length="' + sigText.length + '" /></paragraph>';
        offset += sigText.length;
    }}
    
    const contentXml = '<?xml version="1.0" encoding="UTF-8" ?>\n<template format_id="1.8" >\n<content><![CDATA[' + cleanText + ']]></content>\n<properties><pageFormat mediaSizeName="1" leftMargin="70.8661413192749" rightMargin="70.8661413192749" topMargin="70.8661413192749" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" /></properties>\n<elements resolver="hvl-default" >\n' + elementsXml + '\n</elements>\n<styles><style name="hvl-default" family="Times New Roman" size="12" description="Gövde" /></styles>\n</template>';
    
    const zip = new JSZip();
    zip.file("content.xml", contentXml);
    zip.file("documentproperties.xml", '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd"><properties><entry key="user.gercek"></entry></properties>');
    zip.generateAsync({{type: "blob"}}).then(function(blob) {{
        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = elementId + '.udf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }});
}}

function downloadWord(elementId) {{
    const petitionContent = document.getElementById(elementId);
    if (!petitionContent) {{ alert('Dilekçe içeriği bulunamadı!'); return; }}
    
    let fullText = '';
    
    const title = petitionContent.querySelector('.petition-title');
    if (title) fullText += title.innerText.toUpperCase() + '\n\n';
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {{
        const label = section.querySelector('.petition-label').innerText;
        const content = section.querySelector('.petition-content').innerText;
        if (label) fullText += label + '\n';
        if (content) fullText += content + '\n\n';
    }});
    
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) fullText += '\n' + signature.innerText + '\n';
    
    const blob = new Blob(['\ufeff', fullText], {{type: 'application/msword'}});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = elementId + '.doc';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}}

function copyPetition(elementId) {{
    const petitionContent = document.getElementById(elementId);
    if (!petitionContent) {{ alert('Dilekçe içeriği bulunamadı!'); return; }}
    
    let fullText = '';
    
    const title = petitionContent.querySelector('.petition-title');
    if (title) fullText += title.innerText.toUpperCase() + '\n\n';
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {{
        const label = section.querySelector('.petition-label').innerText;
        const content = section.querySelector('.petition-content').innerText;
        if (label) fullText += label + '\n';
        if (content) fullText += content + '\n\n';
    }});
    
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) fullText += '\n' + signature.innerText + '\n';
    
    navigator.clipboard.writeText(fullText).then(() => alert('Dilekçe kopyalandı!'));
}}
</script>

</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(std_html)
    
    print(f'Standardized: {filepath}')

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if 'ornekleri' not in f]
    
    for f in files:
        try:
            standardize_file(f)
        except Exception as e:
            print(f'Error {f}: {e}')
    
    print('Done!')

if __name__ == '__main__':
    main()
