import subprocess
import time
import requests

# Start Flask server before tests
flask_process = subprocess.Popen(["python", "main.py"])
time.sleep(10)  # Give server time to start

def test_api_status():
    try:
        response = requests.get("http://localhost:5000")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as e:
        print("Connection Error:", e)
        assert False  # Force test to fail with an error message

# Stop server after tests
flask_process.terminate()
