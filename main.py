from website import create_app
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Your local IP: {local_ip}")

app = create_app()
if __name__ == '__main__':
    print(f"Access the app at: http://{local_ip}:5000")
    app.run(host='localhost', port=5000, debug=True)
