#!/usr/bin/env python3
"""
Update all articles to match makale-tck-35-36.html style
Style: Clear opening, semicolon structure, concrete examples, Yargıtay refs, practical application, human conclusion
"""
import os
import re

# Get all article files
all_files = sorted([f for f in os.listdir('.') if f.startswith('makale-') and f.endswith('.html')])

tck_files = [f for f in all_files if 'tck' in f]
cmk_files = [f for f in all_files if 'cmk' in f]

print(f"Total: {len(all_files)} articles")
print(f"TCK: {len(tck_files)}, CMK: {len(cmk_files)}")
print("\nFiles to update:")
for f in all_files:
    print(f"  {f}")
