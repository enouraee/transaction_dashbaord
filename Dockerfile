# Use a stable Python version
FROM python:3.11-slim-buster

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Change ownership to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED 1
