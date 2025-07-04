FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create entrypoint script with better error handling
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Waiting for database..."\n\
while ! nc -z db 5432; do\n\
  sleep 0.1\n\
done\n\
\n\
echo "Database is ready!"\n\
\n\
echo "Running database migrations..."\n\
alembic upgrade head || {\n\
  echo "Migration failed, but continuing..."\n\
}\n\
\n\
echo "Initializing database with default data..."\n\
python scripts/init_db.py || {\n\
  echo "Database initialization failed, but continuing..."\n\
}\n\
\n\
echo "Starting the application..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload\n\
' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Create a healthcheck script
RUN echo '#!/bin/bash\n\
curl -f http://localhost:8000/api/v1/health || exit 1\n\
' > /app/healthcheck.sh && chmod +x /app/healthcheck.sh

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD ["/app/healthcheck.sh"]

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["/app/entrypoint.sh"] 