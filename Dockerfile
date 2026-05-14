# Use Python 3.11 slim image as base
FROM python:3.11-slim

WORKDIR /app

# Install OpenSSL for generating self-signed SSL certificate
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create directory for SSL certificates
RUN mkdir -p /app/certs

# Generate self-signed SSL certificate for HTTPS
RUN openssl req -x509 -newkey rsa:4096 -nodes \
    -out /app/certs/cert.pem \
    -keyout /app/certs/key.pem \
    -days 365 \
    -subj "/C=IL/ST=TelAviv/L=TelAviv/O=Silverfort/OU=DevOps/CN=silverfort.local"

# Expose application port
EXPOSE 5555

# Start the Flask application
CMD ["python", "app.py"]
