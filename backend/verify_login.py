import requests
import asyncio
import aiohttp

API_URL = "http://localhost:8000/api/v1/auth/login"

def test_sync_login():
    print("Testing Synchronous Login Request...")
    try:
        payload = {
            "username": "user",
            "password": "password"
        }
        # FastAPI OAuth2PasswordRequestForm expects form-data, not json
        response = requests.post(API_URL, data=payload)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
            print("✅ Login Successful!")
            return True
        else:
            print("Response:", response.text)
            print("❌ Login Failed")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_sync_login()
