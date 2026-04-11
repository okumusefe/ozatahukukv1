#!/usr/bin/env python3
"""
Fix download functions to include complete petition content
"""

import os
import re
import glob

def get_download_functions(element_id, petition_name, filename_base):
    """Generate proper download functions with escaped newlines"""
    
    js_code = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

<!-- Dilekçe İndirme Fonksiyonları -->
<script>
async function downloadUDF(elementId) {
    const petitionContent = document.getElementById(elementId).querySelector('.petition-letter');
    if (!petitionContent) {
        alert('Dilekçe içeriği bulunamadı!');
        return;
    }
    
    // Tam metni topla
    let fullText = '';
    
    // Başlık
    const title = petitionContent.querySelector('.petition-title');
    if (title) fullText += title.innerText.toUpperCase() + "\\n\\n";
    
    // Tüm section'ları topla
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        if (label) fullText += label + "\\n";
        if (content) fullText += content + "\\n\\n";
    });
    
    // Ek içerikler (section dışındaki petition-content'ler)
    petitionContent.querySelectorAll('.petition-content').forEach(content => {
        if (!content.closest('.petition-section')) {
            fullText += content.innerText + "\\n\\n";
        }
    });
    
    // İmza
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) fullText += "\\n" + signature.innerText + "\\n";
    
    // Elements oluştur
    let elementsXml = '';
    let offset = 0;
    
    // Başlık
    const titleEl = petitionContent.querySelector('.petition-title');
    if (titleEl) {
        const titleText = titleEl.innerText.toUpperCase();
        elementsXml += `<paragraph Alignment="1"><content bold="true" startOffset="${offset}" length="${titleText.length}" /></paragraph>`;
        offset += titleText.length;
        elementsXml += `<paragraph><content startOffset="${offset}" length="1" /></paragraph>`;
        offset += 1;
    }
    
    // Boş satır
    elementsXml += `<paragraph><content startOffset="${offset}" length="1" /></paragraph>`;
    offset += 1;
    
    // Sectionlar
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        
        if (label) {
            elementsXml += `<paragraph><content bold="true" underline="true" startOffset="${offset}" length="${label.length}" /></paragraph>`;
            offset += label.length;
            elementsXml += `<paragraph><content startOffset="${offset}" length="1" /></paragraph>`;
            offset += 1;
        }
        
        if (content) {
            const lines = content.split(/\\r?\\n/);
            lines.forEach((line, idx) => {
                if (line.trim()) {
                    elementsXml += `<paragraph><content startOffset="${offset}" length="${line.length}" /></paragraph>`;
                    offset += line.length;
                }
                elementsXml += `<paragraph><content startOffset="${offset}" length="1" /></paragraph>`;
                offset += 1;
            });
        }
        
        // Boş satır section sonu
        elementsXml += `<paragraph><content startOffset="${offset}" length="1" /></paragraph>`;
        offset += 1;
    });
    
    // İmza
    const sigEl = petitionContent.querySelector('.petition-signature');
    if (sigEl) {
        const sigText = sigEl.innerText;
        elementsXml += `<paragraph Alignment="2"><content startOffset="${offset}" length="${sigText.length}" /></paragraph>`;
        offset += sigText.length;
    }
    
    const contentXml = `<?xml version="1.0" encoding="UTF-8" ?>\\n<template format_id="1.8" >\\n<content><![CDATA[${fullText}]]></content>\\n<properties><pageFormat mediaSizeName="1" leftMargin="70.8661413192749" rightMargin="70.8661413192749" topMargin="70.8661413192749" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" /></properties>\\n<elements resolver="hvl-default" >\\n${elementsXml}\\n</elements>\\n<styles><style name="hvl-default" family="Times New Roman" size="12" description="Gövde" /></styles>\\n</template>`;
    
    const zip = new JSZip();
    zip.file("content.xml", contentXml);
    zip.file("documentproperties.xml", `<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd"><properties><entry key="user.gercek"></entry></properties>`);
    zip.file("sign.sgn", `<?xml version="1.0" encoding="UTF-8"?><signature-list/>`);
    
    const blob = await zip.generateAsync({type: "blob"});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = ''' + f"'{filename_base}.udf';" + '''
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function downloadWord(elementId) {
    const petitionContent = document.getElementById(elementId).querySelector('.petition-letter');
    if (!petitionContent) {
        alert('Dilekçe içeriği bulunamadı!');
        return;
    }
    
    // Tüm içeriği al
    let fullText = '';
    
    // Başlık
    const title = petitionContent.querySelector('.petition-title');
    if (title) fullText += title.innerText.toUpperCase() + "\\n\\n";
    
    // Tüm section'lar
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        if (label) fullText += label + "\\n";
        if (content) fullText += content + "\\n\\n";
    });
    
    // Ek içerikler
    petitionContent.querySelectorAll('.petition-content').forEach(content => {
        if (!content.closest('.petition-section')) {
            fullText += content.innerText + "\\n\\n";
        }
    });
    
    // İmza
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) fullText += "\\n" + signature.innerText + "\\n";
    
    const blob = new Blob(["\\ufeff", fullText], {type: 'application/msword'});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = ''' + f"'{filename_base}.doc';" + '''
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function copyPetition(elementId) {
    const petitionContent = document.getElementById(elementId).querySelector('.petition-letter');
    if (!petitionContent) {
        alert('Dilekçe içeriği bulunamadı!');
        return;
    }
    
    let fullText = '';
    
    // Başlık
    const title = petitionContent.querySelector('.petition-title');
    if (title) fullText += title.innerText.toUpperCase() + "\\n\\n";
    
    // Tüm section'lar
    petitionContent.querySelectorAll('.petition-section').forEach(section => {
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        if (label) fullText += label + "\\n";
        if (content) fullText += content + "\\n\\n";
    });
    
    // Ek içerikler
    petitionContent.querySelectorAll('.petition-content').forEach(content => {
        if (!content.closest('.petition-section')) {
            fullText += content.innerText + "\\n\\n";
        }
    });
    
    // İmza
    const signature = petitionContent.querySelector('.petition-signature');
    if (signature) fullText += "\\n" + signature.innerText + "\\n";
    
    navigator.clipboard.writeText(fullText).then(() => alert('Dilekçe kopyalandı!'));
}
</script>'''
    
    return js_code

def extract_info(content):
    """Extract element_id and filename from content"""
    # Extract element id
    match = re.search(r'<div class="petition-preview" id="([^"]+)"', content)
    element_id = match.group(1) if match else "petition-content"
    
    # Extract title for filename
    match = re.search(r'<title>(.*?)\s*\|', content)
    title = match.group(1).strip() if match else "dilekce"
    filename_base = title.lower().replace(' ', '-').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
    
    return element_id, filename_base

def fix_petition_file(filepath):
    """Fix a single petition file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has correct structure
    if '// Tam metni topla' in content:
        print(f"Skipping {filepath} - already has correct functions")
        return
    
    # Extract info
    element_id, filename_base = extract_info(content)
    
    # Remove old malformed JS
    old_js_pattern = r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jszip[^<]*</script>\s*<!-- Dilekçe İndirme Fonksiyonları -->\s*<script>.*?</script>'
    content = re.sub(old_js_pattern, '', content, flags=re.DOTALL)
    
    # Also remove old pattern without comment
    old_js_pattern2 = r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jszip[^<]*</script>\s*<script>.*?</script>'
    content = re.sub(old_js_pattern2, '', content, flags=re.DOTALL)
    
    # Get new functions
    new_js = get_download_functions(element_id, "", filename_base)
    
    # Insert before </body>
    content = content.replace('</body>', new_js + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

def main():
    petition_files = glob.glob('dilekce-*.html')
    petition_files = [f for f in petition_files if f != 'dilekce-ornekleri.html']
    
    print(f"Found {len(petition_files)} petition files to process")
    
    for filepath in petition_files:
        try:
            fix_petition_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            import traceback
            traceback.print_exc()
    
    print("Done!")

if __name__ == '__main__':
    main()
