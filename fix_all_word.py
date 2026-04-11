#!/usr/bin/env python3
"""
Replace broken downloadWord with working version
"""

import glob

NEW_FUNC = '''function downloadWord(elementId) {
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
}'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start = content.find('function downloadWord(elementId)')
    if start == -1:
        return False
    
    end = content.find('function copyPetition', start)
    if end == -1:
        return False
    
    new_content = content[:start] + NEW_FUNC + '\\n\\n' + content[end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if 'ornekleri' not in f]
    
    fixed = 0
    for f in files:
        try:
            if fix_file(f):
                print(f'Fixed: {f}')
                fixed += 1
        except Exception as e:
            print(f'Error {f}: {e}')
    
    print(f'\\nFixed {fixed} files')

if __name__ == '__main__':
    main()
