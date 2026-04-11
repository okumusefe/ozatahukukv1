#!/usr/bin/env python3
"""
Fix element ID mismatches in petition files
"""

import os
import re
import glob

def fix_petition_file(filepath):
    """Fix element ID mismatches in a single petition file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the petition-preview div ID
    preview_match = re.search(r'<div class="petition-preview"[^>]*id="([^"]+)"', content)
    if preview_match:
        element_id = preview_match.group(1)
    else:
        # Try petition-document pattern
        doc_match = re.search(r'<div class="petition-document"[^>]*id="([^"]+)"', content)
        if doc_match:
            element_id = doc_match.group(1)
        else:
            print(f"No petition element found in {filepath}")
            return
    
    # Find current onclick IDs
    onclick_matches = re.findall(r'onclick="downloadUDF\(\'([^\']+)\'\)"', content)
    if not onclick_matches:
        onclick_matches = re.findall(r'onclick="downloadUDF\("([^"]+)"\)"', content)
    
    if not onclick_matches:
        print(f"No download buttons found in {filepath}")
        return
    
    current_onclick_id = onclick_matches[0]
    
    # If IDs don't match, fix them
    if current_onclick_id != element_id:
        print(f"Fixing {filepath}: changing '{current_onclick_id}' to '{element_id}'")
        
        # Fix all download function calls
        content = re.sub(
            r'onclick="downloadUDF\(\'[^\']+\'\)"',
            f'onclick="downloadUDF(\'{element_id}\')"',
            content
        )
        content = re.sub(
            r'onclick="downloadUDF\("[^"]+"\)"',
            f'onclick="downloadUDF(\"{element_id}\")"',
            content
        )
        content = re.sub(
            r'onclick="downloadWord\(\'[^\']+\'\)"',
            f'onclick="downloadWord(\'{element_id}\')"',
            content
        )
        content = re.sub(
            r'onclick="downloadWord\("[^"]+"\)"',
            f'onclick="downloadWord(\"{element_id}\")"',
            content
        )
        content = re.sub(
            r'onclick="copyPetition\(\'[^\']+\'\)"',
            f'onclick="copyPetition(\'{element_id}\')"',
            content
        )
        content = re.sub(
            r'onclick="copyPetition\("[^"]+"\)"',
            f'onclick="copyPetition(\"{element_id}\")"',
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed!")
    else:
        print(f"OK {filepath}: IDs match ('{element_id}')")

def main():
    petition_files = glob.glob('dilekce-*.html')
    petition_files = [f for f in petition_files if f != 'dilekce-ornekleri.html']
    
    print(f"Found {len(petition_files)} petition files to check")
    print()
    
    for filepath in petition_files:
        try:
            fix_petition_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("Done!")

if __name__ == '__main__':
    main()
