#!/usr/bin/env python3
"""
Debug script to find Operating Income patterns in the Google 10-K
"""
import pdfplumber
import re

def find_operating_income():
    pdf_path = "/Users/neelesh/Documents/Interviews/DealMover/Form 10-K.pdf"
    
    print("Searching for Operating Income patterns...")
    print("=" * 60)
    
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        
        # Extract text from all pages
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text += text + "\n"
        
        # Look for Operating Income patterns
        operating_income_patterns = [
            r'operating\s+income[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
            r'income\s+from\s+operations[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
            r'operating\s+earnings[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        ]
        
        print("Searching for Operating Income patterns...")
        for pattern in operating_income_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                print(f"Pattern: {pattern}")
                print(f"Matches: {matches[:5]}")  # Show first 5 matches
                print()
        
        # Look for specific values we might expect
        print("Searching for large numbers that might be Operating Income...")
        large_numbers = re.findall(r'\$?([0-9,]{6,}(?:\([0-9,]+\))?)', all_text)
        print(f"Found {len(large_numbers)} large numbers")
        print("Sample large numbers:", large_numbers[:10])
        
        # Look for table-like financial data with operating income
        print("\nSearching for table-like financial data...")
        table_patterns = re.findall(r'([A-Za-z\s]*operating\s+income[A-Za-z\s]*)\s+\$?([0-9,]+(?:\([0-9,]+\))?)', all_text, re.IGNORECASE)
        print(f"Operating income table entries: {len(table_patterns)}")
        for entry in table_patterns[:10]:
            print(f"  {entry[0].strip()}: {entry[1]}")

if __name__ == "__main__":
    find_operating_income()
