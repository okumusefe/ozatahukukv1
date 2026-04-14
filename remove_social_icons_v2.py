#!/usr/bin/env python3
"""
Remove all social media icons from all HTML files - Version 2
"""

import glob
import re

def remove_social_icons(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern to match nav-social div and its contents
    # Match from <div class="nav-social" ... > to its closing </div>
    # This div contains Instagram, LinkedIn, YouTube links
    pattern = r'<div class="nav-social"[^>]*>.*?youtube.*?</svg>\s*</a>\s*</div>'
    
    # Replace with nothing - remove entirely
    content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Also remove any remaining nav-social patterns that might have different content
    pattern2 = r'<div class="nav-social"[^>]*>.*?</div>\s*</div>\s*</div>\s*</a>\s*</div>'
    content = re.sub(pattern2, '', content, flags=re.DOTALL)
    
    # Remove social links in footer if any
    footer_social_pattern = r'<div class="social-links">.*?</div>'
    content = re.sub(footer_social_pattern, '', content, flags=re.DOTALL)
    
    # Remove whatsapp float button
    whatsapp_pattern = r'<a href="https://wa\.me/[^"]*"[^>]*class="whatsapp-float".*?</a>'
    content = re.sub(whatsapp_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    if content != original:
        print(f'Removed social icons from: {filepath}')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = glob.glob('*.html') + glob.glob('hesaplamalar/*.html') + glob.glob('dilekce-*.html')
    
    fixed = 0
    for f in files:
        try:
            if remove_social_icons(f):
                fixed += 1
        except Exception as e:
            print(f'Error {f}: {e}')
    
    print(f'\nFixed {fixed} files')

if __name__ == '__main__':
    main()
