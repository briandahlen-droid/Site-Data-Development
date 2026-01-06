"""
Setup Verification Script
Run this to verify all files are present before deploying
"""

import os
import sys

print("=" * 60)
print("SITE DATA DEVELOPMENT TOOL - SETUP VERIFICATION")
print("=" * 60)
print()

# Required files
required_files = {
    'app.py': 'Main Streamlit application',
    'county_adapters.py': 'Property lookup functions',
    'excel_generator.py': 'Excel report generation',
    'municode_parser.py': 'Municode integration',
    'requirements.txt': 'Python dependencies',
    'README.md': 'Documentation',
    '.gitignore': 'Git configuration (optional)'
}

print("Checking for required files...")
print()

all_present = True
for filename, description in required_files.items():
    exists = os.path.exists(filename)
    status = "✓" if exists else "✗"
    
    if not exists and filename != '.gitignore':
        all_present = False
    
    print(f"[{status}] {filename:25} - {description}")

print()
print("=" * 60)

if all_present:
    print("✓ ALL REQUIRED FILES PRESENT")
    print()
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Test locally: streamlit run app.py")
    print("3. Push to GitHub: git add . && git commit -m 'Initial commit' && git push")
    print("4. Deploy on Streamlit Cloud: https://share.streamlit.io")
    print()
else:
    print("✗ MISSING FILES DETECTED")
    print()
    print("Please copy all files from the deployment package before proceeding.")
    print()
    sys.exit(1)

print("=" * 60)

# Try importing modules
print()
print("Testing module imports...")
print()

try:
    import streamlit
    print("✓ streamlit installed")
except ImportError:
    print("✗ streamlit not installed (run: pip install -r requirements.txt)")

try:
    import requests
    print("✓ requests installed")
except ImportError:
    print("✗ requests not installed (run: pip install -r requirements.txt)")

try:
    import openpyxl
    print("✓ openpyxl installed")
except ImportError:
    print("✗ openpyxl not installed (run: pip install -r requirements.txt)")

try:
    import pandas
    print("✓ pandas installed")
except ImportError:
    print("✗ pandas not installed (run: pip install -r requirements.txt)")

print()
print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
