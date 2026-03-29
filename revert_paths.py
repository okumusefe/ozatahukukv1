import os

hesaplamalar_path = 'hesaplamalar'
fixed_count = 0

for filename in os.listdir(hesaplamalar_path):
    if filename.endswith('.html'):
        filepath = os.path.join(hesaplamalar_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Revert CSS paths back to ../
        content = content.replace('href="./styles.css"', 'href="../styles.css"')
        content = content.replace('href="./responsive.css"', 'href="../responsive.css"')
        
        # Revert favicon paths
        content = content.replace('href="./favicon', 'href="../favicon')
        content = content.replace('href="./apple-touch-icon', 'href="../apple-touch-icon')
        
        # Revert logo
        content = content.replace('src="./logo.svg"', 'src="../logo.svg"')
        
        # Revert scripts
        content = content.replace('src="./script.js"', 'src="../script.js"')
        content = content.replace('src="./publications.js"', 'src="../publications.js"')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"REVERTED: {filename}")

print(f"\nTotal files reverted: {fixed_count}")
