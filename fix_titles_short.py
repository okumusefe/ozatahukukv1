#!/usr/bin/env python3
"""
Change titles from 'Hakimliğine' to just 'Mahkemesine'
Change 'Müdürlüğüne' to just 'Dairesi'ne
"""

import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace HAKİMLİĞİNE with NE (for courts)
    content = content.replace('HAKİMLİĞİNE', 'NE')
    
    # Replace MÜDÜRLÜĞÜNE with NE (for offices)
    content = content.replace('MÜDÜRLÜĞÜNE', 'NE')
    
    # Also fix the lowercase versions if any
    content = content.replace('Hakimliğine', 'ne')
    content = content.replace('Müdürlüğüne', 'ne')
    
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
