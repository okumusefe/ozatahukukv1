#!/usr/bin/env python3
"""
Update all 87 articles (39 TCK + 48 CMK) to match makale-tck-35-36.html style
"""
import os
import re

# Get all article files
all_files = [f for f in os.listdir('.') if f.startswith('makale-') and f.endswith('.html')]
tck_files = sorted([f for f in all_files if 'tck' in f])
cmk_files = sorted([f for f in all_files if 'cmk' in f])

print(f"TCK files: {len(tck_files)}")
print(f"CMK files: {len(cmk_files)}")
print(f"Total: {len(all_files)}")

# Check first few files to see current state
for f in tck_files[:3]:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        has_style_markers = 'Yargıtay' in content and ';' in content
        print(f"{f}: {'Has new style' if has_style_markers else 'Needs update'}")
