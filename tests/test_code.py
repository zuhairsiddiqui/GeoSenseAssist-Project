import subprocess
import time
import requests

# Start Flask server before tests
flask_process = subprocess.Popen(["python", "main.py"])
time.sleep(2)  # Give server time to start

def test_api_status():
    response = requests.get("http://0.0.0.0:5000")
    assert response.status_code == 200

# Stop server after tests
flask_process.terminate()
