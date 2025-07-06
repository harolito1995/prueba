import requests
import json
from datetime import datetime
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the Medical Image Processing API"""
    
    print("=== Testing Medical Image Processing API ===\n")
    
    # Test data
    test_payload = {
        "1": {
            "id": "aabbcc1",
            "data": [
                "78 83 21 68 96 46 40 11 1 88",
                "58 75 71 69 33 14 15 93 18 54",
                "46 54 73 63 85 4 30 76 15 56"
            ],
            "deviceName": "CT SCAN"
        },
        "2": {
            "id": "aabbcc2",
            "data": [
                "14 85 30 41 64 66 85 76 96 71",
                "68 53 85 9 35 52 68 0 17 5",
                "78 40 83 72 82 94 8 19 23 62"
            ],
            "deviceName": "MRI SCANNER"
        }
    }
    
    # 1. Test Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # 8. Test Delete Processing Result
    print("8. Testing Delete Processing Result...")
    try:
        response = requests.delete(f"{BASE_URL}/api/elements/aabbcc2")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Message: {result['message']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # 9. Test Delete Non-existent Result
    print("9. Testing Delete Non-existent Result...")
    try:
        response = requests.delete(f"{BASE_URL}/api/elements/nonexistent")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    print("=== API Testing Complete ===")

if __name__ == "__main__":
    test_api()