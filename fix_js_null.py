#!/usr/bin/env python3
"""
Fix null pointer errors in all petition files
Replace .innerText || '' with proper null checks
"""

import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace the problematic pattern:
    # const label = section.querySelector('.petition-label').innerText || '';
    # const content = section.querySelector('.petition-content').innerText || '';
    # With:
    # const labelEl = section.querySelector('.petition-label');
    # const contentEl = section.querySelector('.petition-content');
    # const label = labelEl ? labelEl.innerText : '';
    # const content = contentEl ? contentEl.innerText : '';
    
    # Pattern to match the problematic lines
    pattern = r"(petitionContent\.querySelectorAll\('\.petition-section'\)\.forEach\(section => \{[\s\S]*?)(const label = section\.querySelector\('\.petition-label'\)\.innerText \|\| '';\s*const content = section\.querySelector\('\.petition-content'\)\.innerText \|\| '';)([\s\S]*?\}\);)"
    
    # Apply the fix
    content = re.sub(
        r"const label = section\.querySelector\('\.petition-label'\)\.innerText \|\| '';\s*const content = section\.querySelector\('\.petition-content'\)\.innerText \|\| '';",
        "const labelEl = section.querySelector('.petition-label');\n        const contentEl = section.querySelector('.petition-content');\n        const label = labelEl ? labelEl.innerText : '';\n        const content = contentEl ? contentEl.innerText : '';",
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {filepath}')
        return True
    return False

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if 'ornekleri' not in f]
    
    fixed = 0
    for f in files:
        try:
            if fix_file(f):
                fixed += 1
        except Exception as e:
            print(f'Error {f}: {e}')
    
    print(f'\nFixed {fixed} files')

if __name__ == '__main__':
    main()
