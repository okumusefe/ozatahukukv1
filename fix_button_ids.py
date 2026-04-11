#!/usr/bin/env python3
"""
Fix button ID mismatches in petition files
"""

import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find petition content ID
    content_id_match = re.search(r'id="([\w-]+-content)"', content)
    if not content_id_match:
        return False
    
    content_id = content_id_match.group(1)
    
    # Check if there's a mismatch (double -content-content issue)
    wrong_id = content_id + '-content'
    
    # Count replacements
    original = content
    
    # Fix onclick handlers
    content = content.replace(f"'{wrong_id}'", f"'{content_id}'")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath} ({wrong_id} -> {content_id})")
        return True
    
    return False

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if f != 'dilekce-ornekleri.html']
    
    fixed_count = 0
    for filepath in files:
        try:
            if fix_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"Error: {filepath}: {e}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
