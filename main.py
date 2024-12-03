import discord
import os
import random
import asyncio
import time
from datetime import datetime
from discord.ext import commands
from flask import Flask
from threading import Thread

# Intents setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for reading message content

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

start_time = time.time()  # Track the bot's uptime


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(cookie_reactor())  # Start cookie reactor
    print("Bot is running!")


# 1. Respond to "What is your name?"
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == "what is your name?":
        await message.channel.send("My name is Voltiee <3")

    await bot.process_commands(message)  # Process other commands


# 2. Set an alarm
@bot.command()
async def alarm(ctx, time_in_seconds: int, *, message: str):
    """Set an alarm."""
    await ctx.send(f"Alarm set for {time_in_seconds} seconds!")
    await asyncio.sleep(time_in_seconds)
    await ctx.send(f"⏰ Alarm! {message}")


# 3. Set a timer
@bot.command()
async def timer(ctx, time_in_seconds: int):
    """Set a timer."""
    await ctx.send(f"Timer started for {time_in_seconds} seconds!")
    await asyncio.sleep(time_in_seconds)
    await ctx.send("⏰ Time's up!")


# 4. Send a user-defined message
@bot.command()
async def say(ctx, *, message: str):
    """Command for the bot to say something."""
    await ctx.send(message)


# 5. Uptime command
@bot.command()
async def uptime(ctx):
    """Check the bot's uptime."""
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_string = str(datetime.utcfromtimestamp(uptime_seconds).strftime("%H:%M:%S"))
    await ctx.send(f"I've been running for {uptime_string}!")


# 6. Cookie Reactor
async def cookie_reactor():
    """React to a random message in each channel every 30 seconds."""
    await bot.wait_until_ready()
    while True:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    messages = await channel.history(limit=20).flatten()
                    if messages:
                        random_message = random.choice(messages)
                        await random_message.add_reaction("🍪")
                        print(f"Reacted to a message in {channel.name}")
                except Exception as e:
                    print(f"Error in cookie_reactor: {e}")
        await asyncio.sleep(30)


# 7. Restart command
@bot.command()
async def restart(ctx):
    """Restart the bot."""
    await ctx.send("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)  # Restarts the bot


# 8. Flask server for uptime monitoring
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

# Run the Flask server in a separate thread
Thread(target=run).start()


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
