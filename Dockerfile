FROM python:3.11

# Install cron
RUN apt-get update && apt-get install -y cron

# Set working directory
WORKDIR /Auto-Filter-Bot

# Copy the current directory contents into the container at /Auto-Filter-Bot
COPY . /Auto-Filter-Bot

# Install Python dependencies
RUN pip install -r requirements.txt

# Create a cron job to restart the bot every minute
RUN echo "* * * * * cd /Auto-Filter-Bot && /usr/bin/python bot.py" > /etc/cron.d/restart-bot

# Give execution rights on the cron job file
RUN chmod 0644 /etc/cron.d/restart-bot

# Apply cron job
RUN crontab /etc/cron.d/restart-bot

# Start cron in the background and then run the bot
CMD ["cron", "-f"]
