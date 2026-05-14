from flask import Flask, request
import requests
import socket
import os

app = Flask(__name__)

def get_tel_aviv_temperature():
    """Fetch current temperature in Tel-Aviv using OpenWeatherMap API"""
    try:
        # Using wttr.in service which doesn't require API key
        response = requests.get('https://wttr.in/Tel-Aviv?format=%t', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "N/A"
    except Exception as e:
        print(f"Error fetching temperature: {e}")
        return "N/A"

@app.route('/')
def home():
    # Get client IP - check multiple headers
    client_ip = (
        request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or
        request.headers.get('X-Real-IP', '').strip() or
        request.environ.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or
        request.remote_addr
    )

    # Get container name (hostname in Kubernetes)
    container_name = socket.gethostname()

    # Get Tel-Aviv temperature
    temperature = get_tel_aviv_temperature()

    # Simple text response
    return f"Hello {client_ip} and welcome to Silverfort's {container_name}, Current Temperature in Tel-Aviv is {temperature}"

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    # Run with HTTPS using self-signed certificates
    app.run(
        host='0.0.0.0',
        port=5555,
        ssl_context=('/app/certs/cert.pem', '/app/certs/key.pem')
    )
