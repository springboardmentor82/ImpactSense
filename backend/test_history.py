import requests
import random

BASE_URL = "http://localhost:8000"

def test_impactsense():
    # 1. Register a new test user
    test_email = f"test_{random.randint(1000, 9999)}@example.com"
    test_password = "password123"
    
    print(f"--- Testing with {test_email} ---")
    
    reg_resp = requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": test_email,
        "password": test_password
    })
    try:
        print(f"Registration: {reg_resp.status_code} - {reg_resp.json()}")
    except Exception:
        print(f"Registration: {reg_resp.status_code} - FAILED TO DECODE JSON. Response text: {reg_resp.text}")
        return
    
    # 2. Login to get token
    login_resp = requests.post(f"{BASE_URL}/api/auth/login", data={
        "username": test_email,
        "password": test_password
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Login: Success (Token acquired)")
    
    # 3. Perform a prediction
    print("Performing prediction...")
    predict_resp = requests.post(f"{BASE_URL}/api/predict", json={
        "cdi": 4.5,
        "mmi": 5.0,
        "sig": 600,
        "magnitude": 6.5,
        "depth": 10.0
    }, headers=headers)
    print(f"Prediction: {predict_resp.status_code} - result: {predict_resp.json()['alert']}")
    
    # 4. Check history
    print("Fetching history...")
    history_resp = requests.get(f"{BASE_URL}/api/history", headers=headers)
    history = history_resp.json()
    print(f"History: Found {len(history)} entries")
    
    if len(history) > 0:
        entry = history[0]
        print(f"Latest entry: {entry['alert_level']} alert at {entry['timestamp']}")
        if entry['alert_level'] == predict_resp.json()['alert']:
            print("SUCCESS: History matches prediction!")
        else:
            print("FAILURE: History mismatch.")
    else:
        print("FAILURE: No history found.")

if __name__ == "__main__":
    try:
        test_impactsense()
    except Exception as e:
        print(f"Error during test: {e}")
        print("Make sure the backend is running at http://localhost:8000")
