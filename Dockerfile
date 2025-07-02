# Use the official lightweight Python image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies, including git for pip install of fastapi-admin-patched
RUN apt-get update && apt-get install -y build-essential git

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Render expects
EXPOSE 10000

# Start FastAPI with uvicorn using the PORT Render provides
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
