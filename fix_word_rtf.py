#!/usr/bin/env python3
"""
Fix Word download to use proper RTF format with formatting
"""

import os
import glob

NEW_FUNC = '''function downloadWord(elementId) {
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
}'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start of downloadWord function
    start_idx = content.find('function downloadWord(elementId)')
    if start_idx == -1:
        print(f"Skipping {filepath} - function not found")
        return False
    
    # Find the end of the function (next function or end of script)
    # Look for "function copyPetition" or "</script>"
    end_marker1 = content.find('function copyPetition', start_idx)
    end_marker2 = content.find('</script>', start_idx)
    
    if end_marker1 != -1:
        end_idx = end_marker1
    elif end_marker2 != -1:
        end_idx = end_marker2
    else:
        print(f"Skipping {filepath} - cannot find end of function")
        return False
    
    # Replace the function
    new_content = content[:start_idx] + NEW_FUNC + '\n\n' + content[end_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Fixed: {filepath}")
    return True

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if f != 'dilekce-ornekleri.html']
    
    count = 0
    for f in files:
        try:
            if fix_file(f):
                count += 1
        except Exception as e:
            print(f"Error: {f}: {e}")
    
    print(f"\nFixed {count} files")

if __name__ == '__main__':
    main()
