FROM python:3.11

# Install cron
RUN apt-get update && apt-get install -y cron

# Set working directory
WORKDIR /Auto-Filter-Bot

# Copy the current directory contents into the container at /Auto-Filter-Bot
COPY . /Auto-Filter-Bot

# Install Python dependencies
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
