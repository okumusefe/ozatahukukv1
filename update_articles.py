#!/usr/bin/env python3
"""
Update all articles to match makale-tck-35-36.html style
Style characteristics:
1. Clear, direct opening defining the legal concept
2. Structured paragraphs with semicolons separating key points
3. Concrete examples from real-world scenarios
4. References to Yargıtay
5. Practical application showing how law works
6. Human-centered conclusion about rehabilitation
7. Professional but accessible - no verbosity
"""
import os
import re

# Get all article files
all_files = sorted([f for f in os.listdir('.') if f.startswith('makale-') and f.endswith('.html')])

tck_files = [f for f in all_files if 'tck' in f]
cmk_files = [f for f in all_files if 'cmk' in f]

print(f"Found {len(tck_files)} TCK files and {len(cmk_files)} CMK files")
print(f"Total: {len(all_files)} articles")

# Check each file's current word count to identify which need updating
for f in all_files[:5]:  # Check first 5 as sample
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        # Extract content between article-content div
        match = re.search(r'<div class="article-content">(.*?)</div>', content, re.DOTALL)
        if match:
            text = match.group(1)
            # Count words in paragraphs
            words = len(re.findall(r'<p>(.*?)</p>', text, re.DOTALL))
            print(f"{f}: ~{words} paragraphs")
