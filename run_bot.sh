#!/bin/bash

# Discord Permission Management Bot Startup Script

echo "Starting Discord Permission Management Bot..."
echo "Make sure you have added your bot token to the .env file"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your Discord bot token:"
    echo "DISCORD_TOKEN=your_token_here"
    exit 1
fi

# Check if requirements are installed
if ! python -c "import discord" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

echo "Starting the bot..."
python permission_bot.py