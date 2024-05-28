# Use a smaller base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /smscenter

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy the current directory contents into the container at /smscenter
COPY . /smscenter

# Expose port 8002 to the outside world
EXPOSE 8010

# Command to run the application
CMD ["gunicorn", "--bind", "127.0.0.1:8010", "smscenter.wsgi:application"]
