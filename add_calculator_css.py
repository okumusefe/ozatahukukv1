import os

hesaplamalar_path = 'hesaplamalar'
fixed_count = 0

for filename in os.listdir(hesaplamalar_path):
    if filename.endswith('.html') and filename != 'yayinlar.html':
        filepath = os.path.join(hesaplamalar_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add calculator.css after responsive.css if not already present
        if 'calculator.css' not in content:
            content = content.replace(
                '<link rel="stylesheet" href="./responsive.css">',
                '<link rel="stylesheet" href="./responsive.css">\n    <link rel="stylesheet" href="./calculator.css">'
            )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"ADDED calculator.css: {filename}")
        else:
            print(f"OK: {filename}")

print(f"\nTotal files updated: {fixed_count}")
