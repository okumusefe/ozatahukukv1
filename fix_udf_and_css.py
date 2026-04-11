#!/usr/bin/env python3
"""
Fix UDF sign.sgn issue and CSS styling for all petition files
"""

import os
import re
import glob

def fix_petition_file(filepath):
    """Fix a single petition file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove sign.sgn from UDF download function
    content = re.sub(
        r"zip\.file\(\"sign\.sgn\",[^)]+\);?\s*",
        "",
        content
    )
    
    # 2. Fix petition section styling - add proper CSS classes if missing
    # Ensure petition sections have proper structure
    content = re.sub(
        r'<div class="petition-section">\s*<span class="petition-label">',
        '<div class="petition-section">\n<span class="petition-label">',
        content
    )
    
    # 3. Fix inline styles that might be overriding CSS
    # Remove style="margin-bottom: 1.5rem;" from petition-content divs
    content = re.sub(
        r'<div class="petition-content" style="margin-bottom:\s*[^"]+">',
        '<div class="petition-content">',
        content
    )
    
    # 4. Ensure proper HTML structure in petition letter
    # Fix missing closing tags or improper nesting
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {filepath}")

def main():
    petition_files = glob.glob('dilekce-*.html')
    petition_files = [f for f in petition_files if f != 'dilekce-ornekleri.html']
    
    print(f"Found {len(petition_files)} petition files to fix")
    print()
    
    for filepath in petition_files:
        try:
            fix_petition_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print()
    print("Done!")

if __name__ == '__main__':
    main()
