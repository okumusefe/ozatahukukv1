import os
import re

hesaplamalar_path = 'hesaplamalar'
fixed_count = 0

for filename in os.listdir(hesaplamalar_path):
    if filename.endswith('.html') and filename != 'yayinlar.html':
        filepath = os.path.join(hesaplamalar_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove calculator-nav section (the navigation links)
        # Pattern: <div class="calculator-nav">...</div>
        content = re.sub(
            r'<div class="calculator-nav">.*?</div>\s*',
            '',
            content,
            flags=re.DOTALL
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"REMOVED nav: {filename}")
        else:
            print(f"OK: {filename}")

print(f"\nTotal files updated: {fixed_count}")
