import discord
from discord.ext import commands
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

# Timer command: The bot will start a timer for the specified number of minutes
@bot.command()
async def timer(ctx, time: str):
    """Set a timer and the bot will remind you when time is up (in minutes)."""
    
    try:
        # Convert the time to minutes
        timer_time = int(time)
        if timer_time <= 0:
            await ctx.send("Please provide a positive number of minutes.")
            return
        
        await ctx.send(f"Timer started for {timer_time} minute(s). I'll remind you when it's over.")

        # Wait for the timer to finish
        await asyncio.sleep(timer_time * 60)

        # Notify the user when the timer is up
        await ctx.send("Time's up!")

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

# Respond to "What is your name?"
@bot.command()
async def whatisname(ctx):
    """Responds with the bot's name."""
    await ctx.send("My name is Voltiee <3")

# Run Flask server in a separate thread to keep the bot alive
Thread(target=run).start()

# Run the bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
