#!/usr/bin/env python3
"""
Fix JavaScript escape sequences in RTF content
"""

import glob
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if has downloadWord function with single backslash issue
    if "'\\pard\\qc\\b " not in content and "'\\\\pard\\\\qc\\\\b " not in content:
        return False
    
    # Fix single backslash to double backslash in RTF strings
    # The pattern looks for single backslash RTF commands inside strings
    
    # Find downloadWord function
    func_start = content.find('function downloadWord(elementId)')
    if func_start == -1:
        return False
    
    func_end = content.find('function copyPetition', func_start)
    if func_end == -1:
        func_end = content.find('</script>', func_start)
    
    if func_end == -1:
        return False
    
    func_content = content[func_start:func_end]
    
    # Check if needs fixing (single backslash RTF commands)
    # Pattern: '\par', '\qc', '\b' etc should be '\\par', '\\qc', '\\b'
    
    # Replace single backslash RTF commands with double backslash
    # But be careful not to double-escape already escaped ones
    
    new_func = func_content
    
    # Fix common RTF commands - add extra backslash
    rtf_commands = ['pard', 'qc', 'b ', 'b0', 'qr', 'plain', 'par', 'rtf1', 'ansi', 'ansicpg1254', 'deff0', 'nouicompat', 'deflang1055', 'deflangfe1055', 'fonttbl', 'f0', 'fnil', 'fcharset162', 'generator', 'viewkind4', 'uc1', 'fs28', 'lang1055']
    
    # Replace '\command' with '\\command' in string contexts
    for cmd in rtf_commands:
        # Match single backslash before command in string context
        pattern = rf"(?<=')\\{cmd}(?='|\"|\s|\\)"
        replacement = rf'\\\\{cmd}'
        new_func = re.sub(pattern, replacement, new_func)
    
    if new_func != func_content:
        new_content = content[:func_start] + new_func + content[func_end:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {filepath}")
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
            print(f"Error {filepath}: {e}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
