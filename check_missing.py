import os, re

# Get CMK files on disk
disk = sorted([f.replace('makale-cmk-', '').replace('.html', '') for f in os.listdir('.') if f.startswith('makale-cmk-')])

# Get CMK files in yayinlar.html
with open('yayinlar.html', 'r', encoding='utf-8') as f:
    content = f.read()
html = sorted(set(re.findall(r'makale-cmk-(\d+-\d+)\.html', content)))

print(f"Disk: {len(disk)}, HTML: {len(html)}")
missing = sorted(set(disk) - set(html))
print(f"\nMissing from HTML ({len(missing)}):")
for m in missing:
    print(f"  {m}")
