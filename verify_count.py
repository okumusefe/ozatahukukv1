#!/usr/bin/env python3
"""Verify current article counts in yayinlar.html"""
import os, re

# Read yayinlar.html
with open('yayinlar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Count articles
tck_count = len(re.findall(r'data-category="tck"', content))
cmk_count = len(re.findall(r'data-category="cmk"', content))

print(f"TCK articles in yayinlar.html: {tck_count}")
print(f"CMK articles in yayinlar.html: {cmk_count}")
print(f"Total: {tck_count + cmk_count}")
print(f"\nExpected: 39 TCK + 48 CMK = 87 total")
print(f"Missing: {87 - (tck_count + cmk_count)} articles")

# List which CMK ranges are present
cmk_ranges = sorted(set(re.findall(r'makale-cmk-(\d+-\d+)\.html', content)))
print(f"\nCMK ranges in yayinlar.html ({len(cmk_ranges)}):")
for r in cmk_ranges:
    print(f"  {r}")
