#!/usr/bin/env python3
import re

with open('yayinlar.html', 'r', encoding='utf-8') as f:
    content = f.read()

tck_count = len(re.findall(r'data-category="tck"', content))
cmk_count = len(re.findall(r'data-category="cmk"', content))

print(f"TCK: {tck_count}")
print(f"CMK: {cmk_count}")
print(f"Total: {tck_count + cmk_count}")

# List all CMK ranges found
cmk_matches = re.findall(r'makale-cmk-(\d+-\d+)\.html', content)
print(f"\nCMK articles in yayinlar.html: {len(cmk_matches)}")
print(f"Expected: 48")

# Check which CMK files exist but not in yayinlar.html
import os
cmk_files = [f.replace('makale-cmk-', '').replace('.html', '') for f in os.listdir('.') if f.startswith('makale-cmk-')]
cmk_in_yayinlar = set(cmk_matches)
cmk_files_set = set(cmk_files)

missing = cmk_files_set - cmk_in_yayinlar
extra = cmk_in_yayinlar - cmk_files_set

if missing:
    print(f"\nMissing from yayinlar.html: {sorted(missing)}")
if extra:
    print(f"\nIn yayinlar.html but no file: {sorted(extra)}")
