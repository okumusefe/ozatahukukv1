#!/usr/bin/env python3
"""
Mass update script for all 87 articles to match reference style
"""
import os
import re

# Get all files
files = sorted([f for f in os.listdir('.') if f.startswith('makale-') and f.endswith('.html')])

print("=" * 60)
print(f"Found {len(files)} article files")
print("=" * 60)

# Categorize
tck = [f for f in files if 'tck' in f]
cmk = [f for f in files if 'cmk' in f]

print(f"\nTCK: {len(tck)} files")
print(f"CMK: {len(cmk)} files")

# Check first 5 of each
print("\n--- Sample TCK files ---")
for f in tck[:5]:
    size = os.path.getsize(f)
    print(f"  {f} ({size} bytes)")

print("\n--- Sample CMK files ---")
for f in cmk[:5]:
    size = os.path.getsize(f)
    print(f"  {f} ({size} bytes)")

print("\n" + "=" * 60)
print("Ready to update all files to new style")
print("=" * 60)
