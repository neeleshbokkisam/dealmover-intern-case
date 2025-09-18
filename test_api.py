#!/usr/bin/env python3
"""
Test script for the PDF extraction API
"""
import requests
import json
import time

def test_api():
    url = "http://localhost:8000/api/extract/"
    
    # Test with the Google 10-K PDF
    pdf_path = "/Users/neelesh/Documents/Interviews/DealMover/Form 10-K.pdf"
    
    print("🧪 Testing PDF extraction API...")
    print(f"PDF file: {pdf_path}")
    print(f"API endpoint: {url}")
    print("-" * 50)
    
    # Wait a moment for server to start
    time.sleep(2)
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'pdf_file': pdf_file}
            data = {'period_end_date': '2024-12-31'}
            
            response = requests.post(url, files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Validate the response
            if response.status_code == 200:
                data = response.json()
                if data.get('results', {}).get('revenue') and data.get('results', {}).get('cos'):
                    print("\n✅ API test PASSED - Successfully extracted financial data")
                    print(f"   Revenue: {data['results']['revenue']}")
                    print(f"   Cost of Sales: {data['results']['cos']}")
                else:
                    print("\n❌ API test FAILED - No financial data extracted")
            else:
                print(f"\n❌ API test FAILED - Status code: {response.status_code}")
            
    except FileNotFoundError:
        print(f"❌ Error: PDF file not found at {pdf_path}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure Django server is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_api()
