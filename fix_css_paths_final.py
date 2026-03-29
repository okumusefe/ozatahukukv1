import os

hesaplamalar_path = 'hesaplamalar'
fixed_count = 0

for filename in os.listdir(hesaplamalar_path):
    if filename.endswith('.html'):
        filepath = os.path.join(hesaplamalar_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace CSS paths
        content = content.replace('href="../styles.css"', 'href="./styles.css"')
        content = content.replace('href="../responsive.css"', 'href="./responsive.css"')
        
        # Replace favicon paths  
        content = content.replace('href="../favicon', 'href="./favicon')
        content = content.replace('href="../apple-touch-icon', 'href="./apple-touch-icon')
        
        # Replace logo paths
        content = content.replace('src="../logo.svg"', 'src="./logo.svg"')
        
        # Replace script paths
        content = content.replace('src="../script.js"', 'src="./script.js"')
        content = content.replace('src="../publications.js"', 'src="./publications.js"')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_count += 1
            print(f"FIXED: {filename}")

print(f"\nTotal files fixed: {fixed_count}")
