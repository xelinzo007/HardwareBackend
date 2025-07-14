# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libpq-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pre-install dependencies (allows Docker cache reuse)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application code
COPY . .

# Expose the required port (important for Render)
EXPOSE 10000

# Start the FastAPI app with correct host/port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
