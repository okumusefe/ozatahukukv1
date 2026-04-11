#!/usr/bin/env python3
import glob
import re

for f in glob.glob('dilekce-*.html'):
    if 'ornekleri' in f: continue
    content = open(f, 'r', encoding='utf-8').read()
    m = re.search(r'id="([\w-]+-content)"', content)
    if not m: continue
    cid = m.group(1)
    
    udf_ok = f"downloadUDF('{cid}')" in content
    word_ok = f"downloadWord('{cid}')" in content
    copy_ok = f"copyPetition('{cid}')" in content
    
    if not (udf_ok and word_ok and copy_ok):
        print(f"BROKEN: {f}")
        if not udf_ok: print("  - UDF button missing/broken")
        if not word_ok: print("  - Word button missing/broken")
        if not copy_ok: print("  - Copy button missing/broken")
        print(f"  Content ID: {cid}")
