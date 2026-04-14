#!/usr/bin/env python3
"""
Remove optional chaining (?.) from calculators.js for better browser compatibility
"""

import re

def fix_optional_chaining(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace ?.value with traditional check
    # pattern: document.getElementById('xxx')?.value || 0
    # replacement: (document.getElementById('xxx') && document.getElementById('xxx').value) || 0
    
    # Simple pattern for ?.value || default
    content = re.sub(
        r"document\.getElementById\('([^']+)'\)\?\.value\s*\|\|\s*([^;\n,]+)",
        r"(document.getElementById('\1') && document.getElementById('\1').value) || \2",
        content
    )
    
    # Pattern for ?.checked || default
    content = re.sub(
        r"document\.getElementById\('([^']+)'\)\?\.checked\s*\|\|\s*([^;\n,]+)",
        r"(document.getElementById('\1') && document.getElementById('\1').checked) || \2",
        content
    )
    
    # Pattern for just ?.value without default
    content = re.sub(
        r"document\.getElementById\('([^']+)'\)\?\.value",
        r"(document.getElementById('\1') && document.getElementById('\1').value)",
        content
    )
    
    # Pattern for just ?.checked without default
    content = re.sub(
        r"document\.getElementById\('([^']+)'\)\?\.checked",
        r"(document.getElementById('\1') && document.getElementById('\1').checked)",
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed optional chaining in: {filepath}')
        return True
    return False

if __name__ == '__main__':
    if fix_optional_chaining('hesaplamalar/calculators.js'):
        print('Done!')
    else:
        print('No changes needed')
