import requests

API_URL = "http://localhost:8000/api/v1/auth/login"

def test_multipart_login():
    print("Testing Multipart Login Request...")
    try:
        # requests.post with files argument sends multipart/form-data
        # But for form fields, we usually can just allow requests to handle it if we don't pass files
        # However, to strictly simulate what JS FormData does (multipart), we can do this:
        
        # Method 1: requests handles 'data' as urlencoded by default. 
        # To force multipart without files, it's a bit tricky in requests.
        # But let's try standard 'files' dict with None filename to simulate fields in multipart
        
        # Actually easier: let's just assume the Frontend sends FormData.
        # Let's try to mimic it.
        
        files = {
            'username': (None, 'user'),
            'password': (None, 'password')
        }
        
        response = requests.post(API_URL, files=files)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
            print("✅ Multipart Login Successful!")
        else:
            print("Response:", response.text)
            print("❌ Multipart Login Failed")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_multipart_login()
