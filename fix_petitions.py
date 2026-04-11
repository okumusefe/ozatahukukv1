#!/usr/bin/env python3
"""
Fix all petition files - correct JavaScript functions and structure
"""

import os
import re
import glob

def extract_petition_name(content):
    """Extract petition name from title"""
    title_match = re.search(r'<title>(.*?)\s*\|', content)
    if title_match:
        return title_match.group(1).strip()
    return "Dilekçe"

def extract_element_id(content):
    """Extract petition element ID from content"""
    match = re.search(r'div class="petition-preview" id="([^"]+)"', content)
    if match:
        return match.group(1)
    return "petition-content"

def extract_filename_from_download(content):
    """Extract filename from download functions"""
    match = re.search(r'a\.download = [\'"]([^\'"]+)[\'"]', content)
    if match:
        return match.group(1).replace('.udf', '').replace('.doc', '')
    return None

def fix_petition_file(filepath):
    """Fix a single petition file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has proper structure already
    if '<!-- Dilekçe İndirme Fonksiyonları -->' in content:
        print(f"Skipping {filepath} - already has correct structure")
        return
    
    # Extract key info
    petition_name = extract_petition_name(content)
    element_id = extract_element_id(content)
    filename_base = extract_filename_from_download(content) or element_id
    
    # Find where petition actions section ends
    petition_actions_match = re.search(
        r'(<div class="petition-actions">.*?</div>\s*</article>\s*</div>\s*</section>)', 
        content, 
        re.DOTALL
    )
    
    if not petition_actions_match:
        print(f"Could not find petition-actions in {filepath}")
        return
    
    # The new JavaScript functions to insert
    jszip_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>'
    
    # Clean download functions (without search modal inside)
    download_functions = f'''
<!-- Dilekçe İndirme Fonksiyonları -->
<script>
async function downloadUDF(elementId) {{
    const petitionContent = document.getElementById(elementId).querySelector('.petition-letter');
    if (!petitionContent) {{
        alert('Dilekçe içeriği bulunamadı!');
        return;
    }}
    
    let fullText = '';
    petitionContent.querySelectorAll('.petition-title, .petition-section, .petition-content, .petition-signature').forEach(el => {{ 
        fullText += el.innerText + '\n'; 
    }});
    
    let elementsXml = ''; 
    let offset = 0;
    
    const titleEl = petitionContent.querySelector('.petition-title');
    if (titleEl) {{
        const titleLines = titleEl.innerText.toUpperCase().split('\n');
        titleLines.forEach(line => {{
            if (line.trim()) {{ 
                elementsXml += `<paragraph Alignment="1"><content bold="true" startOffset="${{offset}}" length="${{line.length}}" /></paragraph>`; 
                offset += line.length; 
            }}
            elementsXml += `<paragraph><content startOffset="${{offset}}" length="1" /></paragraph>`; 
            offset += 1;
        }});
    }}
    
    elementsXml += `<paragraph><content startOffset="${{offset}}" length="1" /></paragraph>`; 
    offset += 1;
    
    petitionContent.querySelectorAll('.petition-section').forEach(section => {{
        const label = section.querySelector('.petition-label')?.innerText || '';
        const content = section.querySelector('.petition-content')?.innerText || '';
        
        if (label) {{ 
            elementsXml += `<paragraph><content bold="true" underline="true" startOffset="${{offset}}" length="${{label.length}}" /></paragraph>`; 
            offset += label.length; 
            elementsXml += `<paragraph><content startOffset="${{offset}}" length="1" /></paragraph>`; 
            offset += 1; 
        }}
        
        if (content) {{
            const contentLines = content.split('\n');
            contentLines.forEach((line, idx) => {{
                if (line.trim()) {{ 
                    elementsXml += `<paragraph><content startOffset="${{offset}}" length="${{line.length}}" /></paragraph>`; 
                    offset += line.length; 
                }}
                if (idx < contentLines.length - 1 || label) {{ 
                    elementsXml += `<paragraph><content startOffset="${{offset}}" length="1" /></paragraph>`; 
                    offset += 1; 
                }}
            }});
        }}
        
        elementsXml += `<paragraph><content startOffset="${{offset}}" length="1" /></paragraph>`; 
        offset += 1;
    }});
    
    const sigEl = petitionContent.querySelector('.petition-signature');
    if (sigEl) {{
        const sigLines = sigEl.innerText.split('\n');
        sigLines.forEach(line => {{
            if (line.trim()) {{ 
                elementsXml += `<paragraph Alignment="2"><content startOffset="${{offset}}" length="${{line.length}}" /></paragraph>`; 
                offset += line.length; 
            }} else {{ 
                elementsXml += `<paragraph><content startOffset="${{offset}}" length="1" /></paragraph>`; 
                offset += 1; 
            }}
        }});
    }}
    
    const contentXml = `<?xml version="1.0" encoding="UTF-8" ?>\n<template format_id="1.8" >\n<content><![CDATA[${{fullText}}]]></content>\n<properties><pageFormat mediaSizeName="1" leftMargin="70.8661413192749" rightMargin="70.8661413192749" topMargin="70.8661413192749" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" /></properties>\n<elements resolver="hvl-default" >\n${{elementsXml}}\n</elements>\n<styles><style name="hvl-default" family="Times New Roman" size="12" description="Gövde" /></styles>\n</template>`;
    
    const zip = new JSZip();
    zip.file("content.xml", contentXml);
    zip.file("documentproperties.xml", `<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd"><properties><entry key="user.gercek"></entry></properties>`);
    zip.file("sign.sgn", `<?xml version="1.0" encoding="UTF-8"?><signature-list/>`);
    
    const blob = await zip.generateAsync({{type: "blob"}});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = '{filename_base}.udf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}}

function downloadWord(elementId) {{
    const content = document.getElementById(elementId).querySelector('.petition-letter').innerHTML;
    const blob = new Blob(['\\ufeff', `<html><meta charset="utf-8"><title>{petition_name}</title><body>${{content}}</body></html>`], {{type: 'application/msword'}});
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);
    a.download = '{filename_base}.doc';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}}

function copyPetition(elementId) {{
    const text = document.getElementById(elementId).querySelector('.petition-letter').innerText;
    navigator.clipboard.writeText(text).then(() => alert('Kopyalandı!'));
}}
</script>'''
    
    # Find and remove the malformed JavaScript section (if exists)
    # Look for download functions that contain search modal
    malformed_js_pattern = r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jszip[^<]*</script>\s*<script>.*?(?:downloadUDF|function downloadUDF).*?(?:downloadWord|function downloadWord).*?copyPetition.*?</script>'
    
    # Remove malformed JavaScript
    content = re.sub(malformed_js_pattern, '', content, flags=re.DOTALL)
    
    # Find where to insert the new JS - before </body>
    # Insert JSZip script before closing body
    content = content.replace('</body>', jszip_script + '\n' + download_functions + '\n</body>')
    
    # Find the petition-actions div and ensure it has correct onclick handlers
    # Fix the button onclick handlers if needed
    content = re.sub(
        r'onclick="downloadUDF\([^)]+\)"',
        f'onclick="downloadUDF(\'{element_id}\')"',
        content
    )
    content = re.sub(
        r'onclick="downloadWord\([^)]+\)"',
        f'onclick="downloadWord(\'{element_id}\')"',
        content
    )
    content = re.sub(
        r'onclick="copyPetition\([^)]+\)"',
        f'onclick="copyPetition(\'{element_id}\')"',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

def main():
    # Find all petition files
    petition_files = glob.glob('dilekce-*.html')
    
    # Exclude dilekce-ornekleri.html (main listing page)
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
