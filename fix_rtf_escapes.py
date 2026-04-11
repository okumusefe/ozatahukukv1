#!/usr/bin/env python3
"""
Fix RTF escape sequences in downloadWord function
Replace single backslash with double backslash for RTF commands
"""

import glob
import re

def fix_rtf_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find downloadWord function
    start_marker = 'function downloadWord(elementId) {'
    end_marker = 'function copyPetition'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return False
    
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        end_idx = content.find('</script>', start_idx)
    if end_idx == -1:
        return False
    
    func_content = content[start_idx:end_idx]
    
    # Check if has single backslash RTF commands (not already fixed)
    # Pattern: '\par', '\qc' etc in string literals
    
    # Replace RTF commands: single backslash -> double backslash
    # But first, let's check if already has double backslashes
    if "'\\\\pard\\\\qc\\\\b " in func_content:
        return False  # Already fixed
    
    # RTF commands that need escaping
    rtf_cmds = [
        ('\\pard', '\\\\pard'),
        ('\\qc', '\\\\qc'),
        ('\\qr', '\\\\qr'),
        ('\\b ', '\\\\b '),
        ('\\b0', '\\\\b0'),
        ('\\par', '\\\\par'),
        ('\\plain', '\\\\plain'),
    ]
    
    new_func = func_content
    for old, new in rtf_cmds:
        new_func = new_func.replace(old, new)
    
    if new_func != func_content:
        new_content = content[:start_idx] + new_func + content[end_idx:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if 'ornekleri' not in f]
    
    fixed = 0
    for f in files:
        try:
            if fix_rtf_in_file(f):
                print(f"Fixed: {f}")
                fixed += 1
        except Exception as e:
            print(f"Error {f}: {e}")
    
    print(f"\nFixed {fixed} files")

if __name__ == '__main__':
    main()
