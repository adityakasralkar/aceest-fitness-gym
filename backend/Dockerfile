# Use official Python slim image - smaller size, more secure
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

ARG APP_VERSION=local
ARG DEPLOYMENT_VARIANT=docker

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    APP_VERSION=${APP_VERSION} \
    DEPLOYMENT_VARIANT=${DEPLOYMENT_VARIANT}

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Health check for Docker smoke tests and local verification
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3).read()"

# Run the application
CMD ["python", "app.py"]
