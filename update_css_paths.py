import os

# Update all HTML files in hesaplamalar folder
hesaplamalar_path = 'hesaplamalar'
for filename in os.listdir(hesaplamalar_path):
    if filename.endswith('.html'):
        filepath = os.path.join(hesaplamalar_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace CSS and asset paths from ../ to ./ for file:// protocol compatibility
        content = content.replace('href="../styles.css"', 'href="./styles.css"')
        content = content.replace('href="../responsive.css"', 'href="./responsive.css"')
        content = content.replace('href="../favicon', 'href="./favicon')
        content = content.replace('href="../apple-touch-icon', 'href="./apple-touch-icon')
        content = content.replace('src="../logo.svg"', 'src="./logo.svg"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {filename}')

print('All calculator pages updated successfully!')
