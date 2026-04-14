#!/usr/bin/env python3
"""
Remove all social media icons from all HTML files
"""

import glob
import re

def remove_social_icons(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern to match nav-social div with all its content
    # Match from <div class="nav-social" to </div>
    pattern = r'<div class="nav-social"[^>]*>.*?</div>\s*</div>\s*</div>\s*</a>\s*</div>'
    
    # Simpler approach: match nav-social div and everything until its closing div
    # This is a common pattern in the HTML files
    
    # Try different patterns
    # Pattern 1: nav-social div
    content = re.sub(
        r'<div class="nav-social"[^>]*>.*?</div>\s*</div>\s*</div>\s*</a>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Pattern 2: nav-social with style attribute
    content = re.sub(
        r'<div class="nav-social"[^>]*style="[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>\s*</a>\s*</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Pattern 3: More flexible matching for nav-social
    def replace_nav_social(match):
        return ''
    
    # Find and remove nav-social sections
    nav_social_pattern = r'<div class="nav-social"[^>]*>.*?</div>\s*</nav>'
    content = re.sub(nav_social_pattern, '</nav>', content, flags=re.DOTALL)
    
    # Also try without the closing nav tag requirement
    nav_social_pattern2 = r'<div class="nav-social"[^>]*>.*?</div>\s*</div>\s*</div>\s*</a>\s*</div>\s*</div>'
    content = re.sub(nav_social_pattern2, '</div>', content, flags=re.DOTALL)
    
    # Pattern for the specific structure I saw earlier
    # Match from nav-social to the button after it
    pattern3 = r'<div class="nav-social"[^>]*>.*?<button class="nav-search-btn"'
    content = re.sub(pattern3, '<button class="nav-search-btn"', content, flags=re.DOTALL)
    
    # Pattern 4: Match nav-social with instagram, linkedin, youtube links
    pattern4 = r'<div class="nav-social"[^>]*>.*?youtube.*?</svg>\s*</a>\s*</div>\s*</div>'
    content = re.sub(pattern4, '</div>', content, flags=re.DOTALL)
    
    if content != original:
        print(f'Removed social icons from: {filepath}')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = glob.glob('*.html') + glob.glob('hesaplamalar/*.html')
    
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
