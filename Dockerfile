FROM python:3.11

WORKDIR /Auto-Filter-Bot

# Copy all contents to the container's working directory
COPY . /Auto-Filter-Bot

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y cron

# Create a cron job to restart the bot every 4 hours
RUN echo "0 */4 * * * /usr/bin/pkill -f bot.py" > /etc/cron.d/bot-cron

RUN chmod 0644 /etc/cron.d/bot-cron && crontab /etc/cron.d/bot-cron

CMD cron && python bot.py
