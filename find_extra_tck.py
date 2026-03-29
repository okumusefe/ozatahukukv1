#!/usr/bin/env python3
"""
Compare TCK files against reference list to find excess files
"""
import os

# Reference TCK ranges from user's specification
TCK_REF = [
    (20, 23), (24, 34), (35, 36), (37, 41), (42, 44), (45, 52), (53, 60), (61, 63),
    (64, 75), (76, 78), (79, 80), (81, 85), (86, 93), (94, 96), (97, 98), (99, 101),
    (102, 105), (106, 124), (125, 131), (132, 140), (141, 169), (170, 180), (181, 184),
    (185, 196), (197, 212), (213, 222), (223, 224), (225, 229), (230, 234), (235, 242),
    (243, 246), (247, 266), (267, 298), (299, 301), (302, 308), (309, 316), (317, 325),
    (326, 339), (340, 343)
]

# Convert to set of strings for comparison
ref_set = set([f"{s}-{e}" for s, e in TCK_REF])

# Get actual TCK files
files = [f for f in os.listdir('.') if f.startswith('makale-tck-') and f.endswith('.html')]
actual_set = set([f.replace('makale-tck-', '').replace('.html', '') for f in files])

print(f"Reference TCK count: {len(ref_set)}")
print(f"Actual TCK files: {len(actual_set)}")

# Find differences
missing = ref_set - actual_set  # In ref but no file
extra = actual_set - ref_set     # File exists but not in ref

print(f"\n✓ All reference ranges have files: {len(ref_set - missing)}/{len(ref_set)}")

if extra:
    print(f"\n❌ EXTRA TCK files (not in reference list):")
    for e in sorted(extra):
        print(f"   - makale-tck-{e}.html")
    print(f"\nTotal extra: {len(extra)}")

if missing:
    print(f"\n⚠️  MISSING TCK files (in reference but no file):")
    for m in sorted(missing):
        print(f"   - makale-tck-{m}.html")
