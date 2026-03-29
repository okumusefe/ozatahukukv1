import os
import re

# Get all article files
files = sorted([f for f in os.listdir('.') if f.startswith('makale-') and f.endswith('.html')])

print(f"Total article files: {len(files)}")
print("\nTCK files:")
tck_files = [f for f in files if 'tck' in f]
for f in tck_files:
    print(f"  {f}")

print("\nCMK files:")
cmk_files = [f for f in files if 'cmk' in f]
for f in cmk_files:
    print(f"  {f}")

print(f"\nCounts: TCK={len(tck_files)}, CMK={len(cmk_files)}, Total={len(files)}")
