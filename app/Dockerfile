# Stage 1: Build stage
FROM python:3.12-slim as build-stage

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Stage 2: Production stage
FROM python:3.12-slim as production-stage

# Set the working directory
WORKDIR /app

# Install runtime dependencies (PostgreSQL client libraries)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files from the build stage
COPY --from=build-stage /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build-stage /app /app

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["python", "app.py"]
