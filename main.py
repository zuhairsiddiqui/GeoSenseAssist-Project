from website import create_app
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Your local IP: {local_ip}")

app = create_app()
if __name__ == '__main__':
    print(f"Access the app at: http://{local_ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)


from website import create_app
import os
import socket

# Get the environment variable (default to "development" if not set, so people can run their website locally to check for changes)
flask_env = os.getenv("FLASK_ENV", "development")

if flask_env == "deployment":
    # If we are deploying, use the configurations for Heroku
    port = int(os.getenv("PORT", 5000))

    app = create_app()

    if __name__ == '__main__':
        print(f"Website is live at: https://geosenseassist-3f7440326683.herokuapp.com/")
        app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Local Development Configuration (for when you run it locally)
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f"Your local IP: {local_ip}")

    app = create_app()

    if __name__ == '__main__':
        print(f"Access the app at: http://{local_ip}:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
