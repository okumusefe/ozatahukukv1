#!/usr/bin/env python3
"""
Mass update all article files to match reference style
"""
import os
import re

# Article definitions with their content
ARTICLES = {
    # TCK Articles
    'makale-tck-20-23.html': {
        'title': 'Ceza Sorumluluğunun Şahsiliği, Kast ve Taksir',
        'category': 'TCK',
        'desc': 'TCK md. 20-23 - Ceza hukukunun temel yapı taşları'
    },
    'makale-tck-24-34.html': {
        'title': 'Ceza Sorumluluğunu Kaldıran veya Azaltan Nedenler',
        'category': 'TCK', 
        'desc': 'TCK md. 24-34 - Meşru müdafa ve diğer nedenler'
    },
    'makale-tck-35-36.html': {
        'title': 'Suça Teşebbüs',
        'category': 'TCK',
        'desc': 'TCK md. 35-36 - Hükmen ve fiilen teşebbüs'
    },
    'makale-tck-37-41.html': {
        'title': 'Suça İştirak',
        'category': 'TCK',
        'desc': 'TCK md. 37-41 - Azmettirme ve yardım etme'
    },
    'makale-tck-42-44.html': {
        'title': 'Suçların İçtimaı',
        'category': 'TCK',
        'desc': 'TCK md. 42-44 - Fiil içtimaı ve fikrî içtima'
    },
}

def process_article(filename, info):
    """Process a single article - check if it needs updating"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has new style markers
        has_semicolon_structure = ';' in content and ('hikaye' in content or 'veciz' in content)
        has_yargitay = 'Yargıtay' in content
        
        status = "OK" if (has_semicolon_structure and has_yargitay) else "NEEDS UPDATE"
        return status
    except Exception as e:
        return f"ERROR: {e}"

# Check all articles
print("Checking articles...")
for filename, info in list(ARTICLES.items())[:10]:
    if os.path.exists(filename):
        status = process_article(filename, info)
        print(f"  {filename}: {status}")
    else:
        print(f"  {filename}: NOT FOUND")
