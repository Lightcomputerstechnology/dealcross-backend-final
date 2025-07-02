# Use the official lightweight Python image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Ensure .env is included
COPY .env .env

# Expose your FastAPI port
EXPOSE 10000

# Start FastAPI with uvicorn with correct port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--log-level", "debug"]
