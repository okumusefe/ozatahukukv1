#!/usr/bin/env python3
"""
Check all petition files for download button issues
"""

import glob
import re

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Find petition content ID
    content_id_match = re.search(r'id="([\w-]+-content)"', content)
    if not content_id_match:
        issues.append("No petition content ID found")
        return issues
    
    content_id = content_id_match.group(1)
    
    # Check buttons
    copy_btn = re.search(r"onclick=\"copyPetition\('([^']+)'\)\"", content)
    udf_btn = re.search(r"onclick=\"downloadUDF\('([^']+)'\)\"", content)
    word_btn = re.search(r"onclick=\"downloadWord\('([^']+)'\)\"", content)
    
    if not copy_btn:
        issues.append("Missing copy button")
    elif copy_btn.group(1) != content_id:
        issues.append(f"Copy button ID mismatch: {copy_btn.group(1)} != {content_id}")
    
    if not udf_btn:
        issues.append("Missing UDF button")
    elif udf_btn.group(1) != content_id:
        issues.append(f"UDF button ID mismatch: {udf_btn.group(1)} != {content_id}")
    
    if not word_btn:
        issues.append("Missing Word button")
    elif word_btn.group(1) != content_id:
        issues.append(f"Word button ID mismatch: {word_btn.group(1)} != {content_id}")
    
    # Check JavaScript functions exist
    if 'function downloadUDF' not in content:
        issues.append("Missing downloadUDF function")
    if 'function downloadWord' not in content:
        issues.append("Missing downloadWord function")
    if 'function copyPetition' not in content:
        issues.append("Missing copyPetition function")
    
    return issues

def main():
    files = glob.glob('dilekce-*.html')
    files = [f for f in files if f != 'dilekce-ornekleri.html']
    
    print(f"Checking {len(files)} petition files...")
    print()
    
    total_issues = 0
    for filepath in files:
        issues = check_file(filepath)
        if issues:
            print(f"❌ {filepath}:")
            for issue in issues:
                print(f"   - {issue}")
            total_issues += 1
        else:
            print(f"✅ {filepath}")
    
    print()
    print(f"Found issues in {total_issues} files")

if __name__ == '__main__':
    main()
