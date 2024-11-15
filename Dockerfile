# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy your bot code and requirements.txt into the container
COPY bot.py /app
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add a loop to restart every 4 hours
CMD ["sh", "-c", "while true; do python bot.py; sleep 14400; done"]
