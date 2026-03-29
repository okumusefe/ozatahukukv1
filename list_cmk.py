#!/usr/bin/env python3
import os
import re

# Get all CMK files
cmk_files = sorted([f.replace('makale-cmk-', '').replace('.html', '') for f in os.listdir('.') if f.startswith('makale-cmk-')])

print(f"CMK files on disk: {len(cmk_files)}")
print("All CMK ranges:")
for f in cmk_files:
    print(f"  {f}")
