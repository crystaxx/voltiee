import discord
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

import asyncio
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# Set up the Flask app to keep the bot alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Set up your bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store the bot's start time to calculate uptime
start_time = datetime.now()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Say command: The bot repeats the given message
@bot.command()
async def say(ctx, *, message: str):
    """Bot will repeat whatever you say."""
    await ctx.send(message)

# Set Alarm command: The bot will set a reminder to send a message after a specified delay
@bot.command()
async def setalarm(ctx, time: str, *, message: str):
    """Set an alarm that will remind you after a specified time (in minutes)."""

    try:
        # Convert the given time to an integer (minutes)
        alarm_time = int(time)
        if alarm_time <= 0:
            await ctx.send("Please provide a positive number of minutes.")
            return

        await ctx.send(f"Alarm set! I will remind you in {alarm_time} minute(s).")

        # Wait for the given amount of time (in seconds)
        await asyncio.sleep(alarm_time * 60)

        # Send the reminder
        await ctx.send(f"Reminder: {message}")

    except ValueError:
        await ctx.send("Please provide a valid number of minutes.")

# Uptime command: The bot will tell you how long it's been running
@bot.command()
async def uptime(ctx):
    """Tells you how long the bot has been online."""
    current_time = datetime.now()
    uptime_duration = current_time - start_time

    # Format the uptime duration into hours, minutes, and seconds
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Send the uptime message
    await ctx.send(f"I've been running for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")

# Run Flask server in a separate thread to keep the bot alive
Thread(target=run).start()

# Run the bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
