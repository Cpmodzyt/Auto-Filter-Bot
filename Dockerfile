FROM python:3.11

WORKDIR /Auto-Filter-Bot

COPY . /Auto-Filter-Bot

RUN pip install -r requirements.txt

# Add a script to handle restarts every 6 hours
COPY restart_script.sh /restart_script.sh
RUN chmod +x /restart_script.sh

CMD ["/restart_script.sh"]
