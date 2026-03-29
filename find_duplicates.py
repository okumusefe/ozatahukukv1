#!/usr/bin/env python3
"""
Find duplicate TCK articles in yayinlar.html
"""
import re

with open('yayinlar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all TCK article entries with their file links
tck_pattern = r'<article class="article-card" data-category="tck">.*?onclick="window\.location\.href=\'makale-tck-([^\']+)\.html\'">.*?</article>'
tck_articles = re.findall(tck_pattern, content, re.DOTALL)

print(f"Total TCK entries found: {len(tck_articles)}")
print(f"\nAll TCK ranges in yayinlar.html:")
for i, tck in enumerate(tck_articles, 1):
    print(f"  {i}. makale-tck-{tck}.html")

# Find duplicates
duplicates = []
seen = set()
for tck in tck_articles:
    if tck in seen:
        duplicates.append(tck)
    else:
        seen.add(tck)

if duplicates:
    print(f"\n⚠️  DUPLICATE TCK articles found:")
    for dup in duplicates:
        count = tck_articles.count(dup)
        print(f"  - makale-tck-{dup}.html appears {count} times")
else:
    print("\n✓ No duplicates found by filename")

# Also check for articles with different titles but same file link
print(f"\n\nTotal unique TCK files: {len(set(tck_articles))}")
print(f"Expected: 37")
print(f"Excess: {len(tck_articles) - 37}")
