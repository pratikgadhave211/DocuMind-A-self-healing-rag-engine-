FROM python:3.13-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (if any are needed by Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the app runs on (Railway sets the PORT environment variable)
EXPOSE ${PORT:-8000}

# Run the FastAPI application using uvicorn directly for production (avoids reload=True)
CMD uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8000}
