import subprocess
import time
import requests

# Start Flask server before tests
flask_process = subprocess.Popen(["python", "main.py"])

# Wait for the server to be fully ready (with retry logic)
def wait_for_server(url='http://localhost:5000', timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    return False

def test_api_status():
    # Wait for the server to start
    if wait_for_server():
        # Make HTTP requests to the server
        response = requests.get('http://localhost:5000')
        assert response.status_code == 200
    else:
        print("Server failed to start in time.")
        assert False  # Fail the test if the server didn't start in time

# Stop server after tests
flask_process.terminate()
