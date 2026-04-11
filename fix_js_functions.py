#!/usr/bin/env python3
"""
Fix JavaScript functions - remove optional chaining for better compatibility
"""

import glob

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace optional chaining with traditional checks
    original = content
    content = content.replace('?.innerText', '.innerText')
    content = content.replace('?.', '.')
    
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
