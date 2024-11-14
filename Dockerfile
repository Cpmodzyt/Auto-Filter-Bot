# Use Python 3.11 as the base image
FROM python:3.11

# Set the working directory
WORKDIR /Auto-Filter-Bot

# Copy all contents to the container's working directory
COPY . /Auto-Filter-Bot

# Install the required Python packages
RUN pip install -r requirements.txt

# Install cron to enable scheduled restarts
RUN apt-get update && apt-get install -y cron

# Create a cron job to restart the bot every 2 hours
RUN echo "0 */2 * * * /usr/bin/pkill -f bot.py" > /etc/cron.d/bot-cron

# Apply permissions and enable the cron job
RUN chmod 0644 /etc/cron.d/bot-cron && crontab /etc/cron.d/bot-cron

# Start the cron service and the bot script
CMD cron && python bot.py
