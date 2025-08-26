#!/usr/bin/env python3
"""
Test script for the emergency notification system
"""

import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Test data
test_user = {
    "id": "test-user-123",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "contacts": [
        {
            "id": "counselor-1",
            "name": "Dr. Sarah Wilson",
            "email": "sarah.wilson@counseling.com",  # Replace with a real email for testing
            "relationship": "counselor",
            "phone": "+1234567890"
        },
        {
            "id": "parent-1", 
            "name": "Jane Doe",
            "email": "jane.doe@email.com",  # Replace with a real email for testing
            "relationship": "parent",
            "phone": "+1234567891"
        }
    ]
}

def test_emergency_notification():
    """Test the emergency notification endpoint"""
    
    # API endpoint
    api_url = os.environ.get("VITE_EMERGENCY_API_URL", "http://localhost:8000")
    endpoint = f"{api_url}/api/notify/emergency"
    
    # Test data
    payload = {
        "user": test_user,
        "emotionScore": 85.0,  # High distress score
        "message": "I'm feeling really overwhelmed and don't know what to do anymore...",
        "relationships": ["counselor", "parent"]
    }
    
    try:
        print("Testing emergency notification endpoint...")
        print(f"Endpoint: {endpoint}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(endpoint, json=payload, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print("\n✅ Emergency notification sent successfully!")
                return True
            else:
                print(f"\n❌ Failed to send notification: {data.get('message')}")
                if 'trace' in data:
                    print(f"Error trace: {data['trace']}")
                return False
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to the API server at {api_url}")
        print("Make sure the Python backend server is running:")
        print("  cd python_backend")
        print("  python start_server.py")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    
    api_url = os.environ.get("VITE_EMERGENCY_API_URL", "http://localhost:8000")
    endpoint = f"{api_url}/api/health"
    
    try:
        print("Testing health check endpoint...")
        response = requests.get(endpoint, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 BrightSide Emergency Notification Test")
    print("=" * 50)
    
    # Test health check first
    if test_health_check():
        print("\n" + "=" * 50)
        # Test emergency notification
        test_emergency_notification()
    else:
        print("\nHealth check failed. Please ensure the server is running.")
    
    print("\n" + "=" * 50)
    print("Test completed.")
