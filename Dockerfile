# Use a base Python image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev \
    wget \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 8501 (Streamlit's default port)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "project_tooling.py", "--server.port=8501", "--server.address=0.0.0.0"]
