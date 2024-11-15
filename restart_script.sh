#!/bin/bash

while true; do
    echo "Starting the bot..."
    python bot.py
    echo "Restarting in 6 hours..."
    sleep 21600 # 6 hours in seconds
done
