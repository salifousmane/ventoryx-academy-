FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p media/vault logs && \
    chmod +x manage.py

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health/ || exit 1

# Collect static files
RUN python manage.py collectstatic --noinput --clear

EXPOSE 8080

CMD ["gunicorn", "wsgi:application", "-w", "4", "-b", "0.0.0.0:8080", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-"]
